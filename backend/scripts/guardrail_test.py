import asyncio
from app.rag.retrieval.hybrid_retriever import hybrid_retriever

async def main():
    # Test Case 1: PII Masking
    print("\n--- 1. Testing PII Masking ---")
    pii_query = "What is Evelyn Reed's email address?"
    results_masked = await hybrid_retriever.retrieve(pii_query, top_k=1, apply_pii_mask=True)
    if results_masked:
        print("Masked Result:", results_masked[0]['text_snippet'])

    results_unmasked = await hybrid_retriever.retrieve(pii_query, top_k=1, apply_pii_mask=False)
    if results_unmasked:
        print("Unmasked Result:", results_unmasked[0]['text_snippet'])


    # Test Case 2: Low-confidence filtering
    print("\n--- 2. Testing Low-Confidence Filter ---")
    low_quality_query = "asdfghjkl" # Gibberish query
    results_low_quality = await hybrid_retriever.retrieve(low_quality_query)
    print(f"Results for gibberish query: {len(results_low_quality)}")


    # Test Case 3: Citation Formatting
    print("\n--- 3. Testing Citation Formatting ---")
    citation_query = "What is LangGraph?"
    results_citation = await hybrid_retriever.retrieve(citation_query, top_k=2)
    print("Formatted Citations:")
    for res in results_citation:
        print(res)


if __name__ == "__main__":
    # First, upload pii_sample.pdf and project_details.pdf
    asyncio.run(main())