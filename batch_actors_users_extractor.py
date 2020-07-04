#!/usr/bin/env python

"""

"""

import json
from pathlib import Path
from tqdm import tqdm

import eventernote_crawler as crawler


if __name__ == "__main__":
    actors_list_fn = "./list/actors_top1000.json"
    output_root = Path("./data/actor_users")
    actors_list = json.load(open(actors_list_fn))["actors"]

    for actors in tqdm(actors_list):
        actor_id = actors["actor_id"]
        actor_users = crawler.get_actor_users(actor_id)
        output_fn = output_root / f"{actor_id}.json"
        json.dump(actor_users, open(output_fn, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        