from shutil import move
from os import path, getcwd, mkdir
import os
from bs4 import BeautifulSoup as soup
from requests import get


class scraper_tool(object):
    def __init__(self, url=""):
        self.url = url

    def get_html(self, file_name="", update_cache=False):
        if not file_name:
            file_name = self.url.replace("/", " ")

        file_dir = f"{getcwd()}/website_html"

        if not path.isdir(file_dir):
            mkdir(file_dir)

        file_path = f"{file_dir}/{file_name}.html"
        if not update_cache and path.isfile(file_path):
            with open(file_path, "r") as site:
                html_contents = soup(site, "html.parser")

        else:
            with get(self.url) as site:
                html_contents = soup(site.content, "html.parser")
            with open(file_path, "w+") as file:
                file.write(html_contents.prettify())

        return html_contents

    def write_toCSV(self, file_name, *items):

        def remove_commas(dictionary):
            try:
                for key in dictionary:
                    dictionary[key] = dictionary[key].replace(",", "")
            except Exception as exc:
                print(exc)
                return {}
            return dictionary

        if not items:
            print("No items found:", file_name)

        header = ",".join(items[0].keys()) + "\n" if items else ""
        if not file_name:
            raise FileNotFoundError(file_name)

        if not path.isdir(f"{getcwd()}/stored_data"):
            os.mkdir("stored_data")

        file_path = f"{getcwd()}/stored_data/{file_name}.csv"

        items = list(map(remove_commas, items))

        with open(file_path, "w+") as file:
            file.write(header)
            for item in items:
                file.write(",".join(item.values()) + "\n")

    def group_files(self, category, cat_pos=0, delim="-"):
        file_dir = getcwd()
        if "stored_data" in file_dir:
            file_dir = getcwd()
        else:
            file_dir = f"{getcwd()}/stored_data"

        if not path.isdir(file_dir):
            raise FileNotFoundError
        os.chdir(file_dir)
        file_names = os.listdir()

        if category in file_names:
            del file_names[file_names.index(category)]
        move_files = [fn for fn in file_names if fn.split(delim)[cat_pos] == category]

        category_path = f"{file_dir}/{category}"

        if not path.isdir(category_path):
            os.mkdir(category_path)

        for fn in move_files:
            new_fn = "-".join(fn.split(delim)[1:])
            move(
                f"{file_dir}/{fn}",
                f"{category}/{new_fn}"
            )
