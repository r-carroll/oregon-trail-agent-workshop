import os

from redisvl.extensions.router import Route, SemanticRouter
from redisvl.utils.vectorize import HFTextVectorizer
from dotenv import load_dotenv
load_dotenv()

REDIS_URL = os.environ.get("REDIS_URL", "redis://host.docker.internal:6379/0")

# Semantic router
blocked_references = [
    "thinks about aliens",
    "corporate questions about agile",
    "anything about the S&P 500",
]

# TODO: implement route to blocked traffic
blocked_route = Route(name='block_list', references=blocked_references)

# TODO: implement allow/block router
router = SemanticRouter(
  name='blocker',
  routes=[blocked_route],
  redis_url=REDIS_URL,
  overwrite=False
)
