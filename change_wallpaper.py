"""Provides utility methods to fetch earthview images and set them as wallpaper."""

import ctypes
import random
import urllib.request
import os
import sys
import subprocess
import re


class ChangeWallpaper:
    """Provides utility methods to fetch earthview images and set them as wallpaper."""

    @staticmethod
    def set_wallpaper(wallpaper_name):
        """Sets image as wallpaper. Image has to be in current working directory."""

        def gnome_version():
            version_string = subprocess.check_output("gnome-shell --version", shell=True).decode("utf-8")
            version_search = re.search(r"\d*\..*", version_string)
            if version_search:
                return list(map(int, version_search.group(0).split(".")))
            return None

        path_to_dir = os.getcwd()

        # Use SystemParametersInfoA for Python 2
        # Use absolute path for image
        # SPI_SETDESKWALLPAPER = 20
        if sys.platform.startswith("win32"):
            if os.path.isfile(path_to_dir + "\\" + wallpaper_name):
                ctypes.windll.user32.SystemParametersInfoW(20, 0, path_to_dir + "\\" + wallpaper_name, 0x3)
        elif sys.platform.startswith("darwin"):
            if os.path.isfile(path_to_dir + "/" + wallpaper_name):
                os.system("osascript -e 'tell application \"System Events\" to set picture of every desktop to POSIX file \"" +
                          path_to_dir + "/" + wallpaper_name + "\"'")
        elif sys.platform.startswith("linux")\
            and "gnome" in os.environ["XDG_CURRENT_DESKTOP"].lower()\
            and gnome_version() and gnome_version()[0] == 3:
            if os.path.isfile(path_to_dir + "/" + wallpaper_name):
                command = "gsettings set org.gnome.desktop.background picture-uri file://" + path_to_dir + "/" + wallpaper_name
                os.system(command)

    @staticmethod
    def fetch_and_set_random_wallpaper():
        """Fetches random url from 'prettyearth.txt', downloads it, and calls the set_downloaded_image_as_wallpaper() method."""
        with open("prettyearth.txt") as file:
            content = file.readlines()
            content = [x.strip("\n") for x in content]

            random_img_url = content[random.randint(0, len(content) - 1)]
            wallpaper_name = "wallpaper" + str(ChangeWallpaper.get_last_number() + 1) + ".jpg"

            urllib.request.urlretrieve(random_img_url, wallpaper_name)
            ChangeWallpaper.delete_old_image()

        ChangeWallpaper.set_wallpaper(wallpaper_name)

    @staticmethod
    def delete_old_image():
        """Deletes file starting with 'wallpaper', followed by the highest number if one exists. Uses the method get_last_number()
        to determine highest available number."""
        path_to_dir = os.getcwd()
        previous_number = ChangeWallpaper.get_last_number() - 1

        if os.path.isfile(path_to_dir + "/wallpaper" + str(previous_number) + ".jpg"):
            os.remove(path_to_dir + "/wallpaper" +
                      str(previous_number) + ".jpg")

    @staticmethod
    def get_last_number():
        """Searches current directory for images starting with 'wallpaper',
        succeeded by a number and returns the highest number of those."""
        wallpapers = [filename for filename in os.listdir(".") if filename.startswith("wallpaper")]
        numbers = [int(wallpaper[9:][:-4]) for wallpaper in wallpapers]

        if numbers:
            numbers.sort()
            numbers.reverse()

            return numbers[0]

        return 0
