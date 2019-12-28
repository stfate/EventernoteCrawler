"""
Spiders for crawling Eventernote
"""

import json
import os
import re
import time
import scrapy

ROOT_URL = "https://www.eventernote.com"


class EventernoteActorEventsSpider(scrapy.Spider):
    """
    @class EventernoteActorEventsSpider
    @brief a class for searching events of a specified actor

    input:
        actor_id actor id
    generates:
        {
            "actor_id": ,
            "events": [
                {
                    "event_id": ,
                    "event_name": 
                }
            ]
        }
    """
    name = "eventernote-actor-events"
    MAX_LIMIT = 10000000

    def start_requests(self):
        self.actor_id = int( getattr(self, "actor_id", None) )

        urls = [
            f"{ROOT_URL}/actors/{self.actor_id}/events?actor_id={self.actor_id}&limit={self.MAX_LIMIT}"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        div_events = response.css("div.event")
        events = []
        for _event in div_events:
            h4 = _event.css("h4")
            a = h4.css("a")
            event_name = a.css("::text").extract_first()
            link = a.css("::attr(href)").extract_first()
            event_id = int( os.path.basename(link) )
            events.append({"event_id": event_id, "event_name": event_name})
        yield {"actor_id": self.actor_id, "events": events}


class EventernoteEventInfoSpider(scrapy.Spider):
    """
    @class EventernoteEventInfoSpider
    @brief a class for searching detailed information of a specified event

    input:
        event_id
    generates:
        {
            "event_id": ,
            "event_name": ,
            "holding_date": ,
            "opening_time": ,
            "starting_time": ,
            "ending_time": ,
            "venue_name": ,
            "venue_id": ,
            "actors": [
                {
                    "actor_name": ,
                    "actor_id": 
                }
            ],
            "related_links": [
            
            ],
            "description": ,
            "participants_cnt": 
        }
    """
    name = "eventernote-event-info"

    def start_requests(self):
        self.event_id = int( getattr(self, "event_id", None) )
        urls = [
            f"{ROOT_URL}/events/{self.event_id}"
        ]

        for url in urls:
            self.event_info = {"event_id": self.event_id}
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # イベント名
        div_event_title = response.css("div.gb_events_detail_title")
        self.event_info["event_name"] = div_event_title.css("h2::text").extract_first()

        # テーブル解析
        div_events_info_table = response.css("div.gb_events_info_table")
        events_info_table = div_events_info_table.css("table.table")
        tr_list = events_info_table.css("tr")
        for tr in tr_list:
            td_list = tr.css("td")
            field = td_list[0].css("::text").extract_first()
            if field == "開催日時":
                holding_date = td_list[1].css("td a::text").extract_first()
                self.event_info["holding_date"] = holding_date
            elif field == "時間":
                holding_time_str = td_list[1].css("td::text").extract_first()
                splt = holding_time_str.split(" ")
                opening_time = splt[1]
                starting_time = splt[3]
                ending_time = splt[5]
                self.event_info["opening_time"] = opening_time
                self.event_info["starting_time"] = starting_time
                self.event_info["ending_time"] = ending_time
            elif field == "開催場所":
                venue_name = td_list[1].css("td a::text").extract_first()
                if venue_name is None:
                    venue_name = ""

                venue_href = td_list[1].css("td a::attr(href)").extract_first()
                if venue_href is not None:
                    venue_id = int( os.path.basename(venue_href) )
                else:
                    venue_id = -1
                self.event_info["venue_name"] = venue_name
                self.event_info["venue_id"] = venue_id
            elif field == "出演者":
                div_listview = td_list[1].css("div.gb_listview")
                if len(div_listview) > 0:
                    li_list = div_listview.css("li")
                    actors = []
                    for _li in li_list:
                        _actor_name = _li.css("a::text").extract_first()
                        _actor_id = int( os.path.basename( _li.css("a::attr(href)").extract_first() ) )
                        actors.append({"actor_name": _actor_name, "actor_id": _actor_id})
                    self.event_info["actors"] = actors
                else:
                    self.event_info["actors"] = []
            elif field == "関連リンク":
                related_links = td_list[1].css("td a::text").extract()
                self.event_info["related_links"] = related_links
            elif field == "Twitterハッシュタグ":
                hashtag = td_list[1].css("td a::text").extract_first()
                if hashtag is not None:
                    self.event_info["hashtag"] = hashtag
                else:
                    self.event_info["hashtag"] = ""
            else: # description
                description = td_list[1].css("td::text").extract_first()
                if description is not None:
                    self.event_info["description"] = description
                else:
                    self.event_info["description"] = ""

        # 参加者数
        div_span4 = response.css("div.span4")
        h2_elems = div_span4.css("h2")
        for _h2 in h2_elems:
            h2_text = _h2.css("::text").extract_first()
            if h2_text.find("このイベントに参加のイベンター") >= 0:
                participants_count = int( h2_text.replace("このイベントに参加のイベンター(", "").replace("人)", "") )
                self.event_info["participants_cnt"] = participants_count

        yield self.event_info


class EventernoteActorsRankingSpider(scrapy.Spider):
    """
    @class EventernoteActorsRankingSpider
    @brief a class for deriving actors ranking

    input:
        none
    generates:
        {
            "actor_id":,
            "actor_name":
        }
    """
    name = "eventernote-actors-ranking"

    def start_requests(self):
        urls = [
            f"{ROOT_URL}/actors/ranking"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        div_ranking = response.css("div.gb_ranking")
        li_actors = div_ranking.css("li")
        for li_actor in li_actors:
            a_actor = li_actor.css("a")
            actor_name = a_actor.css("::text").extract_first()
            actor_link = a_actor.css("::attr(href)").extract_first()
            actor_id = int( os.path.basename(actor_link) )
            yield {"actor_id": actor_id, "actor_name": actor_name}


class EventernoteActorsSpider(scrapy.Spider):
    """
    @class EventernoteActorsSpider
    @brief a class for deriving actors

    input:
        user_cnt_thr threshold of user-count
    generates:
        {
            "actor_id": ,
            "actor_name": ,
            "yomi": ,
            "user_cnt": 
        }
    """
    name = "eventernote-actors"
    initials = [
        "あ", "い", "う", "え", "お",
        "か", "き", "く", "け", "こ",
        "さ", "し", "す", "せ", "そ",
        "た", "ち", "つ", "て", "と",
        "な", "に", "ぬ", "ね", "の",
        "は", "ひ", "ふ", "へ", "ほ",
        "ま", "み", "む", "め", "も",
        "や", "ゆ", "よ",
        "ら", "り", "る", "れ", "ろ",
        "わ", "を", "ん", "ヘ"
    ]

    def start_requests(self):
        self.min_user_cnt = int( getattr(self, "min_user_cnt", None) )
        urls = [f"{ROOT_URL}/actors/initial/{_initial}" for _initial in self.initials]
        for url in urls:
            time.sleep(1.0)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        ul_actors = response.css("ul.gb_actors_list")
        li_actors = ul_actors.css("li")
        for li in li_actors:
            actor_id = int( os.path.basename( li.css("a::attr(href)").extract_first() ) )
            actor_name = li.css("a::text").extract_first()
            yomi = li.css("span.kana::text").extract_first().rstrip()
            user_cnt = int( li.css("span.number::text").extract_first().replace("(", "").replace(")", "") )
            if user_cnt >= self.min_user_cnt:
                yield {"actor_id": actor_id, "actor_name": actor_name, "yomi": yomi, "user_cnt": user_cnt}


class EventernoteActorUsersSpider(scrapy.Spider):
    """
    @class EventernoteActorUsersSpider
    @brief a class for deriving users of a specified actor

    input:
        actor_id actor id
    generates:
        {
            "actor_id": ,
            "users": [
                {
                    "user_id": ,
                    "user_img": 
                },
            ]
        }
    """
    name = "eventernote-actor-users"
    MAX_LIMIT = 1000000

    def start_requests(self):
        self.actor_id = int( getattr(self, "actor_id", None) )
        urls = [
            f"{ROOT_URL}/actors/{self.actor_id}/users?actor_id={self.actor_id}&limit={self.MAX_LIMIT}"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        div_users = response.css("div.gb_users_icon")
        li_usernames = div_users.css("li")
        actor_users = []
        for _li in li_usernames:
            _p_name = _li.css("p.name")
            user_id = _p_name.css("p::text").extract_first()
            _p_img = _li.css("p.img")
            user_img = _p_img.css("p a img::attr(src)").extract_first()
            actor_users.append( {"user_id": user_id, "user_img": user_img} )
        
        yield {"actor_id": self.actor_id, "users": actor_users}


class EventernoteActorUserRankingSpider(scrapy.Spider):
    """
    @class EventernoteActorUserRankingSpider
    @brief a class for deriving user ranking of a specified actor

    input:
        actor_id actor id
    generates:
        {
            "actor_id":,
            "user_ranking": [
                {
                    "user_id": ,
                    "event_cnt": 
                }
            ]
        }
    """
    name = "eventernote-actor-user-ranking"
    re_event_cnt = re.compile(r"[1-9]+[0-9]*回")

    def start_requests(self):
        self.actor_id = int( getattr(self, "actor_id", None) )

        urls = [
            f"{ROOT_URL}/actors/{self.actor_id}"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        div_users_list = response.css("div.gb_users_list")
        li_users_list = div_users_list.css("ul li")
        user_ranking = []
        for _li in li_users_list:
            user_id = _li.css("a::text").extract_first()
            _li_text = _li.css("li::text").extract_first()
            match = self.re_event_cnt.search(_li_text)
            event_cnt = 0
            if match:
                start = match.start()
                end = match.end()
                event_cnt = int(_li_text[start:end-1])
            user_ranking.append({"user_id": user_id, "event_cnt": event_cnt})

        actor_user_ranking = {"actor_id": self.actor_id, "user_ranking": user_ranking}
        yield actor_user_ranking


class EventernoteUserInfoSpider(scrapy.Spider):
    """
    @class EventernoteUserInfoSpider
    @brief a class for deriving a specified user information

    input:
        user_id user id
    generates:
        {
            "user_id": ,
            "following_cnt": ,
            "follower_cnt": ,
            "events_cnt": ,
            "fav_actors": [
                {
                    "actor_name": ,
                    "actor_id": 
                },
            ]
        }
    """
    name = "eventernote-user-info"

    def start_requests(self):
        self.user_id = getattr(self, "user_id", None)

        urls = [
            f"{ROOT_URL}/users/{self.user_id}"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # following/followers/events count
        following_count = 0
        follower_count = 0
        events_count = 0
        div_score_table = response.css("div")
        p_number = div_score_table.css("p.number")

        for _p in p_number:
            a_href = _p.css("a::attr(href)").extract_first()
            if a_href.find("following") >= 0:
                following_count = int( _p.css("a::text").extract_first() )
            elif a_href.find("follower") >= 0:
                follower_count = int( _p.css("a::text").extract_first() )
            elif a_href.find("events") >= 0:
                events_count = int( _p.css("a::text").extract_first() )

        # favorite actors
        ul_actors_list = response.css("ul.gb_actors_list")
        li_actors = ul_actors_list.css("li")
        fav_actors = []
        for _li in li_actors:
            actor_name = _li.css("a::text").extract_first()
            actor_id = int( os.path.basename( _li.css("a::attr(href)").extract_first() ) )
            fav_actors.append({"actor_name": actor_name, "actor_id": actor_id})

        yield {
            "user_id": self.user_id,
            "following_cnt": following_count,
            "follower_cnt": follower_count,
            "events_cnt": events_count,
            "fav_actors": fav_actors
        }


class EventernoteUserEventPagesSpider(scrapy.Spider):
    """
    @class EventernoteUserEventPagesSpider
    @brief a class for deriving number of pages for a specified user and conditions

    input:
        user_id user id
        year year
        month month
        day day
    generates:
        {
            "num_pages": 
        }
    """
    name = "eventernote-user-event-pages"

    def start_requests(self):
        self.user_id = getattr(self, "user_id", None)
        self.year = getattr(self, "year", "")
        self.month = getattr(self, "month", "")
        self.day = getattr(self, "day", "")

        urls = [f"{ROOT_URL}/users/{self.user_id}/events?year={self.year}&month={self.month}&day={self.day}"]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        div_pagination = response.css("div.pagination")
        a_list = div_pagination.css("ul li a")
        num_pages = 0
        for _a in a_list[1:-1]:
            text = _a.css("a::text").extract_first()
            try:
                text = int(text)
                num_pages = text
            except:
                pass

        yield {"num_pages": num_pages}


class EventernoteUserEventListSpider(scrapy.Spider):
    """
    @class EventernoteUserEventListSpider
    @brief a class for deriving a list of events for specified user

    input:
        user_id user id
        year year
        month month
        day day
        num_pages number of pages
    generates:
        {
            "event_name": ,
            "event_id": ,
            "place_name": ,
            "day": ,
            "holding_time": ,
            "actors": [
                
            ]
        }
    """
    name = "eventernote-user-event-list"

    def start_requests(self):
        self.user_id = getattr(self, "user_id", None)
        self.year = getattr(self, "year", "")
        self.month = getattr(self, "month", "")
        self.day = getattr(self, "day", "")
        self.num_pages = int(getattr(self, "num_pages", "1"))

        urls = []
        for p in range(self.num_pages):
            urls.append(f"{ROOT_URL}/users/{self.user_id}/events?year={self.year}&month={self.month}&day={self.day}&page={p+1}")

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        div_gb_event_list = response.css("div.gb_event_list li.clearfix")
        
        events = []
        for _entry in div_gb_event_list:
            div_event = _entry.css("div.event")
            div_date = _entry.css("div.date")
            div_count = _entry.css("div.note_count")
            
            # event_name
            event_name = div_event.css("h4 a::text").extract_first()

            # event_id
            event_href = div_event.css("h4 a::attr(href)").extract_first()
            event_id = event_href.replace("/events/", "")
            
            # place_name
            place_name = div_event.css("div.place a::text").extract_first()
            
            # day
            p_tags = div_date.css("p")
            for _p in p_tags:
                _text = _p.css("p::text").extract_first()
                if _text is not None:
                    day = _text[:-2]

            # holding_time
            holding_time = div_event.css("div.place span.s::text").extract_first().rstrip()

            # actors
            actor_list = []
            li_actors = div_event.css("div.actor a")
            for _li_actor in li_actors:
                actor_name = _li_actor.css("a::text").extract_first()
                actor_list.append(actor_name)

            # note_count
            p_note_count = div_count.css("p")
            for _p in p_note_count:
                note_count = _p.css("p::text").extract_first()

            events.append({
                "event_id": event_id,
                "event_name": event_name,
                "place_name": place_name,
                "day": day,
                "holding_time": holding_time,
                "note_count": note_count,
                "actors": actor_list
            })
            
        yield {"events": events}



class EventernoteEventParticipantsSpider(scrapy.Spider):
    """
    @class EventernoteEventParticipantsSpider
    @brief a class for deriving participants of a specified event

    input:
        event_id event id
    generates:
        {
            "event_id": ,
            "participants": [
                ,
            ]
        }
    """
    name = "eventernote-event-participants"
    MAX_LIMIT = 10000000

    def start_requests(self):
        self.event_id = int( getattr(self, "event_id", None) )
        urls = [
            f"{ROOT_URL}/events/{self.event_id}/users?event_id={self.event_id}&limit={self.MAX_LIMIT}"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        div_users_icon = response.css("div.gb_users_icon")
        ul = div_users_icon.css("ul.clearfix")
        p_name = ul.css("p.name")
        participants = []
        for _p in p_name:
            user_id = _p.css("::text").extract_first()
            participants.append(user_id)
        yield {"event_id": self.event_id, "participants": participants}


class EventernoteVenueInfoSpider(scrapy.Spider):
    """
    @class EventernoteVenueInfoSpider
    @brief a class for deriving a specified venue information

    input:
        venue_id venue id
    generates:
        {
            "venue_id": ,
            "venue_name": ,
            "address": ,
            "phone_number": ,
            "official_site_url": ,
            "capacity": ,
            "seat_info": 
        }
    """
    name = "eventernote-venue-info"

    def start_requests(self):
        self.venue_id = int( getattr(self, "venue_id", None) )

        urls = [
            f"{ROOT_URL}/places/{self.venue_id}"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 会場名
        div_title = response.css("div.gb_place_detail_title")
        venue_name = div_title.css("h2::text").extract_first()

        # テーブル解析
        address = ""
        phone_number = ""
        official_site_url = ""
        capacity = ""
        seat_info = ""

        div_table = response.css("div.gb_place_detail_table")
        tr_list = div_table.css("table tr")
        for _tr in tr_list:
            td_list = _tr.css("td")
            field = td_list[0].css("::text").extract_first()
            if field == "所在地":
                address = td_list[1].css("a::text").extract_first()
            elif field == "電話番号":
                phone_number = td_list[1].css("::text").extract_first()
            elif field == "公式サイト":
                official_site_url = td_list[1].css("a::attr(href)").extract_first()
            elif field == "収容人数":
                capacity = td_list[1].css("::text").extract_first()
            elif field == "座席情報":
                seat_info = td_list[1].css("a::attr(href)").extract_first()

        yield {
            "venue_id": self.venue_id,
            "venue_name": venue_name,
            "address": address,
            "phone_number": phone_number,
            "official_site_url": official_site_url,
            "capacity": capacity,
            "seat_info": seat_info
        }
