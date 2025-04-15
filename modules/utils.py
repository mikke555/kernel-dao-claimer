import random
import time
from datetime import datetime

from tqdm import tqdm

import settings
from models.account import Account


def read_file(path: str, prefix: str = "") -> list[str]:
    with open(path) as f:
        return [prefix + line.strip() for line in f if line.strip()]


def get_accounts() -> list[Account]:
    keys = read_file("keys.txt")
    proxies = read_file("proxies.txt", prefix="http://")

    pairs = [(key, proxies[i % len(proxies)] if settings.USE_PROXY else None) for i, key in enumerate(keys)]

    if settings.SHUFFLE_KEYS:
        random.shuffle(pairs)

    accounts = [
        Account(id=f"[{index}/{len(keys)}]", private_key=key, proxy=proxy)
        for index, (key, proxy) in enumerate(pairs, start=1)
    ]

    return accounts


def random_sleep(max_time: int, min_time: int = 1) -> None:
    if min_time > max_time:
        min_time, max_time = max_time, min_time

    x = random.randint(min_time, max_time)
    time.sleep(x)


def sleep(from_sleep: int, to_sleep: int) -> None:
    x = random.randint(from_sleep, to_sleep)
    desc = datetime.now().strftime("%H:%M:%S")

    for _ in tqdm(range(x), desc=desc, bar_format="{desc} | Sleeping {n_fmt}/{total_fmt}"):
        time.sleep(1)
    print()
