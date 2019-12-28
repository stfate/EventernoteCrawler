#!/usr/bin/env python

"""

"""

import json
import eventernote_crawler as crawler


if __name__ == "__main__":
    actor_id = 2890
    out_fname = "../data/output/actor_user_ranking.json"
    output = crawler.get_actor_user_ranking(actor_id)
    json.dump( output, open(out_fname, "w"), ensure_ascii=False, indent=2 )
