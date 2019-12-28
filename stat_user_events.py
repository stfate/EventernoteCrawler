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
    event_dict = json.load(open("./data/user_event_list_2019.json", "r", encoding="utf-8"))

    events = event_dict["events"]
    print(len(events))

    actors_count_dict = count_actors(events)
    print(actors_count_dict)

    sorted_actors_count = sorted(actors_count_dict.items(), key=lambda x:x[1], reverse=True)
    for _actor in sorted_actors_count:
        print(_actor)

    reina_factor = actors_count_dict["上田麗奈"] / len(events)
    print("reina_factor=", reina_factor)