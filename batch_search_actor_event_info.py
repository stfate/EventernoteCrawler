#!/usr/bin/env python

"""

"""

import os
import json
import time
from tqdm import tqdm
import numpy as np
import eventernote_crawler as crawler


if __name__ == "__main__":
    actors_json_fname = "../list/actors_top200.json"
    out_root = "../data/downloads"
    actors_dict = json.load( open(actors_json_fname, "r") )
    for actor in tqdm(actors_dict["actors"]):
        actor_id = actor["actor_id"]
        out_actor_dir = os.path.join( out_root, str(actor_id) )
        events_json_fname = os.path.join(out_actor_dir, "events.json")
        events_dict = json.load( open(events_json_fname, "r") )
        for event in events_dict["events"]:
            event_id = event["event_id"]
            event_info_dict = crawler.get_event_info(event_id)
            out_event_dir = os.path.join(out_actor_dir, "event_info")
            if not os.path.exists(out_event_dir):
                os.mkdir(out_event_dir)
            out_fname = os.path.join( out_event_dir, "{}.json".format(event_id) )
            json.dump( event_info_dict, open(out_fname, "w"), ensure_ascii=False, indent=2 )
            time.sleep( 2.0 + np.random.normal(0.0, 0.33) )
