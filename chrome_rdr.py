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
    "cache": base_path + "/User Data/Default/Cache/Cache_Data/",
    "bookmarks": base_path + "/User Data/Default/Bookmarks"
}

print(paths["cookies"])


def get_cookies():
    cnn = sqlite3.connect(paths["cookies"])
    # cnn = sqlite3.connect("Cookies.db")
    crs = cnn.cursor()

    cookies_sql = """
    select
        datetime(creation_utc/1e6-11644473600,'unixepoch','utc'),
        host_key,
        top_frame_site_key,
        name,
        value,
        encrypted_value,
        path,
        datetime(expires_utc/1e6-11644473600,'unixepoch','utc'),
        is_secure,
        is_httponly,
        datetime(last_access_utc/1e6-11644473600,'unixepoch','utc'),
        case when has_expires = 1 then true else false end as has_expires,
        priority,
        samesite,
        source_scheme,
        source_port,
        datetime(last_update_utc/1e6-11644473600,'unixepoch','utc')
    from cookies
    """

    crs.execute(cookies_sql)
    rows = crs.fetchall()
    headers = "creation_utc,host_key,top_frame_site_key,name,value,encrypted_value,path,expires_utc,is_secure,is_httponly,last_access_utc,has_expires,priority,samesite,source_scheme,source_port,last_update_utc".split(',')
    html = gen_html(title="Chrome Cookies", headers=headers, data=rows)
    with open("chrome_cookies.html", 'w') as f:
        f.write(html)
    webbrowser.open_new_tab(os.path.join(os.getcwd(), "chrome_cookies.html"))
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
        datetime(last_visit_time/1e6-11644473600,'unixepoch','utc'),
        hidden
    from urls
    """
    crs.execute(history_sql)
    rows = crs.fetchall()
    headers = "id,url,title,visit_count,typed_count,last_visit_time,hidden".split(",")
    html = gen_html(title="Chrome History", headers=headers, data=rows)
    with open ("chrome_history.html", 'w') as f:
        f.write(html)
    webbrowser.open_new_tab(os.path.join(os.getcwd(), "chrome_history.html"))
    # pprint(rows)
    return rows


def get_bookmarks():
    with open(paths["bookmarks"], 'r') as f:
        text = f.read()
    bookmarks = json.loads(text)
    try:
        roots = bookmarks['roots']
    except:
        print('cannot find roots')
    for key, val in roots.items():
        print('key:', key)
        if len(val['children']) > 1:
            for child_key, child in val.items():
                if child_key == 'children':
                    for item in child:
                        print(item)
                else:
                    print("key:", child_key)
                    print("child: ", child)
        else:
            print("val:", val)
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
    # with open('Chrome/User Data/Default/Cache/Cache_Data/f_000003', 'rb') as f:
        # bytes = f.read()
        # print(f"for file 000003: f[0] = {hex(bytes[0])} and f[1] = {hex(bytes[1])}")
        # exit()
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
        get_bookmarks()
        # pprint(get_bookmarks())
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



"""
key: bookmark_bar
val: {'children': [], 'date_added': '13355079180650349', 'date_last_used': '0', 'date_modified': '0', 'guid': '0bc5d13f-2cba-5d74-951f-3f233fe6c908', 'id': '1', 'name': 'Bookmarks bar', 'type': 'folder'}
key: other
key: children
child:  [{'date_added': '13355079367486086', 'date_last_used': '0', 'guid': '4e967a07-a0d3-46e1-b530-31e0cfc1ccf3', 'id': '5', 'meta_info': {'power_bookmark_meta': ''}, 'name': 'Different Online Crypto Tools', 'type': 'url', 'url': 'https://www.devglan.com/'}, {'date_added': '13355079494487496', 'date_last_used': '0', 'guid': '7fa8a9bb-0184-4ce8-9cb2-7812154a4025', 'id': '6', 'meta_info': {'power_bookmark_meta': ''}, 'name': 'Encrypt and Decrypt Text Online', 'type': 'url', 'url': 'https://www.devglan.com/online-tools/text-encryption-decryption'}]
key: date_added
child:  13355079180650351
key: date_last_used
child:  0
key: date_modified
child:  13355079494487496
key: guid
child:  82b081ec-3dd3-529c-8475-ab6c344590dd
key: id
child:  2
key: name
child:  Other bookmarks
key: type
child:  folder
key: synced
val: {'children': [], 'date_added': '13355079180650352', 'date_last_used': '0', 'date_modified': '0', 'guid': '4cf2e351-0e85-532b-bb37-df045d8f8d0f', 'id': '3', 'name': 'Mobile bookmarks', 'type': 'folder'}
"""