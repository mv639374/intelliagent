from app.agents.state import AgentState
from app.rag.retrieval.hybrid_retriever import hybrid_retriever

class RetrieverNode:
    """
    A node that retrieves context from the knowledge base using hybrid search.
    """
    async def __call__(self, state: AgentState) -> AgentState:
        print("--- 📚 Retriever Node ---")
        
        query = state['query']
        
        # Retrieve context without reranking for now, as the Solver will synthesize it.
        # We also disable PII masking at this stage.
        retrieved_chunks = await hybrid_retriever.retrieve(
            query, 
            top_k=10, 
            rerank=False, 
            apply_pii_mask=False
        )
        
        print(f"Retrieved {len(retrieved_chunks)} chunks.")
        
        state['context'] = retrieved_chunks
        return state

retriever_node = RetrieverNode()