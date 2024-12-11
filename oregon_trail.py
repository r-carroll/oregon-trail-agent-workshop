import json
import time

from dotenv import load_dotenv
from final_example import ExampleAgent
from game_play import GamePlayInterface
from langchain_core.messages import HumanMessage

load_dotenv()


def format_question(q):
    question = q["question"]
    options = q.get("options", "")
    if options:
        formatted = f"{question}, options: {' '.join(options)}"
    else:
        formatted = question
    return [HumanMessage(content=formatted)]


def run_game(player_agent: GamePlayInterface):
    with open("questions.json") as f:
        questions = json.load(f)

    router = player_agent.get_router()
    cache = player_agent.get_semantic_cache()

    for q in questions:
        start = time.time()

        print(f"Question: {q['question']}")

        if options := q.get("options"):
            print(f"Options: {options}")

        cache_hit = cache.check(prompt=q["question"], return_fields=["response"])

        if cache_hit:
            end = time.time() - start
            print(f"Cache hit! {q['answer']}")
            assert cache_hit[-1]["response"] == q["answer"]
            assert end < 1
            continue

        blocked_topic_match = router(q["question"], distance_threshold=0.2)

        if blocked_topic_match.name == "block_list":
            print(f"Get behind me Satan! Blocked topic: {q['question']}")
            continue

        res = player_agent.get_graph().invoke({"messages": format_question(q)})

        if q["type"] == "action":
            end = time.time() - start
            if end > 1:
                print(f"Too slow!! took: {end}s")
                raise AssertionError(f"Too slow!! took: {end}s")

        print(f"Agent answer: {res['messages'][-1].content}")
        if res["messages"][-1].content != q["answer"]:
            print(f"Expected: {q['answer']}, got: {res['messages'][-1].content}")
            raise AssertionError("\n You have failed the Oregon Trail ¯\_(ツ)_/¯ \n ")

    print("You made it to Oregon! 🎉")


if __name__ == "__main__":
    run_game(ExampleAgent())
