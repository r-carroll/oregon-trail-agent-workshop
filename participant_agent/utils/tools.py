import os

from dotenv import load_dotenv
from langchain.tools.retriever import create_retriever_tool
from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_redis import RedisVectorStore
from pydantic import BaseModel, Field

from .vector_store import get_vector_store

load_dotenv()

REDIS_URL = os.environ.get("REDIS_URL", "redis://host.docker.internal:6379/0")


@tool
def multiply(a: int, b: int) -> int:
    """multiply two numbers."""
    return a * b


# TODO: define restock pydantic model for structure input
class RestockInput(BaseModel):
    daily_usage: int = Field()
    lead_time: int = Field()
    safety_stock: int = Field()
    pass


# TODO: modify to accept correct inputs and have meaningful docstring
@tool("restock-tool", args_schema=RestockInput)
def restock_tool(daily_usage, lead_time, safety_stock) -> int:
    # this docstring is super important so that the llm knows how to use this tool
    """restock formula tool used specifically for calculating the amount of food at which you should start restocking."""
    print(f"\n Using restock tool!")
    return (daily_usage * lead_time) + safety_stock


# TODO: implement the retriever tool
# update get_vector_store function
vector_store = get_vector_store()
# update tool with appropriate information so the agent knows how to invoke
retriever_doc = "When asked about which direction to take, searches maps and routes to find the best path."
retriever_tool = create_retriever_tool(vector_store.as_retriever(), 
                                       "get_directions",
                                       retriever_doc)

tools = [retriever_tool, restock_tool]
