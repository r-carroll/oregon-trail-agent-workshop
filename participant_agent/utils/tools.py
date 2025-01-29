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

class RestockInput(BaseModel):
    daily_usage: int = Field(
        description="Pounds (lbs) of food expected to be consumed daily"
    )
    lead_time: int = Field(description="Lead time to replace food in days")
    safety_stock: int = Field(
        description="Number of pounds (lbs) of safety stock to keep on hand"
    )


@tool("restock-tool", args_schema=RestockInput)
def restock_tool(daily_usage: int, lead_time: int, safety_stock: int) -> int:
    """restock formula tool used specifically for calculating the amount of food at which you should start restocking."""
    print(f"\n Using restock tool!: {daily_usage=}, {lead_time=}, {safety_stock=} \n")
    return (daily_usage * lead_time) + safety_stock


## retriever tool
# see .vector_store for implementation logic
vector_store = get_vector_store()

retriever_tool = create_retriever_tool(
    vector_store.as_retriever(),
    "get_directions",
    "Search and return information related to which routes/paths/trails to take along your journey.",
)

tools = [retriever_tool, restock_tool]
