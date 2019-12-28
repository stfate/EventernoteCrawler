#!/usr/bin/env python

"""

"""

import json
import eventernote_crawler as crawler


if __name__ == "__main__":
    user_id = "stfate"
    out_fname = "../data/user.json"
    output = crawler.get_user_info(user_id)
    json.dump( output, open(out_fname, "w", encoding="utf-8"), ensure_ascii=False, indent=2 )