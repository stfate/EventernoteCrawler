#!/usr/bin/env python

"""

"""

import json
import os
from tqdm import tqdm
import time
import numpy as np
import eventernote_crawler as crawler


if __name__ == "__main__":
    actors_dict_fname = "../list/actors_top774.json"
    actors_dict = json.load( open(actors_dict_fname, "r") )
    out_dir = "../data/downloads"

    for actor in tqdm(actors_dict["actors"]):
        actor_id = actor["actor_id"]
        events_dict = crawler.get_actor_events(actor_id)
        dst_dir = os.path.join(out_dir, str(actor_id) )
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        
        out_fname = os.path.join(dst_dir, "events.json")
        json.dump( events_dict, open(out_fname, "w"), ensure_ascii=False, indent=2 )

        time.sleep( 2.0 + np.random.normal(0.0, 0.33) )
