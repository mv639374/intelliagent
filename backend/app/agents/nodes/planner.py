import asyncio
from app.agents.state import AgentState
from app.agents.config import get_llm, default_agent_config

class PlannerNode:
    """
    A node that creates a plan to answer the user's query.
    """
    def __init__(self, config=None):
        self.llm = get_llm(config or default_agent_config)

    async def __call__(self, state: AgentState) -> AgentState:
        print("--- 🧠 Planner Node ---")
        
        prompt = f"""You are a master planner. Your job is to create a step-by-step plan to answer a complex user query.
        
        Query: "{state['query']}"
        
        Based on the query, create a concise, step-by-step plan. The plan should involve fetching information, analyzing it, and then formulating a final answer.
        
        Example Plan:
        1. Retrieve relevant documents about the core topics in the query.
        2. Identify key entities and concepts from the retrieved context.
        3. Synthesize the information to construct a comprehensive answer.
        
        Your Plan:"""
        
        response = await self.llm.ainvoke(prompt)
        plan = response.content
        
        print(f"Generated Plan:\n{plan}")
        
        state['plan'] = plan
        return state

planner_node = PlannerNode()