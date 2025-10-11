# import asyncio
# from app.agents.state import AgentState
# from app.agents.config import get_llm, default_agent_config

# class SolverNode:
#     """
#     A node that generates a final answer based on the retrieved context, including citations.
#     """
#     def __init__(self, config=None):
#         self.llm = get_llm(config or default_agent_config)

#     async def __call__(self, state: AgentState) -> AgentState:
#         print("--- ✍️ Solver Node ---")
        
#         context_str = "\n\n".join([f"[{i+1}] {chunk['text']}" for i, chunk in enumerate(state['context'])])
        
#         prompt = f"""You are a world-class synthesis expert. Your task is to answer the user's query based *only* on the provided context.
        
#         Here is the retrieved context:
#         ---
#         {context_str}
#         ---
        
#         User's Query: "{state['query']}"
        
#         Your instructions:
#         1. Formulate a comprehensive answer to the user's query.
#         2. You MUST cite the context in your answer using the format [1], [2], etc.
#         3. If the context does not contain enough information to answer the query, state that clearly.
#         4. Do not use any prior knowledge.
        
#         Answer:"""

#         response = await self.llm.ainvoke(prompt)
#         answer = response.content
        
#         print(f"Generated Answer:\n{answer}")
        
#         state['answer'] = answer
#         return state

# solver_node = SolverNode()















# import asyncio
# from app.agents.state import AgentState
# from app.agents.config import get_llm, default_agent_config


# class SolverNode:
#     """
#     A node that generates a final answer based on the retrieved context, including citations.
#     """
#     def __init__(self, config=None):
#         self.llm = get_llm(config or default_agent_config)

#     async def __call__(self, state: AgentState) -> AgentState:
#         print("--- ✍️ Solver Node ---")
        
#         # Extract text from chunks using the correct field name: 'text_snippet'
#         context_parts = []
#         for i, chunk in enumerate(state['context']):
#             content = ""
            
#             if isinstance(chunk, dict):
#                 # The field is 'text_snippet' from format_citations()
#                 content = (
#                     chunk.get('text_snippet') or 
#                     chunk.get('text') or 
#                     chunk.get('content') or 
#                     chunk.get('chunk_text') or
#                     chunk.get('page_content') or
#                     ''
#                 )
#             else:
#                 # Handle object attributes
#                 content = (
#                     getattr(chunk, 'text_snippet', None) or
#                     getattr(chunk, 'text', None) or
#                     getattr(chunk, 'content', None) or
#                     getattr(chunk, 'chunk_text', None) or
#                     getattr(chunk, 'page_content', None) or
#                     ''
#                 )
            
#             if content:
#                 context_parts.append(f"[{i+1}] {content}")
        
#         if not context_parts:
#             print("ERROR: No text content found in any chunks!")
#             state['answer'] = "I apologize, but I cannot find relevant information to answer your question based on the available context."
#             return state
        
#         context_str = "\n\n".join(context_parts)
        
#         prompt = f"""You are a world-class synthesis expert. Your task is to answer the user's query based *only* on the provided context.

# Here is the retrieved context:

# ---
# {context_str}
# ---

# User's Query: "{state['query']}"

# Your instructions:
# 1. Formulate a comprehensive answer to the user's query.
# 2. You MUST cite the context in your answer using the format [1], [2], etc.
# 3. If the context does not contain enough information to answer the query, state that clearly.
# 4. Do not include information outside the provided context.

# Provide your answer now:
# """

#         response = await self.llm.ainvoke(prompt)
#         answer = response.content
        
#         print(f"Generated Answer: {answer[:100]}...")
        
#         state['answer'] = answer
#         return state


# solver_node = SolverNode()














import asyncio
from app.agents.state import AgentState
from app.agents.config import get_llm, default_agent_config


class SolverNode:
    """
    A node that generates a final answer based on the retrieved context, including citations.
    """
    def __init__(self, config=None):
        self.llm = get_llm(config or default_agent_config)

    async def __call__(self, state: AgentState) -> AgentState:
        print("--- ✍️ Solver Node ---")
        
        # Extract text from chunks using 'text_snippet' field
        context_parts = []
        for i, chunk in enumerate(state['context']):
            content = ""
            
            if isinstance(chunk, dict):
                content = (
                    chunk.get('text_snippet') or 
                    chunk.get('text') or 
                    chunk.get('content') or 
                    ''
                )
            else:
                content = (
                    getattr(chunk, 'text_snippet', None) or
                    getattr(chunk, 'text', None) or
                    getattr(chunk, 'content', None) or
                    ''
                )
            
            if content:
                context_parts.append(f"[{i+1}] {content}")
        
        if not context_parts:
            print("❌ ERROR: No text content found in any chunks!")
            state['answer'] = "I apologize, but I cannot find relevant information to answer your question based on the available context."
            return state
        
        context_str = "\n\n".join(context_parts)
        
        # Print retrieved context prominently
        print("\n" + "="*80)
        print("📚 RETRIEVED CONTEXT (RAG Chunks sent to LLM):")
        print("="*80)
        print(context_str)
        print("="*80 + "\n")
        
        prompt = f"""You are a world-class synthesis expert. Your task is to answer the user's query based *only* on the provided context.

Here is the retrieved context:

---
{context_str}
---

User's Query: "{state['query']}"

Your instructions:
1. Formulate a comprehensive answer to the user's query.
2. You MUST cite the context in your answer using the format [1], [2], etc.
3. If the context does not contain enough information to answer the query, state that clearly.
4. Do not include information outside the provided context.

Provide your answer now:
"""

        response = await self.llm.ainvoke(prompt)
        answer = response.content
        
        # Print LLM's answer prominently
        print("\n" + "="*80)
        print("🤖 LLM GENERATED ANSWER:")
        print("="*80)
        print(answer)
        print("="*80 + "\n")
        
        state['answer'] = answer
        return state


solver_node = SolverNode()
