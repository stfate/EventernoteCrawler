"""
APIs of EventernoteCrawler
"""

import subprocess
import os
import json

CRAWLER_DIR = os.path.dirname( os.path.abspath(__file__) )


def get_actor_events(actor_id):
    """ 演者ごとのイベントリスト取得
    @param actor_id actor id [int]
    @return events [dict]
    """
    cur_dir = os.getcwd()
    os.chdir(CRAWLER_DIR)

    cmd = [
        "scrapy", "crawl", "eventernote-actor-events",
        "-a", "actor_id={}".format(actor_id),
        "-t", "json",
        "-o", "-"
    ]
    output_str = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")
    output_dict = json.loads(output_str)[0]

    os.chdir(cur_dir)

    return output_dict


def get_actor_users(actor_id):
    """ 演者をお気に入り登録しているユーザーの取得
    @param actor_id actor id [int]
    @return users list [dict]
    """
    cur_dir = os.getcwd()
    os.chdir(CRAWLER_DIR)

    cmd = [
        "scrapy", "crawl", "eventernote-actor-users",
        "-a", "actor_id={}".format(actor_id),
        "-t", "json",
        "-o", "-"
    ]
    output_str = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")
    output_dict = json.loads(output_str)[0]

    os.chdir(cur_dir)

    return output_dict


def get_actor_user_ranking(actor_id):
    """ 演者のユーザランキングを取得
    @param actor_id actor id [int]
    @return users list [dict]
    """
    cur_dir = os.getcwd()
    os.chdir(CRAWLER_DIR)

    cmd = [
        "scrapy", "crawl", "eventernote-actor-user-ranking",
        "-a", "actor_id={}".format(actor_id),
        "-t", "json",
        "-o", "-"
    ]
    output_str = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")
    output_dict = json.loads(output_str)[0]

    os.chdir(cur_dir)

    return output_dict


def get_actors(min_user_cnt=10):
    """ 登録ユーザ数が一定値以上の演者のリストを取得
    @param min_user_cnt minimum of user count [int]
    @return actors list [dict]
    """
    cur_dir = os.getcwd()
    os.chdir(CRAWLER_DIR)

    cmd = [
        "scrapy", "crawl", "eventernote-actors",
        "-a", "min_user_cnt={}".format(min_user_cnt),
        "-t", "json",
        "-o", "-"
    ]
    actors_str = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")
    actors = json.loads(actors_str)
    sorted_actors = sorted(actors, key=lambda actor:actor["actor_id"])
    output_dict = {"actors": sorted_actors}

    os.chdir(cur_dir)

    return output_dict


def get_actors_ranking():
    """ 演者のランキング(Top100)を取得
    @param none
    @return actors ranking [dict]
    """
    cur_dir = os.getcwd()
    os.chdir(CRAWLER_DIR)

    cmd = [
        "scrapy", "crawl", "eventernote-actors-ranking",
        "-t", "json",
        "-o", "-"
    ]
    output_str = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")
    actor_ranking = json.loads(output_str)
    output_dict = {"actor_ranking": actor_ranking}

    os.chdir(cur_dir)

    return output_dict


def get_event_info(event_id):
    """ イベント詳細情報の取得
    @param event_id event id [int]
    @return event metadata [dict]
    """
    cur_dir = os.getcwd()
    os.chdir(CRAWLER_DIR)

    cmd = [
        "scrapy", "crawl", "eventernote-event-info",
        "-a", "event_id={}".format(event_id),
        "-t", "json",
        "-o", "-"
    ]
    output_str = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")
    output_dict = json.loads(output_str)[0]

    os.chdir(cur_dir)

    return output_dict


def get_event_participants(event_id):
    """ イベントの参加者一覧を取得
    @param event_id event id [int]
    @return participants of the event [dict]
    """
    cur_dir = os.getcwd()
    os.chdir(CRAWLER_DIR)

    cmd = [
        "scrapy", "crawl", "eventernote-event-participants",
        "-a", "event_id={}".format(event_id),
        "-t", "json",
        "-o", "-"
    ]
    output_str = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")
    output_dict = json.loads(output_str)[0]

    os.chdir(cur_dir)

    return output_dict


def get_user_info(user_id):
    """ ユーザーの詳細情報を取得
    @param user_id user id [string]
    @return user metadata [dict]
    """
    cur_dir = os.getcwd()
    os.chdir(CRAWLER_DIR)

    cmd = [
        "scrapy", "crawl", "eventernote-user-info",
        "-a", "user_id={}".format(user_id),
        "-t", "json",
        "-o", "-"
    ]
    output_str = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")
    output_dict = json.loads(output_str)[0]

    os.chdir(cur_dir)

    return output_dict


def get_user_events(user_id, year="", month="", day=""):
    """ ユーザーの参加イベントを取得 (年/月/日で絞り込み可能)
    @param user_id user id [string]
    @param year year [string]
    @param month month [string]
    @param day day [string]
    @return user-events metadata [dict]
    """
    cur_dir = os.getcwd()
    os.chdir(CRAWLER_DIR)

    cmd = [
        "scrapy", "crawl", "eventernote-user-event-pages",
        "-a", f"user_id={user_id}", "-a", f"year={year}", "-a", f"month={month}", "-a", f"day={day}",
        "-t", "json",
        "-o", "-"
    ]
    urls_str = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")
    urls_dict = json.loads(urls_str)[0]
    num_pages = urls_dict["num_pages"]

    cmd = [
        "scrapy", "crawl", "eventernote-user-event-list",
        "-a", f"user_id={user_id}", "-a", f"year={year}", "-a", f"month={month}", "-a", f"day={day}", "-a", f"num_pages={num_pages}",
        "-t", "json",
        "-o", "-"
    ]
    output_str = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")
    _output_dict = json.loads(output_str)

    output_dict = _output_dict[0]
    for i in range(1, len(_output_dict)):
        output_dict["events"].extend(_output_dict[i]["events"])

    os.chdir(cur_dir)

    return output_dict


def get_venue_info(venue_id):
    """ 会場の詳細情報を取得
    @param venue_id venue id [int]
    @return venue metadata [dict]
    """
    cur_dir = os.getcwd()
    os.chdir(CRAWLER_DIR)

    cmd = [
        "scrapy", "crawl", "eventernote-venue-info",
        "-a", "venue_id={}".format(venue_id),
        "-t", "json",
        "-o", "-"
    ]
    output_str = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")
    output_dict = json.loads(output_str)[0]

    os.chdir(cur_dir)

    return output_dict
