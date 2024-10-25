import sqlite3
from pprint import pprint
import sys
import json
import os
import gzip
from gen_html import gen_html
import webbrowser

args = sys.argv

base_path = args[1] if len(args) > 1 else '.'

paths = {
    "history": base_path + "/User Data/Default/History",
    "cookies": base_path + "/User Data/Default/Network/Cookies",
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
    headers = "creation_utc,host_key,top_frame_site_key,name,value,encrypted_value,path,expires_utc,is_secure,is_httponly,last_access_utc,has_expires,priority,samesite,source_scheme,source_port,last_update_utc".split(',')
    html = gen_html(title="Edge Chromium Cookies", headers=headers, data=rows)
    with open("edge_chromium_cookies.html", 'w') as f:
        f.write(html)
    webbrowser.open_new_tab(os.path.join(os.getcwd(), "edge_chromium_cookies.html"))
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
    headers = "id,url,title,visit_count,typed_count,last_visit_time,hidden".split(",")
    html = gen_html(title="Edge Chromium History", headers=headers, data=rows)
    with open ("edge_chromium_history.html", 'w') as f:
        f.write(html)
    webbrowser.open_new_tab(os.path.join(os.getcwd, "edge_chromium_history.html"))
    # pprint(rows)
    return rows


def get_bookmarks():
    with open(paths["bookmarks"], 'r') as f:
        text = f.read()
    bookmarks = json.loads(text)
    return bookmarks


def get_cache(output_path):
    print(output_path)
    files = os.listdir(paths['cache'])
    for file in files:
        # print(os.path.join(paths['cache'], file))
        # continue
        if os.path.isdir(os.path.join(paths['cache'], file)):
            continue
        try:
            with open(os.path.join(paths['cache'], file), 'rb') as f:
                bytes = f.read()

                # print(f"for file {file}: f[0] = {hex(bytes[0])} and f[1] = {hex(bytes[1])}")
                if bytes[0] == 0xff and bytes[1] == 0xd8:
                    print(f"{file} is jpg")
                    if output_path is not None:
                        with open(os.path.join(output_path, file + ".jpg"), 'wb') as fout:
                            fout.write(bytes)
                        print(f"path to file is {os.path.join(output_path, file + '.jpg')}")
                elif bytes[0] == 0x89 and bytes[1] == 0x50 and bytes[2] == 0x4e and bytes[3] == 0x47 and bytes[4] == 0x0d and bytes[5] == 0x0a and bytes[6] == 0x1a and bytes[7] == 0x0a:
                    print(f"{file} is png")
                    if output_path is not None:
                        with open(os.path.join(output_path, file + ".png"), 'wb') as fout:
                            fout.write(bytes)
                        print(f"path to file is {os.path.join(output_path, file + '.png')}")
                elif bytes[0] == 0x47 and bytes[1] == 0x49 and bytes[2] == 0x46 and bytes[3] == 0x38 and bytes[4] == 0x37 and bytes[5] == 0x61: 
                    print(f"{file} is gif")
                    if output_path is not None:
                        with open(os.path.join(output_path, file + ".gif"), 'wb') as fout:
                            fout.write(bytes)
                        print(f"path to file is {os.path.join(output_path, file + '.gif')}")
                elif bytes[0] == 0x47 and bytes[1] == 0x49 and bytes[2] == 0x46 and bytes[3] == 0x38 and bytes[4] == 0x39 and bytes[5] == 0x61:
                    print(f"{file} is gif")
                    if output_path is not None:
                        with open(os.path.join(output_path, file + ".gif"), 'wb') as fout:
                            fout.write(bytes)
                        print(f"path to file is {os.path.join(output_path, file + '.gif')}")
                elif bytes[0] == 0x87 and bytes[1] == 0x45 and bytes[2] == 0x42 and bytes[3] == 0x50:
                    print(f"{file} is webp")
                    if output_path is not None:
                        with open(os.path.join(output_path, file + ".webp"), 'wb') as fout:
                            fout.write(bytes)
                        print(f"path to file is {os.path.join(output_path, file + '.webp')}")
                elif bytes[0] == 0x1f and bytes[1] == 0x8b and bytes[2] == 0x08:
                    print(f"{file} is gzip archive")
                    decompressed_bytes = gzip.decompress(bytes)
                    if output_path is not None:
                        with open(os.path.join(output_path, file + ".txt"), 'wb') as fout:
                            fout.write(decompressed_bytes)
                        print(f"path to file is {os.path.join(output_path, file + '.txt')}")
        except:
            continue


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
    elif args[2] == "--cache":
        output_path = None
        try:
            output_path = args[3]
            print(f"writing to path {output_path}")
        except:
            print("no output path specified. printing hints")
        print("chrome cache")
        get_cache(output_path)
    exit()