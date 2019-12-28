#!/usr/bin/env python

"""

"""

import json
import eventernote_crawler as crawler


if __name__ == "__main__":
    user_id = "stfate"
    output_fn = "./data/user_event_list_2019.json"
    output = crawler.get_user_events(user_id, year="2019")
    json.dump(output, open(output_fn, "w", encoding="utf-8"), ensure_ascii=False, indent=2)