import discord
from discord import app_commands
from typing import List
from pathlib import Path
import aiofiles
from discord_rag_bot.core import RAGEngine, ProcessingStatus
from discord_rag_bot.utils.config import Config


class UploadCommand:
    """Handle file uploads and KB creation"""
    
    def __init__(self, engine: RAGEngine):
        self.engine = engine
    
    async def execute(
        self,
        interaction: discord.Interaction,
        name: str,
        files: List[discord.Attachment],
        description: str = ""
    ):
        """
        Upload files and create knowledge base
        
        Args:
            interaction: Discord interaction
            name: Knowledge base name
            files: List of attached files
            description: Optional description
        """
        # Defer response (processing might take time)
        await interaction.response.defer(ephemeral=False)
        
        try:
            # Validate files
            validation_errors = await self._validate_files(files)
            if validation_errors:
                await interaction.followup.send(
                    embed=self._create_error_embed(
                        "File Validation Failed",
                        "\n".join(validation_errors)
                    )
                )
                return
            
            # Send initial status
            status_embed = discord.Embed(
                title="📤 Uploading Files",
                description=f"Creating knowledge base: **{name}**",
                color=discord.Color.blue()
            )
            status_embed.add_field(
                name="Files",
                value=f"{len(files)} file(s) uploading...",
                inline=False
            )
            status_message = await interaction.followup.send(embed=status_embed)
            
            # Download files
            file_paths = await self._download_files(files, interaction.user.id)
            
            # Create progress callback
            async def progress_callback(filename: str, current: int, total: int):
                percentage = int((current / total) * 100)
                
                embed = discord.Embed(
                    title="⚙️ Processing Files",
                    description=f"Knowledge Base: **{name}**",
                    color=discord.Color.orange()
                )
                embed.add_field(
                    name="Progress",
                    value=f"{current}/{total} files ({percentage}%)",
                    inline=False
                )
                embed.add_field(
                    name="Current File",
                    value=f"📄 {filename}",
                    inline=False
                )
                
                await status_message.edit(embed=embed)
            
            # Create knowledge base
            kb = await self.engine.create_knowledge_base(
                name=name,
                owner_id=str(interaction.user.id),
                owner_name=str(interaction.user),
                file_paths=file_paths,
                description=description,
                progress_callback=progress_callback
            )
            
            # Cleanup downloaded files
            for path in file_paths:
                path.unlink(missing_ok=True)
            
            # Send final result
            if kb.status == ProcessingStatus.SUCCESS:
                embed = self._create_success_embed(kb)
            elif kb.status == ProcessingStatus.PARTIAL:
                embed = self._create_partial_embed(kb)
            else:
                embed = self._create_error_embed(
                    "Processing Failed",
                    "All files failed to process. Check the error details."
                )
            
            await status_message.edit(embed=embed)
        
        except Exception as e:
            await interaction.followup.send(
                embed=self._create_error_embed("Error", str(e))
            )
    
    async def _validate_files(self, files: List[discord.Attachment]) -> List[str]:
        """Validate uploaded files"""
        errors = []
        
        if not files:
            errors.append("❌ No files attached")
            return errors
        
        if len(files) > 10:
            errors.append(f"❌ Too many files (max 10, got {len(files)})")
        
        max_size = Config.MAX_FILE_SIZE_MB * 1024 * 1024  # Convert to bytes
        
        for file in files:
            # Check file size
            if file.size > max_size:
                errors.append(f"❌ {file.filename}: Too large ({file.size / 1024 / 1024:.1f}MB > {Config.MAX_FILE_SIZE_MB}MB)")
            
            # Check file type
            suffix = Path(file.filename).suffix.lower()
            if suffix not in Config.ALLOWED_EXTENSIONS:
                errors.append(f"❌ {file.filename}: Unsupported format (allowed: {', '.join(Config.ALLOWED_EXTENSIONS)})")
        
        return errors
    
    async def _download_files(
        self,
        attachments: List[discord.Attachment],
        user_id: int
    ) -> List[Path]:
        """Download files to temporary location"""
        user_upload_dir = Config.UPLOADS_DIR / str(user_id)
        user_upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_paths = []
        
        for attachment in attachments:
            file_path = user_upload_dir / attachment.filename
            
            # Download file
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(await attachment.read())
            
            file_paths.append(file_path)
        
        return file_paths
    
    def _create_success_embed(self, kb) -> discord.Embed:
        """Create success embed"""
        embed = discord.Embed(
            title="✅ Knowledge Base Created!",
            description=f"**{kb.name}** is ready to answer questions!",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="📊 Statistics",
            value=f"• Files: {kb.processed_files}\n• Chunks: {kb.total_chunks}\n• Status: {kb.status.value}",
            inline=False
        )
        
        if kb.description:
            embed.add_field(
                name="📝 Description",
                value=kb.description,
                inline=False
            )
        
        embed.add_field(
            name="💡 How to Use",
            value=f"Use `/ask` to query this knowledge base!",
            inline=False
        )
        
        embed.set_footer(text=f"KB ID: {kb.kb_id}")
        
        return embed
    
    def _create_partial_embed(self, kb) -> discord.Embed:
        """Create partial success embed"""
        embed = discord.Embed(
            title="⚠️ Knowledge Base Created (With Errors)",
            description=f"**{kb.name}** was created but some files failed",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="📊 Statistics",
            value=f"• Processed: {kb.processed_files}\n• Failed: {kb.failed_files}\n• Chunks: {kb.total_chunks}",
            inline=False
        )
        
        if kb.errors:
            error_text = "\n".join([f"• {e['filename']}: {e['error'][:50]}..." for e in kb.errors[:3]])
            embed.add_field(
                name="❌ Errors",
                value=error_text,
                inline=False
            )
        
        return embed
    
    def _create_error_embed(self, title: str, message: str) -> discord.Embed:
        """Create error embed"""
        embed = discord.Embed(
            title=f"❌ {title}",
            description=message,
            color=discord.Color.red()
        )
        return embed