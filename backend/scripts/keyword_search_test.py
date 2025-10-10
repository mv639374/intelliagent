import asyncio
import time

from app.db.elasticsearch_client import es_client
from app.rag.retrieval.keyword_retriever import keyword_retriever


async def run_search_test():
    # First, show what documents exist
    print("=== Documents in Index ===")
    try:
        all_docs = es_client.client.search(index=es_client.index_name, query={"match_all": {}}, size=10)
        print(f"Total documents: {all_docs['hits']['total']['value']}")
        for hit in all_docs["hits"]["hits"]:
            print(f"\nDoc ID: {hit['_id']}")
            print(f"Text preview: {hit['_source']['text'][:200]}...")
    except Exception as e:
        print(f"Error fetching documents: {e}")

    print("\n" + "=" * 50 + "\n")

    query = input("Enter keyword search query (e.g., 'London', 'email', 'doctor'): ")
    if not query:
        return

    start_time = time.time()
    results = await keyword_retriever.retrieve(query)
    end_time = time.time()

    duration_ms = (end_time - start_time) * 1000
    print(f"\nSearch completed in {duration_ms:.2f} ms.")
    print(f"Found {len(results)} results\n")

    print("--- Top Search Results ---")
    for result in results:
        print(f"Score: {result['score']:.4f}, Chunk ID: {result['chunk_id']}")
        print(f"Text: {result['text'][:250]}...")
        print("-" * 20)


if __name__ == "__main__":
    asyncio.run(run_search_test())
