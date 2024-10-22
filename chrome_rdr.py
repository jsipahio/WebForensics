import sqlite3
from pprint import pprint
import sys
import pandas as pd
import json

args = sys.argv

base_path = args[1]

paths = {
    "history": base_path + "/User Data/Default/History",
    "cookies": base_path + "\\User Data\\Default\\Network\\Cookies",
    "cache": base_path + "/User Data/Default/Cache/Chache_Data/",
    "bookmarks": base_path + "/User Data/Default/Bookmarks"
}

print(paths["cookies"])


def get_cookies():
    cnn = sqlite3.connect(paths["cookies"])
    # cnn = sqlite3.connect("Cookies.db")
    crs = cnn.cursor()

    cookies_sql = """
    select strftime('%m-%d-%Y', creation_utc, 'unixepoch'),
        host_key,
        top_frame_site_key,
        name,
        value,
        encrypted_value,
        path,
        strftime('%m-%d-%Y', expires_utc, 'unixepoch'),
        is_secure,
        is_httponly,
        strftime('%m-%d-%Y', last_access_utc, 'unixepoch'),
        case when has_expires = 1 then true else false end as has_expires,
        priority,
        samesite,
        source_scheme,
        source_port,
        strftime('%m-%d-%Y', last_update_utc, 'unixepoch')
    from cookies
    """

    crs.execute(cookies_sql)
    rows = crs.fetchall()
    # pprint(rows)
    return rows


def get_history():
    cnn = sqlite3.connect(paths["history"])
    crs = cnn.cursor()

    history_sql = """
    select 
        id,
        url,
        title,
        visit_count,
        typed_count,
        strftime('%m-%d-%Y', last_visit_time, 'unixepoch'),
        hidden
    from urls
    """

    crs.execute(history_sql)
    rows = crs.fetchall()
    # pprint(rows)
    return rows


def get_bookmarks():
    with open(paths["bookmarks"], 'r') as f:
        text = f.read()
    bookmarks = json.loads(text)
    return bookmarks


if __name__ == "__main__":
    if args[1] == "-h":
        print("""usage: python chrome_rdr <chrome_directory> [<option>]
options: --history: Chrome browsing history
         --cookies: Chrome cookies""")
        exit()
    if len(args) < 3:
        print("Chrome history")
        pprint(get_history())
        print("Chrome cookies")
        pprint(get_cookies())
    elif args[2] == "--history":
        print("Chrome history")
        pprint(get_history())
    elif args[2] == "--cookies":
        print("Chrome cookies")
        pprint(get_cookies())
    elif args[2] == "--bookmarks":
        print("Chrome bookmarks")
        pprint(get_bookmarks())
    exit()