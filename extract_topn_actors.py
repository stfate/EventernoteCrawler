#!/usr/bin/env python

"""

"""

import json
import numpy as np


if __name__ == "__main__":
    actors_dict = json.load( open("./list/actors.json", "r", encoding="utf-8") )
    user_cnts = np.array([_actor["user_cnt"] for _actor in actors_dict["actors"] ])
    n_actors = len(actors_dict["actors"])
    nbest = 1000
    if nbest > n_actors:
        nbest = n_actors
        
    sort_idxs = np.flip( np.argsort(user_cnts), 0 )[:nbest]
    
    topn_actors_dict = {"actors": []}
    for _idx in sort_idxs:
        topn_actors_dict["actors"].append(actors_dict["actors"][_idx])

    json.dump( topn_actors_dict, open(f"./list/actors_top{nbest}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    