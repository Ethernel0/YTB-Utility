#Ethernel | https://github.com/Ethernel0 | Python Utility
import pyperclip,re,time,threading,sys,getopt,os
from pytube import Playlist

clipboard_url_filename = "clipboard-url-repo.txt"
playlist_url_filename = "playlist-url-repo.txt"
github_url = "https://github.com/Ethernel0/YTB-Utility"

YOUTUBE_LINK_REGEX = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'

def playlist_parse(user_playlist_link):
    playlist = Playlist(user_playlist_link)
    with open(playlist_url_filename, "w") as fl:
        for video_url in playlist.video_urls:
            fl.write(video_url+"\n")
        print("Successful !")
        print("Saved in "+os.getcwd()+playlist_url_filename)

def is_youtube_link(link):
    return re.match(YOUTUBE_LINK_REGEX, link) is not None

def check_clipboard():
    previous_clipboard = ""
    while True:
        current_clipboard = pyperclip.paste()
        if current_clipboard != previous_clipboard and is_youtube_link(current_clipboard):
            with open(clipboard_url_filename, "a") as file:
                file.write(current_clipboard+"\n")
                previous_clipboard = current_clipboard
                time.sleep(.1)

def mainFunc():
    clipboard_thread = threading.Thread(target=check_clipboard, daemon=True)
    clipboard_thread.start()
    print("Clipboard checker started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Stopping clipboard chcker...")
        print("Restart the terminal !")
        clipboard_thread.join()

def delete_file(file_name):
    try:
        os.remove(file_name)
        print("File deleted successfully !")
    except FileNotFoundError:
        print("Couldn't find the file.")

if __name__ == '__main__':
    argumentList = sys.argv[1:]
    argv_options = "hspc"
    long_argv_options = ["Help", "Start", "Playlist", "ClearFile"]

    if len(argumentList) == 0:
        print("/\-> \tYouTube Utility by https://github.com/Ethernel0")
        print("/\-> \tInclude : Clipboard to File | Playlist Parser")
        print("/\-> \t-h for more information")
        print("/\-> \t"+github_url)

    arguments, values = getopt.getopt(argumentList, argv_options, long_argv_options)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h"):
            print("Possible input:")
            print("-h for help information.")
            print("-s starts the script.")
            print("-p request a link of the Playlist to parse.")
            print("-c request a filename to delete it.")

        elif currentArgument in ("-s"):
            mainFunc()

        elif currentArgument in ("-p"):
            user_playlist_link = input("Enter the playlist link/url:")
            playlist_parse(user_playlist_link)

        elif currentArgument in ("-c"):
            print("Choose the file you want to delete")
            print("'pl' for playlist-url file.")
            print("'cb' for clipboard-url file.")
            user_choice = input("input?:")
            if user_choice == "pl":
                delete_file(playlist_url_filename)
            elif user_choice == "cb":
                delete_file(clipboard_url_filename)
