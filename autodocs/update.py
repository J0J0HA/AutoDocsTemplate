import gh_md_to_html.core_converter
import requests
import yaml
import os
import glob
import json

def emptydir(dir):
    "Deletes the contents of a directory."
    print(f"Clearing folder '{dir}'...")
    for file in glob.glob(dir + "/*"):
        try:
            os.remove(file)
        except IsADirectoryError:
            emptydir(file)
            os.rmdir(file)

# Ensure empty docs folder
try:
    print("Creating folder '../docs'...")
    os.mkdir("../docs")
except FileExistsError:
    print("Folder '../docs' is already existing!")
    emptydir("../docs")

# load config
with open("config.yml", "r") as file:
    print("Loading config...")
    config = yaml.safe_load(file)

# configure default data etc.
print("Constructing extras...")
extra = ''

# -> include style
if "style" in config:
    if "favicon" in config["style"]:
        print("Implementing favicon...")
        extra += '<link rel="icon" href="' + config["style"]["favicon"] + '" />'
    if "load" in config["style"]:
        print("Implementing CSS files...")
        for link in config["style"]["load"]:
            extra += '<link rel="stylesheet" href="' + link + '" />'
    if "themes" in config["style"]:
        print("Implementing themes...")
        extra += '<script>themes = ' + json.dumps(config["style"]["themes"]) + ';</script>'
        if "default theme" in config["style"]:
            extra += '<script>default_theme = "' + config["style"]["default theme"] + '";</script>'
        extra += '<script>apply_theme()</script>'

# -> include scripts
if "scripts" in config:
    for link in config["scripts"]:
        extra += '<script src="' + link + '"></script>'

# load template
with open("static/template.html", "r") as file:
    print("Loading template...")
    template = file.read()

# create required folders
for folder in config["folders"]:
    print(f"Creating folder '{folder}'...")
    os.mkdir("../docs/" + folder)

# implement internal files
print(f"Creating folder '.autodocs'...")
os.mkdir("../docs/:autodocs")
os.system("cp 'static/script.js' '../docs/:autodocs/script.js'")
os.system("cp 'static/style.css' '../docs/:autodocs/style.css'")

# transfer files
for path in config["files"]:
    for filen in glob.glob("../" + path, recursive=True):
        if filen.endswith(".md"):
            print(f"Converting '{filen}'...")
            # .md files get converted to html and saved in docs
            with open(filen, "r") as file:
                raw = file.read()
            html = gh_md_to_html.core_converter.markdown(raw)
            with open("../docs/" + filen.removeprefix("../").removesuffix(".md") + ".html", "w") as file:
                file.write(
                    template
                        .replace("%title%", filen.removeprefix("../"))
                        .replace("%extra%", extra)
                        .replace("%content%", html)
                )
        # all files (also .md) are stored directly in the docs folder
        print(f"Tranferring '{filen}'...")
        try:
            with open(filen, "rb") as file:
                raw = file.read()
            with open("../docs/" + filen.removeprefix("../"), "wb") as file:
                file.write(raw)
        except IsADirectoryError:
            print("-> Is a directory! Skipping...")
            continue

# creating an optional index page
if "index" in config:
    print("Constucting index.html...")
    with open("../" + config["index"], "r") as file:
        raw = file.read()
    html = gh_md_to_html.core_converter.markdown(raw)
    with open("../docs/index.html", "w") as file:
        file.write(
            template
                .replace("%title%", config["index"])
                .replace("%extra%", extra)
                .replace("%content%", html)
        )
