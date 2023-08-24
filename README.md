# MS Teams Notify with Sound (Python porting)

**Disclaimer**

This script is a porting of the code written by **Christian Foti** in Rust (https://github.com/christianfosli/msteams-notify-with-sound). I wanted to modify some things (e.g., remove duplicate notifications and be able to select the sound myself), but I don't have a deep knowledge of the language. Hence, the porting from here.

**Problem**

Using the Microsoft Teams PWA on a Linux distribution with Gnome, it can be easy to miss notifications.

The built-in notifications (at least with PWA installed via Chrome) only appear for a short period of time,
and there is no sound when they appear, so unless you are constantly looking at the screen,
or constantly checking in MS Teams itself it's easy to miss something.

**Solution**

This python-based console app listens to the notification on dbus and republishes the notification
with a notification sound and in a way that it doesn't dissapear from the notifications center right away.

:warning: **Work-In-Progress**
## Usage

1. Clone this repository
2. Customize the configuration variable of the script (*msteams-notify-sound-python.py*) if you need to:
	1. For example if you installed the Teams PWA with Microsoft Edge instead of Google Chrome you'll want something like this

  ```py
    # Selected Browser
    selected_browser = "Microsoft Edge"
    #selected_browser = "Google Chrome"
  ```

3. Install python requirements if you need:

  ```sh
    sudo apt install python3-gi
    pip3 install dbus-python playsound xdg-base-dirs
  ```

4. Copy the following files in your $HOME directory:

  ```
    cp msteams-notify-sound-python.py $HOME/.local/bin
    cp msteams-notification-tone.mp3 $HOME/.local/share/sounds/msteams-notify-sound-fix/
    cp msteams-notify-sound-python.service $HOME$/.config/systemd/user/
  ```

5.  Run it in the background automatically with systemd. E.g.

  ```sh
    systemctl --user enable ./msteams-notify-sound-python.service
    systemctl --user start msteams-notify-sound-python.service
  ```


6.  Troubleshooting the systemd service:

  ```sh
    systemctl --user status msteams-notify-sound-python
    journalctl SYSLOG_IDENTIFIER=msteams-notify-sound-python -f
  ```
