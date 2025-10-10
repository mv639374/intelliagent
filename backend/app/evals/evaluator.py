# import asyncio
# import json
# from typing import List, Dict, Any
# from pathlib import Path
# from app.rag.retrieval.hybrid_retriever import hybrid_retriever
# from app.evals.metrics import precision_at_k, recall_at_k
# from app.db.sync_session import get_sync_db
# from app.models.evaluation import EvaluationRun
# from app.evals.langsmith_integration import log_eval_to_langsmith


# class RagEvaluator:
#     def __init__(self, dataset_path: Path):
#         self.dataset_path = dataset_path  # ADDED: Store dataset_path
#         self.dataset = self.load_dataset(dataset_path)

#     def load_dataset(self, dataset_path: Path) -> List[Dict[str, Any]]:
#         with open(dataset_path, 'r') as f:
#             return [json.loads(line) for line in f]

#     async def run_evaluation(self) -> Dict[str, float]:
#         retrieved_doc_ids = []
#         expected_doc_ids = []

#         for item in self.dataset:
#             query = item["query"]
#             expected = set(item["expected_docs"])

#             # Run the retriever
#             results = await hybrid_retriever.retrieve(query, top_k=10, rerank=True)
#             retrieved = [citation["document_id"] for citation in results]

#             retrieved_doc_ids.append(retrieved)
#             expected_doc_ids.append(expected)

#         # Calculate metrics
#         p_at_5 = sum([precision_at_k(r, e, 5) for r, e in zip(retrieved_doc_ids, expected_doc_ids)]) / len(self.dataset)
#         r_at_10 = sum([recall_at_k(r, e, 10) for r, e in zip(retrieved_doc_ids, expected_doc_ids)]) / len(self.dataset)

#         metrics = {
#             "precision_at_5": round(p_at_5, 4),
#             "recall_at_10": round(r_at_10, 4),
#             "dataset_size": len(self.dataset)
#         }

#         self.save_results(metrics)
#         log_eval_to_langsmith(self.dataset_path.name, metrics)  # FIXED: Use self.dataset_path
#         return metrics

#     def save_results(self, metrics: Dict[str, float]):
#         with get_sync_db() as db:
#             eval_run = EvaluationRun(
#                 dataset_name=self.dataset_path.name,  # FIXED: Use self.dataset_path.name
#                 metrics=metrics
#             )
#             db.add(eval_run)
#             db.commit()
#             print("Saved evaluation results to the database.")


# async def main_async(dataset_path):
#     evaluator = RagEvaluator(dataset_path)
#     return await evaluator.run_evaluation()



import json
from typing import List, Dict, Any
from pathlib import Path
from fastapi.testclient import TestClient

from app.evals.metrics import precision_at_k, recall_at_k
from app.db.sync_session import get_sync_db
from app.models.evaluation import EvaluationRun
from app.evals.langsmith_integration import log_eval_to_langsmith

class RagEvaluator:
    def __init__(self, dataset_path: Path, client: TestClient, headers: dict, project_id: str):
        self.dataset = self.load_dataset(dataset_path)
        self.client = client
        self.headers = headers
        self.project_id = project_id
        self.dataset_name = dataset_path.name

    def load_dataset(self, dataset_path: Path) -> List[Dict[str, Any]]:
        if not dataset_path.exists():
            return []
        with open(dataset_path, 'r') as f:
            return [json.loads(line) for line in f]

    def run_evaluation(self) -> Dict[str, float]:
        if not self.dataset:
            raise ValueError("Dataset is empty or could not be loaded.")

        retrieved_doc_ids = []
        expected_doc_ids = []

        for item in self.dataset:
            query = item["query"]
            expected = set(item["expected_docs"])

            # --- FIX: Make an API call instead of direct import ---
            response = self.client.post(
                "/api/v1/chat/ask",
                headers=self.headers,
                json={"query": query, "project_id": self.project_id, "top_k": 10},
            )
            response.raise_for_status()
            results = response.json()["citations"]
            # --- END FIX ---

            retrieved = [citation["document_id"] for citation in results]
            retrieved_doc_ids.append(retrieved)
            expected_doc_ids.append(expected)

        p_at_5 = sum([precision_at_k(r, e, 5) for r, e in zip(retrieved_doc_ids, expected_doc_ids)]) / len(self.dataset)
        r_at_10 = sum([recall_at_k(r, e, 10) for r, e in zip(retrieved_doc_ids, expected_doc_ids)]) / len(self.dataset)

        metrics = {
            "precision_at_5": round(p_at_5, 4),
            "recall_at_10": round(r_at_10, 4),
            "dataset_size": len(self.dataset)
        }
        
        self.save_results(metrics)
        log_eval_to_langsmith(self.dataset_name, metrics)
        
        return metrics

    def save_results(self, metrics: Dict[str, float]):
        with get_sync_db() as db:
            eval_run = EvaluationRun(dataset_name=self.dataset_name, metrics=metrics)
            db.add(eval_run)
            db.commit()
        print("Saved evaluation results to the database.")