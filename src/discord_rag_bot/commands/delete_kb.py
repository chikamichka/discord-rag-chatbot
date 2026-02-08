import discord
from discord_rag_bot.core import RAGEngine


class DeleteKBCommand:
    """Delete knowledge bases"""
    
    def __init__(self, engine: RAGEngine):
        self.engine = engine
    
    async def execute(
        self,
        interaction: discord.Interaction,
        kb_name: str
    ):
        """
        Delete a knowledge base
        
        Args:
            interaction: Discord interaction
            kb_name: Knowledge base name to delete
        """
        await interaction.response.defer()
        
        try:
            # Find knowledge base
            kb = self.engine.kb_manager.find_kb_by_name(
                str(interaction.user.id),
                kb_name
            )
            
            if not kb:
                embed = discord.Embed(
                    title="❌ Knowledge Base Not Found",
                    description=f"You don't have a knowledge base named **{kb_name}**",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Delete knowledge base
            success = self.engine.delete_knowledge_base(kb.kb_id)
            
            if success:
                embed = discord.Embed(
                    title="✅ Knowledge Base Deleted",
                    description=f"**{kb.name}** has been permanently deleted",
                    color=discord.Color.green()
                )
                embed.add_field(
                    name="📊 Statistics",
                    value=f"• {kb.total_chunks} chunks removed\n• {kb.processed_files} files deleted",
                    inline=False
                )
            else:
                embed = discord.Embed(
                    title="❌ Deletion Failed",
                    description="Could not delete the knowledge base",
                    color=discord.Color.red()
                )
            
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to delete knowledge base: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)