import discord
from discord_rag_bot.core import RAGEngine


class AskCommand:
    """Handle questions to knowledge bases"""
    
    def __init__(self, engine: RAGEngine):
        self.engine = engine
    
    async def execute(
        self,
        interaction: discord.Interaction,
        kb_name: str,
        question: str
    ):
        """
        Ask a question to a knowledge base
        
        Args:
            interaction: Discord interaction
            kb_name: Knowledge base name
            question: User's question
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
                embed.add_field(
                    name="💡 Tip",
                    value="Use `/list-kb` to see your knowledge bases",
                    inline=False
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Check status
            if kb.status.value != "success":
                embed = discord.Embed(
                    title="⚠️ Knowledge Base Not Ready",
                    description=f"**{kb.name}** is currently {kb.status.value}",
                    color=discord.Color.orange()
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Query the knowledge base
            result = self.engine.query_knowledge_base(kb.kb_id, question)
            
            # Create response embed
            embed = discord.Embed(
                title="💬 Answer",
                description=result['answer'],
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="📚 Knowledge Base",
                value=kb.name,
                inline=True
            )
            
            embed.add_field(
                name="📊 Sources",
                value=f"{result['num_chunks_retrieved']} chunks retrieved",
                inline=True
            )
            
            embed.set_footer(text=f"Question: {question}")
            
            # Show sources (optional - first chunk preview)
            if result['chunks']:
                top_chunk = result['chunks'][0]
                source_preview = top_chunk['content'][:150] + "..."
                source_name = top_chunk['metadata'].get('filename', 'Unknown')
                
                embed.add_field(
                    name=f"📄 Top Source: {source_name}",
                    value=f"```{source_preview}```",
                    inline=False
                )
            
            await interaction.followup.send(embed=embed)
        
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to answer question: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)