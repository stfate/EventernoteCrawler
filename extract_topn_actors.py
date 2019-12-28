#!/usr/bin/env python

"""

"""

import json
import numpy as np


if __name__ == "__main__":
    actors_dict = json.load( open("../list/actors.json", "r") )
    user_cnts = np.array([_actor["user_cnt"] for _actor in actors_dict["actors"] ])
    n_actors = len(actors_dict["actors"])
    print(n_actors)
    nbest = 200
    if nbest > n_actors:
        nbest = n_actors
        
    sort_idxs = np.flip( np.argsort(user_cnts), 0 )[:nbest]
    
    topn_actors_dict = {"actors": []}
    for _idx in sort_idxs:
        topn_actors_dict["actors"].append(actors_dict["actors"][_idx])

    json.dump( topn_actors_dict, open( "../list/actors_top{}.json".format(nbest), "w" ), ensure_ascii=False, indent=2 )
    