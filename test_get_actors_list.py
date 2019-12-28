#!/usr/bin/env python

"""

"""

import json
import eventernote_crawler as crawler


if __name__ == "__main__":
    min_user_cnt = 50
    out_fname = "../data/output/actors_list.json"

    output = crawler.get_actors_list(min_user_cnt)
    json.dump( output, open(out_fname, "w"), ensure_ascii=False, indent=2 )