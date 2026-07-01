import random


def generate_scores() -> dict[str, int]:
    return {
        "believability": random.randint(60, 95),
        "drama": random.randint(10, 80),
        "risk": random.randint(5, 50),
    }
