#!/usr/bin/env python

"""

"""

import json
import eventernote_crawler as crawler


if __name__ == "__main__":
    out_fname = "../data/output/actors_ranking.json"
    output = crawler.get_actors_ranking()
    json.dump( output, open(out_fname, "w"), ensure_ascii=False, indent=2 )