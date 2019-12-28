#!/usr/bin/env python

"""

"""

import json
import eventernote_crawler as crawler


if __name__ == "__main__":
    event_id = 55476
    out_fname = "../data/output/event_info.json"
    output = crawler.get_event_info(event_id)
    json.dump( output, open(out_fname, "w"), ensure_ascii=False, indent=2 )