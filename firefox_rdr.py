import sqlite3
from pprint import pprint
import sys
import glob
import json
import os
import gzip

args = sys.argv

base_path = args[1] if len(args) > 1 else '.'

paths = {
    "history": base_path + "/Profiles/*.default-release/places.sqlite",
    "cookies": base_path + "/Profiles/*.default-release/cookies.sqlite",
    "cache": base_path + "/Profiles/*.default-release/cache2/entries/",
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


def get_cache(output_path):
    print(output_path)
    files = os.listdir(glob.glob(paths['cache'])[0])
    for file in files:
        # print(os.path.join(paths['cache'], file))
        # continue
        if os.path.isdir(os.path.join(glob.glob(paths['cache'])[0], file)):
            continue
        try:
            with open(os.path.join(glob.glob(paths['cache'])[0], file), 'rb') as f:
                bytes = f.read()

                # print(f"for file {file}: f[0] = {hex(bytes[0])} and f[1] = {hex(bytes[1])}")
                if bytes[0] == 0xff and bytes[1] == 0xd8:
                    print(f"{file} is jpg")
                    if output_path is not None:
                        with open(os.path.join(output_path, file + ".jpg"), 'wb') as fout:
                            fout.write(bytes)
                        print(f"path to file is {os.path.join(output_path, file + ".jpg")}")
                elif bytes[0] == 0x89 and bytes[1] == 0x50 and bytes[2] == 0x4e and bytes[3] == 0x47 and bytes[4] == 0x0d and bytes[5] == 0x0a and bytes[6] == 0x1a and bytes[7] == 0x0a:
                    print(f"{file} is png")
                    if output_path is not None:
                        with open(os.path.join(output_path, file + ".png"), 'wb') as fout:
                            fout.write(bytes)
                        print(f"path to file is {os.path.join(output_path, file + ".png")}")
                elif bytes[0] == 0x47 and bytes[1] == 0x49 and bytes[2] == 0x46 and bytes[3] == 0x38 and bytes[4] == 0x37 and bytes[5] == 0x61: 
                    print(f"{file} is gif")
                    if output_path is not None:
                        with open(os.path.join(output_path, file + ".gif"), 'wb') as fout:
                            fout.write(bytes)
                        print(f"path to file is {os.path.join(output_path, file + ".gif")}")
                elif bytes[0] == 0x47 and bytes[1] == 0x49 and bytes[2] == 0x46 and bytes[3] == 0x38 and bytes[4] == 0x39 and bytes[5] == 0x61:
                    print(f"{file} is gif")
                    if output_path is not None:
                        with open(os.path.join(output_path, file + ".gif"), 'wb') as fout:
                            fout.write(bytes)
                        print(f"path to file is {os.path.join(output_path, file + ".gif")}")
                elif bytes[0] == 0x87 and bytes[1] == 0x45 and bytes[2] == 0x42 and bytes[3] == 0x50:
                    print(f"{file} is webp")
                    if output_path is not None:
                        with open(os.path.join(output_path, file + ".webp"), 'wb') as fout:
                            fout.write(bytes)
                        print(f"path to file is {os.path.join(output_path, file + ".webp")}")
                elif bytes[0] == 0x1f and bytes[1] == 0x8b and bytes[2] == 0x08:
                    print(f"{file} is gzip archive")
                    decompressed_bytes = gzip.decompress(bytes)
                    if output_path is not None:
                        with open(os.path.join(output_path, file + ".txt"), 'wb') as fout:
                            fout.write(decompressed_bytes)
                        print(f"path to file is {os.path.join(output_path, file + ".txt")}")
        except:
            continue


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
    if len(args) < 2:
        print("""usage: python chrome_rdr <chrome_directory> [<option>]
options: --history: Chrome browsing history
         --cookies: Chrome cookies""")
        exit()
    if  args[1] == "-h":
        print("""usage: python chrome_rdr <chrome_directory> [<option>]
options: --history: Chrome browsing history
         --cookies: Chrome cookies""")
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
    elif args[2] == "--cache":
        output_path = None
        try:
            output_path = args[3]
            print(f"writing to path {output_path}")
        except:
            print("no output path specified. printing hints")
        print("firefox cache")
        get_cache(output_path)
    exit()