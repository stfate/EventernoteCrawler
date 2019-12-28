#!/usr/bin/env python

"""

"""

import json
import eventernote_crawler as crawler


if __name__ == "__main__":
    actor_id = 6582
    out_fname = "../data/actor_events.json"
    output = crawler.get_actor_events(actor_id)
    json.dump( output, open(out_fname, "w", encoding="utf-8"), ensure_ascii=False, indent=2 )