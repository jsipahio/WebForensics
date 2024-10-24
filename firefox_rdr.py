import sqlite3
from pprint import pprint
import sys
import glob
import json

args = sys.argv

base_path = args[1]

paths = {
    "history": base_path + "/Profiles/*.default-release/places.sqlite",
    "cookies": base_path + "/Profiles/*.default-release/cookies.sqlite",
    "cache": base_path + "/Profiles/*.default-release/cache2/",
    "bookmarks": base_path + "/Profiles/*.default-release/places.sqlite"
}

print(paths["cookies"])


def get_cookies():
    print(glob.glob(paths["cookies"]))
    cnn = sqlite3.connect(glob.glob(paths["cookies"])[0])
    # cnn = sqlite3.connect("Cookies.db")
    crs = cnn.cursor()

    cookies_sql = """
    select
        id,
        originAttributes,
        name,
        value,
        host,
        path,
        strftime('%m-%d-%Y', expiry/1000000, 'unixepoch'),
        strftime('%m-%d-%Y', lastAccessed/1000000, 'unixepoch'),
        strftime('%m-%d-%Y', creationTime/1000000, 'unixepoch'),
        case when isSecure = 1 then true else false end as has_expires,
        isHttpOnly,
        inBrowserElement,
        sameSite,
        rawSameSite,
        schemeMap
    from moz_cookies
    """

    crs.execute(cookies_sql)
    rows = crs.fetchall()
    # pprint(rows)
    return rows


def get_history():
    cnn = sqlite3.connect(glob.glob(paths["history"])[0])
    crs = cnn.cursor()

    history_sql = """
    select 
        h.id,
        p.url,
        p.title,
        p.description,
        h.from_visit,
        h.place_id,
        strftime('%m-%d-%Y', h.visit_date/1000000, 'unixepoch'),
        h.visit_type,
        h.session,
        h.source,
        h.triggeringPlaceId
    from moz_historyvisits h join moz_places p on h.place_id = p.id
    """

    crs.execute(history_sql)
    rows = crs.fetchall()
    # pprint(rows)
    return rows


def get_bookmarks():
    cnn = sqlite3.connect(glob.glob(paths['bookmarks'])[0])
    crs = cnn.cursor()

    bookmarks_sql = """
    select 
        b.id,
        p.url,
        p.title,
        p.description,
        b.type,
        b.fk,
        b.parent,
        b.position,
        b.title,
        b.keyword_id,
        b.folder_type,
        b.dateAdded,
        b.lastModified,
        b.guid,
        b.syncStatus,
        b.syncChangeCounter
    from moz_bookmarks b join moz_places p on b.fk = p.id
    """
    crs.execute(bookmarks_sql)
    bookmarks = crs.fetchall()
    return bookmarks


if __name__ == "__main__":
    if args[1] == "-h":
        print("""usage: python firefox_rdr <firefox_directory> [<option>]
options: --history: Firefox browsing history
         --cookies: Firefox cookies""")
        exit()
    if len(args) < 3:
        print("Firefox history")
        pprint(get_history())
        print("Firefox cookies")
        pprint(get_cookies())
    elif args[2] == "--history":
        print("Firefox history")
        pprint(get_history())
    elif args[2] == "--cookies":
        print("Firefox cookies")
        pprint(get_cookies())
    elif args[2] == "--bookmarks":
        print("Firefox bookmarks")
        pprint(get_bookmarks())
    exit()