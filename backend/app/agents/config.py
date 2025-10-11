from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from typing import Literal, Union
from dotenv import load_dotenv
load_dotenv()

LLMProvider = Literal["groq", "google_genai", "openai"]

class AgentConfig(BaseModel):
    llm_provider: LLMProvider = "groq"
    model_name: str = "llama-3.3-70b-versatile"
    temperature: float = 0.1
    max_iterations: int = 15
    
    class Config:
        frozen = True

def get_llm(config: AgentConfig) -> Union[ChatGroq, ChatGoogleGenerativeAI, ChatOpenAI]:
    """Factory function to get a LangChain chat model instance based on config."""
    if config.llm_provider == "groq":
        return ChatGroq(temperature=config.temperature, model_name=config.model_name)
    elif config.llm_provider == "google_genai":
        return ChatGoogleGenerativeAI(temperature=config.temperature, model=config.model_name)
    elif config.llm_provider == "openai":
        return ChatOpenAI(temperature=config.temperature, model_name=config.model_name)
    else:
        raise ValueError(f"Unsupported LLM provider: {config.llm_provider}")

# Default configuration instance
default_agent_config = AgentConfig(llm_provider="groq", model_name="llama-3.3-70b-versatile")