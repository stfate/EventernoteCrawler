#!/usr/bin/env python

"""

"""

import json
import eventernote_crawler as crawler


if __name__ == "__main__":
    actor_id = 2890
    output_fn = "./data/actor_users.json"

    output = crawler.get_actor_users(actor_id)
    json.dump(output, open(output_fn, "w"), ensure_ascii=False, indent=2)