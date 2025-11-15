import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
import random
import pgzrun
import pygame
import urllib.request
from html.parser import HTMLParser

pygame.mixer.music.load("song.mp3")  # ZetaZero
pygame.mixer.music.play(-1)

target = "http://localhost"
level = -2

# Globale Variable für Statusmeldungen
download_messages = []

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for (attr, value) in attrs:
                if attr == "href":
                    self.links.append(value)

def wget_all(url, download_dir="downloads"):
    global download_messages
    download_messages.clear()  # alte Meldungen löschen

    response = urllib.request.urlopen(url)
    html = response.read().decode("utf-8")

    parser = LinkParser()
    parser.feed(html)

    os.makedirs(download_dir, exist_ok=True)

    for link in parser.links:
        if "." in link:
            file_url = urllib.request.urljoin(url, link)
            filename = os.path.join(download_dir, os.path.basename(link))
            # Meldung speichern statt direkt zeichnen
            download_messages.append(f"Downloading {file_url} → {filename}")
            try:
                urllib.request.urlretrieve(file_url, filename)
                download_messages.append(f"Finished {filename}")
            except Exception as e:
                download_messages.append(f"Error {file_url}: {e}")

    download_messages.append("All matching files downloaded!")

def draw():
    global level, target
    screen.clear()
    if level == -2:
        screen.blit("disclaimer", (0, 0))
    elif level == -1:
        screen.blit("title", (0, 0))
    elif level == 0:
        screen.blit("intro", (0, 0))
    elif level == 1:
        screen.blit("back", (0, 0))
        screen.draw.text("Website to download:", center=(400, 130), fontsize=24, color=(25, 200, 55))
        screen.draw.text(target, center=(400, 180), fontsize=24, color=(55, 55, 0))
    elif level == 2:
        screen.blit("back", (0, 0))
        # Alle gespeicherten Meldungen anzeigen
        y = 100
        for msg in download_messages:
            screen.draw.text(msg, (50, y), fontsize=24, color=(25, 200, 55))
            y += 30

def on_key_down(key, unicode=None):
    global level, target
    if key == keys.ESCAPE:
        pygame.quit()
    if key == keys.BACKSPACE:
        target = ""
    elif key == keys.RETURN and level == 1:
        if not target.strip():
            target = "http://127.0.0.1"
        level = 2
        wget_all(target, "downloads")  # Start Download hier
    elif unicode and key != keys.RETURN and level == 1:
        target += unicode

def update():
    global level
    if (level == 0 or level == -2) and keyboard.RETURN:
        level += 1
    elif level - 1 and keyboard.space:
        level = 0
    if level == 2 and keyboard.space:
        level = 0

pgzrun.go()
