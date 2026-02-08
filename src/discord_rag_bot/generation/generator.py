from typing import List, Dict, Any
import ollama
from discord_rag_bot.utils.config import Config


class AnswerGenerator:
    """Generate answers using Ollama LLM"""
    
    def __init__(self, model_name: str = None):
        """
        Initialize generator
        
        Args:
            model_name: Ollama model name
        """
        self.model_name = model_name or Config.OLLAMA_MODEL
        print(f"🤖 Using LLM: {self.model_name}")
    
    def generate(
        self,
        query: str,
        context_chunks: List[Dict[str, Any]],
        temperature: float = 0.7,
        max_tokens: int = 300
    ) -> str:
        """
        Generate answer based on query and context
        
        Args:
            query: User question
            context_chunks: Retrieved chunks with metadata
            temperature: LLM temperature (0-1)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated answer
        """
        # Build context from chunks
        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            source = chunk['metadata'].get('source', 'Unknown')
            content = chunk['content']
            context_parts.append(f"[Source {i}: {source}]\n{content}")
        
        context = "\n\n".join(context_parts)
        
        # Create prompt
        prompt = self._build_prompt(query, context)
        
        # Generate with Ollama
        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            )
            return response['response'].strip()
        
        except Exception as e:
            return f"❌ Error generating answer: {str(e)}\nMake sure Ollama is running (ollama serve)"

    def generate_summary(self, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Generate a summary of the document
        
        Args:
            context_chunks: All available chunks
            
        Returns:
            Document summary
        """
        # Get a sample of chunks for summary
        sample_chunks = context_chunks[:5] if len(context_chunks) > 5 else context_chunks
        context = "\n\n".join([chunk['content'] for chunk in sample_chunks])
        
        prompt = f"""You are a helpful AI assistant. Based on the following excerpts from a document, provide a clear, concise summary of what the document is about.

Focus on:
1. Main topic/subject
2. Key points or findings
3. Purpose of the document

Document excerpts:
{context}

Provide a 2-3 sentence summary of what this document is about:"""
        
        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={"temperature": 0.7, "num_predict": 200}
            )
            return response['response'].strip()
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def _build_prompt(self, query: str, context: str) -> str:
        """
        Build the prompt for the LLM
        
        Args:
            query: User question
            context: Retrieved context
            
        Returns:
            Formatted prompt
        """
        prompt = f"""You are a helpful AI assistant for the AI Bootcamp Discord server.

Your role is to answer questions about the bootcamp materials based on the provided context.

RULES:
1. Answer ONLY using information from the context below
2. If the answer is not in the context, say "I don't have that information in the knowledge base."
3. Keep answers concise and helpful (2-4 sentences)
4. Cite the source number when referencing specific information
5. Be friendly and encouraging - these are students learning!

CONTEXT FROM KNOWLEDGE BASE:
{context}

STUDENT QUESTION: {query}

ANSWER:"""
        
        return prompt