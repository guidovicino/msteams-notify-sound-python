#!/usr/bin/python3

"""
Author: Guido Vicino
Last update: 2023-08-23

Description: "The Microsoft Teams Progressive Web App (PWA) correctly generates events (and notification sounds) for calls but not for messages (which are displayed) where no sound is generated. While waiting for the issue to be fixed, this script captures the event on 'dbus' and generates a notification sound."

Requirements:
  - sudo apt install python3-gi
  - pip3 install dbus-python playsound xdg-base-dirs
"""


import logging
import os
from systemd.journal import JournalHandler

import dbus
from xdg_base_dirs import xdg_data_home
from playsound import playsound
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib


# Extra bit to get logging level from environment variable
DEBUG_MODE = (os.environ.get('DEBUG_MODE', 'False') == 'True')
if DEBUG_MODE:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

# Logging Creation
logger = logging.getLogger("msteams-notify-sound-python")

# Create journal logger
journalHandler = JournalHandler(SYSLOG_IDENTIFIER='msteams-notify-sound-python')

# add jh to logger
logger.addHandler(journalHandler)

# Selected Browser
selected_browser = "Microsoft Edge"
#selected_browser = "Google Chrome"

# Sounds Directory ($HOME/.local/share/sounds/msteams-notify-sound-python)
sounds_dir = xdg_data_home() / "sounds" / "msteams-notify-sound-python"

# Sound notification file
sound_file = str(sounds_dir) + "/msteams-notification-tone.mp3"


def handle_notification(bus, message):

    keys = ["app_name", "replaces_id", "app_icon", "summary",
          "body", "actions", "hints", "expire_timeout"]

    args = message.get_args_list()

    global sounds_dir

    if len(args) == 8:
        notification = dict([(keys[i], args[i]) for i in range(8)])
        hintsDictionary = notification["hints"]


        # If the notification is the first one with the Sender PID (Microsoft Teams PWA send sometimes two notification events for the same event) and is launched by an app call "Microsoft Edge" and include the domains "Teams.microsoft.com"
        #
        # WARN: If you ouse

        if "sender-pid" in hintsDictionary and notification["app_name"] == "Microsoft Edge" and "teams.microsoft.com" in notification["body"]:

            logger.info("catched message - id = %s , app_name = %s, body = %s, summary = %s", notification["replaces_id"], notification["app_name"], notification["body"].replace("\n", " "), notification["summary"])
            playsound(sound_file)

        else:
            logger.debug("ignored message - id = %s , app_name = %s, body = %s, summary = %s", notification["replaces_id"], notification["app_name"], notification["body"].replace("\n", " "), notification["summary"])


def main():

    logger.info("Starting to catch Teams notifications..")

    # dbus loop initialization
    DBusGMainLoop(set_as_default=True)

    # Obtaining the bus session
    bus=dbus.SessionBus()

    # Add a filter for the notifications
    bus.add_match_string_non_blocking("type='method_call',interface='org.freedesktop.Notifications',member='Notify',eavesdrop=true")
    
    
    # Callback handle function registration
    bus.add_message_filter(handle_notification)

    # Start the main loop
    loop = GLib.MainLoop()
    loop.run()

if __name__ == '__main__':
    main()

