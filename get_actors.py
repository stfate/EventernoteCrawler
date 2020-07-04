#!/usr/bin/env python

"""

"""

import json
import eventernote_crawler as crawler


if __name__ == "__main__":
    out_fname = "./list/actors.json"
    min_user_cnt = 50
    output = crawler.get_actors(min_user_cnt=min_user_cnt)
    json.dump( output, open(out_fname, "w", encoding="utf-8"), ensure_ascii=False, indent=2 )