import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from pathlib import Path

from discord_rag_bot.core import RAGEngine
from discord_rag_bot.commands import UploadCommand, AskCommand, ListKBCommand, DeleteKBCommand
from discord_rag_bot.utils.config import Config


class RAGBot(commands.Bot):
    """Discord RAG Bot"""
    
    def __init__(self):
        """Initialize bot"""
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(
            command_prefix=Config.DISCORD_PREFIX,
            intents=intents,
            help_command=None
        )
        
        # Initialize RAG engine
        print("🚀 Initializing RAG Engine...")
        self.rag_engine = RAGEngine()
        
        # Initialize commands
        self.upload_cmd = UploadCommand(self.rag_engine)
        self.ask_cmd = AskCommand(self.rag_engine)
        self.list_cmd = ListKBCommand(self.rag_engine)
        self.delete_cmd = DeleteKBCommand(self.rag_engine)
    
    async def setup_hook(self):
        """Setup hook - called when bot starts"""
        # Register slash commands
        await self.register_commands()
        
        # Sync commands with Discord
        print("🔄 Syncing commands with Discord...")
        await self.tree.sync()
        print("✅ Commands synced!")
    
    async def register_commands(self):
        """Register all slash commands"""
        
        # /upload command
        @self.tree.command(
            name="upload",
            description="Upload files to create a knowledge base"
        )
        @app_commands.describe(
            name="Name for the knowledge base",
            file1="First file (required)",
            file2="Second file (optional)",
            file3="Third file (optional)",
            file4="Fourth file (optional)",
            file5="Fifth file (optional)",
            description="Description of the knowledge base"
        )
        async def upload(
            interaction: discord.Interaction,
            name: str,
            file1: discord.Attachment,
            file2: discord.Attachment = None,
            file3: discord.Attachment = None,
            file4: discord.Attachment = None,
            file5: discord.Attachment = None,
            description: str = ""
        ):
            files = [f for f in [file1, file2, file3, file4, file5] if f is not None]
            await self.upload_cmd.execute(interaction, name, files, description)
        
        # /ask command
        @self.tree.command(
            name="ask",
            description="Ask a question to your knowledge base"
        )
        @app_commands.describe(
            kb_name="Name of the knowledge base to query",
            question="Your question"
        )
        async def ask(
            interaction: discord.Interaction,
            kb_name: str,
            question: str
        ):
            await self.ask_cmd.execute(interaction, kb_name, question)
        
        # /list-kb command
        @self.tree.command(
            name="list-kb",
            description="List all your knowledge bases"
        )
        async def list_kb(interaction: discord.Interaction):
            await self.list_cmd.execute(interaction)
        
        # /delete-kb command
        @self.tree.command(
            name="delete-kb",
            description="Delete a knowledge base"
        )
        @app_commands.describe(
            kb_name="Name of the knowledge base to delete"
        )
        async def delete_kb(
            interaction: discord.Interaction,
            kb_name: str
        ):
            await self.delete_cmd.execute(interaction, kb_name)
        
        # /help command
        @self.tree.command(
            name="help",
            description="Show help and available commands"
        )
        async def help_command(interaction: discord.Interaction):
            embed = discord.Embed(
                title="🤖 AI Bootcamp RAG Bot",
                description="Upload documents and ask questions powered by AI!",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="📤 /upload",
                value="Upload files to create a knowledge base\n`/upload name:<kb_name> file1:<file>`",
                inline=False
            )
            
            embed.add_field(
                name="💬 /ask",
                value="Ask questions to your knowledge base\n`/ask kb_name:<name> question:<question>`",
                inline=False
            )
            
            embed.add_field(
                name="📚 /list-kb",
                value="List all your knowledge bases\n`/list-kb`",
                inline=False
            )
            
            embed.add_field(
                name="🗑️ /delete-kb",
                value="Delete a knowledge base\n`/delete-kb kb_name:<name>`",
                inline=False
            )
            
            embed.add_field(
                name="📖 Supported File Types",
                value="PDF, DOCX, TXT, MD",
                inline=True
            )
            
            embed.add_field(
                name="📏 File Size Limit",
                value=f"{Config.MAX_FILE_SIZE_MB}MB per file",
                inline=True
            )
                        
            await interaction.response.send_message(embed=embed)
    
    async def on_ready(self):
        """Called when bot is ready"""
        print("\n" + "="*70)
        print(f"✅ Bot is ready! Logged in as {self.user}")
        print(f"📊 Connected to {len(self.guilds)} server(s)")
        print("="*70 + "\n")
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="for /help"
            )
        )
    
    async def on_command_error(self, ctx, error):
        """Handle command errors"""
        print(f"❌ Error: {error}")


def main():
    """Main entry point"""
    # Validate config
    try:
        Config.validate()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\n💡 Make sure you've set DISCORD_BOT_TOKEN in your .env file")
        return
    
    # Create and run bot
    bot = RAGBot()
    
    print("\n" + "="*70)
    print("🤖 DISCORD RAG BOT")
    print("="*70)
    print(f"📁 Data directory: {Config.DATA_DIR}")
    print(f"💾 Vector DB: {Config.CHROMADB_DIR}")
    print(f"📊 Embedding model: {Config.EMBEDDING_MODEL}")
    print(f"🤖 LLM model: {Config.OLLAMA_MODEL}")
    print("="*70 + "\n")
    
    print("🔌 Starting bot...\n")
    
    try:
        bot.run(Config.DISCORD_TOKEN)
    except discord.errors.LoginFailure:
        print("❌ Invalid bot token! Check your .env file")
    except KeyboardInterrupt:
        print("\n👋 Bot stopped")


if __name__ == "__main__":
    main()