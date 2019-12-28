#!/usr/bin/env python

"""

"""

import json
import eventernote_crawler as crawler


if __name__ == "__main__":
    event_id = 152482
    out_fname = "../data/output/participants.json"

    output = crawler.get_event_participants(event_id)
    json.dump( output, open(out_fname, "w"), ensure_ascii=False, indent=2 )
    