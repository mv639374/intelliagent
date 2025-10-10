import asyncio
import time
from app.rag.retrieval.vector_retriever import vector_retriever
from app.rag.retrieval.keyword_retriever import keyword_retriever
from app.rag.retrieval.hybrid_retriever import hybrid_retriever

async def run_all_retrievers(query: str):
    print(f"\n{'='*20}\nQuery: '{query}'\n{'='*20}")

    # --- Vector Search ---
    start = time.time()
    vector_res = await vector_retriever.retrieve(query, top_k=3)
    print(f"--- Vector Search ({(time.time() - start)*1000:.2f} ms) ---")
    for r in vector_res:
        print(f"Score: {r['score']:.4f}, Text: {r['text'][:80]}...")

    # --- Keyword Search ---
    start = time.time()
    keyword_res = await keyword_retriever.retrieve(query, top_k=3)
    print(f"\n--- Keyword Search ({(time.time() - start)*1000:.2f} ms) ---")
    for r in keyword_res:
        print(f"Score: {r['score']:.4f}, Text: {r['text'][:80]}...")

    # --- Hybrid Search ---
    start = time.time()
    hybrid_res = await hybrid_retriever.retrieve(query, top_k=3, rerank=True)
    print(f"\n--- Hybrid (RRF + Rerank) ({(time.time() - start)*1000:.2f} ms) ---")
    for r in hybrid_res:
        print(f"Score: {r['score']:.4f}, Text: {r['text'][:80]}...")

async def main():
    # Query for a specific term that keyword search will excel at
    await run_all_retrievers("LangGraph")

    # Query for a broad concept that vector search will excel at
    await run_all_retrievers("challenges in knowledge management")

if __name__ == "__main__":
    asyncio.run(main())