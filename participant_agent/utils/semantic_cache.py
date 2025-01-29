import os

from dotenv import load_dotenv
from redisvl.extensions.llmcache import SemanticCache

load_dotenv()

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

# Semantic cache
hunting_example = "There's a deer. You're starving. You know what you have to do..."

# TODO: implement semantic cache
semantic_cache = SemanticCache(
    name="oregon_trail_cache",
    redis_url=REDIS_URL,
    distance_threshold=0.1,
)

# TODO store appropriate values in cache
semantic_cache.store(prompt=hunting_example, response="bang")
