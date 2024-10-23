# import chrome_rdr
# import edge_rdr
# import firefox_rdr
import sys
import os


def print_help():
    help_msg = "WebForensics extracts forensic information for recent browsers, including Edge, Chrome, and Firefox.\n\n"
    help_msg += "Usage: <browser> <-d/-f> <directory/file> [<--history, --bookmarks, --cookies, --cache>] [<-o output_file_or_directory>]\n\n"
    help_msg += "browser: supported broswers are Microsoft Edge Chromium (edgec), Google Chrome (chrome), Mozilla Firefox (firefox)\n"
    help_msg += "pass -d if passing path to browser data directory. pass -f if passing a file. if passing a file, the type (ex: --history) must be specified\n"
    help_msg += "directory: usually located at 'C:\\Users\\username\\AppData\\Local\\CompanyName\\BrowserName'.\n"
    help_msg += "NOTE: Firefox cookies, bookmarks, and history are in Roaming, not Local directory. The Firefox cache is in Local, however."
    help_msg += "file: can be history, cookies, or bookmarks file. must pass file type as next argument\n"
    help_msg += "type: if passing a file this parameter is required. if passing a directory, passing this argument will only return the data for that type\n"
    help_msg += "output: instead of printing to console, data will be output to file or directory stated. if doing a cache dump, output directory must be specified.\n"
    print(help_msg)


def get_args():
    if len(sys.argv) < 4:
        print("Must specify directory/file to search.")
        print_help()
        exit()
    if sys.argv[2] == '-f' and len(sys.argv) < 5:
        print("Must specify type of file to search")
        print_help()
        exit()
    if len(sys.argv) > 5:
        if len(sys.argv) < 7:
            print("if using output file or directory, please specify.")
            print_help()
            exit()
    return sys.argv[2], sys.argv[3], sys.argv[4]


def handle_edge():

    
    exit()


def handle_chrome():
    exit()


def handle_firefox():
    exit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        exit()
    if sys.argv[1] == "edgec":
        handle_edge()
    elif sys.argv[1] == "chrome":
        handle_chrome()
    elif sys.argv[1] == "firefox":
        handle_firefox()
    else:
        print("Invalid or unsupported browser passed.")
        print_help()
        exit()
