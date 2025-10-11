from app.agents.state import AgentState

class ToolNode:
    """
    A node that executes tool calls identified by the LLM.
    """
    async def __call__(self, state: AgentState) -> AgentState:
        print("--- 🛠️ Tool Node ---")
        
        tool_calls = state.get('tool_calls', [])
        
        if not tool_calls:
            print("No tool calls to execute.")
            return state

        results = []
        for tool_call in tool_calls:
            # In a real app, you would have a tool registry to dispatch these calls.
            # For this checkpoint, we'll use a mock result.
            tool_name = tool_call.get("type")
            tool_args = tool_call.get("args", {})
            
            print(f"Executing tool '{tool_name}' with args: {tool_args}")
            
            mock_result = f"Mock result for tool '{tool_name}' with arguments {tool_args}."
            
            # Format the result like a context chunk
            results.append({
                "text": mock_result,
                "metadata": {"source": "tool", "tool_name": tool_name}
            })
            
        # Append the tool results to the existing context
        state['context'].extend(results)
        return state

tool_node = ToolNode()