#!/usr/bin/env python

"""

"""

import argparse
import json
import eventernote_crawler as crawler


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", type=str, required=True, help="user id")
    parser.add_argument("-o", "--out", type=str, required=True, help="path to output json")
    parser.add_argument("-y", "--year", type=str, default="", help="year(yyyy)")
    parser.add_argument("-m", "--month", type=str, default="", help="month(mm)")
    parser.add_argument("-d", "--day", type=str, default="", help="day(dd)")
    args = parser.parse_args()

    user_id = args.user
    output_fn = args.out
    year = args.year
    month = args.month
    day = args.day

    output = crawler.get_user_events(user_id, year=year, month=month, day=day)
    json.dump(output, open(output_fn, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
