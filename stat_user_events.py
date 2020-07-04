#!/usr/bin/env python

"""

"""

import json


def count_actors(events):
    actors_count_dict = {}
    for ev in events:
        for actor in ev["actors"]:
            if actor in actors_count_dict:
                actors_count_dict[actor] += 1
            else:
                actors_count_dict[actor] = 1

    return actors_count_dict


if __name__ == "__main__":
    event_dict = json.load(open("./data/user_event_list_2017.json", "r", encoding="utf-8"))

    events = event_dict["events"]

    actors_count_dict = count_actors(events)
    sorted_actors_count = sorted(actors_count_dict.items(), key=lambda x:x[1], reverse=True)
    reina_factor = actors_count_dict["上田麗奈"] / len(events)
    
    with open("2017.txt", "w", encoding="utf-8") as fo:
        fo.write(f"#events={len(events)}\n")
        fo.write("\n")

        fo.write("top actors=\n")
        for _actor in sorted_actors_count[:10]:
            fo.write(f"{_actor[0]}\t{_actor[1]}\n")
        fo.write("\n")

        fo.write(f"ReinaFactor={reina_factor:.06f}")
