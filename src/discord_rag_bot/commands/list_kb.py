import discord
from discord_rag_bot.core import RAGEngine


class ListKBCommand:
    """List user's knowledge bases"""
    
    def __init__(self, engine: RAGEngine):
        self.engine = engine
    
    async def execute(self, interaction: discord.Interaction):
        """
        List all knowledge bases for the user
        
        Args:
            interaction: Discord interaction
        """
        await interaction.response.defer()
        
        try:
            # Get user's knowledge bases
            kbs = self.engine.get_user_knowledge_bases(str(interaction.user.id))
            
            if not kbs:
                embed = discord.Embed(
                    title="📚 Your Knowledge Bases",
                    description="You don't have any knowledge bases yet!",
                    color=discord.Color.blue()
                )
                embed.add_field(
                    name="💡 Get Started",
                    value="Use `/upload` to create your first knowledge base",
                    inline=False
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Create embed
            embed = discord.Embed(
                title=f"📚 Your Knowledge Bases ({len(kbs)})",
                description=f"You have {len(kbs)} knowledge base(s)",
                color=discord.Color.green()
            )
            
            for kb in kbs:
                # Status emoji
                status_emoji = {
                    "success": "✅",
                    "processing": "⚙️",
                    "failed": "❌",
                    "partial": "⚠️",
                    "pending": "⏳"
                }.get(kb.status.value, "❓")
                
                # KB info
                value = (
                    f"{status_emoji} **Status**: {kb.status.value}\n"
                    f"📊 **Chunks**: {kb.total_chunks}\n"
                    f"📄 **Files**: {kb.processed_files} processed, {kb.failed_files} failed\n"
                    f"🕒 **Created**: {kb.created_at.strftime('%Y-%m-%d %H:%M')}"
                )
                
                if kb.description:
                    value += f"\n📝 {kb.description}"
                
                embed.add_field(
                    name=kb.name,
                    value=value,
                    inline=False
                )
            
            embed.set_footer(text="Use /ask <kb_name> <question> to query a knowledge base")
            
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to list knowledge bases: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)