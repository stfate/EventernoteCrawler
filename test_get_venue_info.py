#!/usr/bin/env python

"""

"""

import json
import eventernote_crawler as crawler


if __name__ == "__main__":
    venue_id = 3
    out_fname = "../data/output/venue.json"
    output = crawler.get_venue_info(venue_id)
    json.dump( output, open(out_fname, "w"), ensure_ascii=False, indent=2 )
    