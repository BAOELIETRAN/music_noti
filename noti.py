import gi
import subprocess
import urllib.parse
import requests
from bs4 import BeautifulSoup

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Notify

class InputDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Input", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label(label="Please enter the song name:")

        self.entry = Gtk.Entry()

        box = self.get_content_area()
        box.add(label)
        box.add(self.entry)
        self.show_all()

    def get_text(self):
        return self.entry.get_text()

class NotificationApp:
    def __init__(self):
        Notify.init("InputApp")

    def show_notification(self):
        # Create a notification
        notification = Notify.Notification.new("Song Request", "Please enter the song name", None)
        notification.show()

        # Wait a bit for user to see the notification
        Gtk.main_iteration_do(False)
        Gtk.main_iteration_do(False)
        Gtk.main_iteration_do(False)

        # Show the input dialog
        dialog = InputDialog(None)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            song_name = dialog.get_text()
            self.search_and_play_song(song_name)
        else:
            print("No input provided")

        dialog.destroy()

    # def search_and_play_song(self, song_name):
    #     prompt_string = "https://www.youtube.com/results?search_query="
    #     query = urllib.parse.quote(song_name)
    #     searching_result = prompt_string + query
    #     print(searching_result)
    #     subprocess.run(['xdg-open', searching_result], check=True)
    def search_and_play_song(self, song_name):
        prompt_string = "https://www.youtube.com/results?search_query="
        query = urllib.parse.quote(song_name)
        search_url = prompt_string + query
        print(f"Searching YouTube for: {search_url}")

        # Fetch the search results page
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')


        # fix it
        # Find the first video link
        video_link = None
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and '/watch?v=' in href:
                video_link = href
                break

        if video_link:
            video_url = 'https://www.youtube.com' + video_link
            print(f"Opening video URL: {video_url}")
            subprocess.run(['xdg-open', video_url], check=True) 
        else:
            print("No video found")

if __name__ == "__main__":
    app = NotificationApp()
    app.show_notification()
