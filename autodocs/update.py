import gh_md_to_html.core_converter
import requests
import yaml
import os
import glob
import json


def emptydir(dir):
    "Deletes the contents of a directory."
    print(f" -> Clearing folder '{dir}'...")
    for file in glob.glob(dir + "/*"):
        try:
            os.remove(file)
        except IsADirectoryError:
            emptydir(file)
            print(f" -> Deleting folder '{dir}'...")
            os.rmdir(file)

            
# Ensure empty docs folder
try:
    print(" -> Creating folder '../docs'...")
    os.mkdir("../docs")
except FileExistsError:
    print(" -> Folder '../docs' is already existing!")
    emptydir("../docs")

    
# load config
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)
    print(" -> Loaded config from 'config.yml'...")


# create required folders
if "folders" in config:
    for folder in config["folders"]:
        os.mkdir("../docs/" + folder)
        print(f" -> Created additional folder '{folder}'.")

if config["include"]["original-markdown"] is True:
    os.mkdir("../docs/:markdown")
    print(f" -> Created additional folder '../docs/:markdown'.")
    if "folders" in config:
        for folder in config["folders"]:
            os.mkdir("../docs/" + folder)
            print(f" -> Created additional folder '{folder}'.")
# configure default data etc.
print(" -> Implementing additional features...")
extra = ''


# implement internal files
os.mkdir("../docs/:autodocs")
print(f" -> Created internal folder '../docs/:autodocs'.")
os.system("cp 'static/script.js' '../docs/:autodocs/script.js'")
os.system("cp 'static/style.css' '../docs/:autodocs/style.css'")
print(f" -> Created folder contents '../docs/:autodocs'.")


# add themes folder
os.mkdir("../docs/:themes")


# -> include style
if "style" in config:
    if "favicon" in config["style"]:
        print(f" -> Favicon '{config['style']['favicon']}' implemented.")
        extra += '<link rel="icon" href="' + config["style"]["favicon"] + '" />'
    if "load" in config["style"]:
        for link in config["style"]["load"]:
            print(f" -> CSS-file {link} implemented.")
            extra += '<link rel="stylesheet" href="' + link + '" />'
    themes = {}
    for theme in glob.glob("themes/*.css"):
        name = theme.removeprefix("themes/").removesuffix(".css")
        path = ":" + theme
        themes[name] = path
        os.system(f"cp '{theme}' '../docs/{path}'")
        print(f" -> Custom theme '{name}' from '{theme}' implemented. (saved at: '../docs/{path}')")
    if "extra-themes" in config["style"]:
        themes.update(config["style"]["extra-themes"])
        print(" -> Extra themes implemented.")
    extra += '<script>/*THEMES*/themes = ' + json.dumps(themes) + '</script>'
    if "default-theme" in config["style"]:
        extra += '<script>/*DEFAULT THEME*/default_theme = "' + config["style"]["default-theme"] + '"</script>'
    extra += '<script>/*APPLY*/apply_theme()</script>'

        
# -> include scripts
if "scripts" in config:
    for link in config["scripts"]:
        extra += '<script src="' + link + '"></script>'
        print(f" -> JS-file {link} implemented.")

        
# load template
with open("static/template.html", "r") as file:
    template = file.read()
    print(" -> Template loaded.")

    
# transfer files
for path in config["files"]:
    for filen in glob.glob("../" + path, recursive=True):
        if filen.endswith(".md"):
            # .md files get converted to html and saved in /docs
            with open(filen, "r") as file:
                raw = file.read()
            html = gh_md_to_html.core_converter.markdown(raw)
            print(f" -> Converted '{filen}'.")
            with open("../docs/" + filen.removeprefix("../") + ".html", "w") as file:
                file.write(
                    template
                        .replace("%title%", filen.removeprefix("../"))
                        .replace("%extra%", extra)
                        .replace("%content%", html)
                )
            print(f" -> Saved converted '{filen}' at '../docs/{filen.removeprefix('../') + '.html'}'.")
            # write original file in :markdown
            if config["include"]["original-markdown"] is True:
                with open("../docs/:markdown/" + filen.removeprefix("../"), "w") as file:
                    file.write(raw)
                print(f" -> Saved original '{filen}' at '../docs/:markdown/{filen.removeprefix('../')}'.")
        else:
            # other files are tranferred directly to /docs
            try:
                with open(filen, "rb") as file:
                    raw = file.read()
                with open("../docs/" + filen.removeprefix("../"), "wb") as file:
                    file.write(raw)
                print(f" -> Saved original '{filen}' at '../docs/:markdown/{filen.removeprefix('../')}'.")
            except IsADirectoryError:
                print(f" -> '{filen}' is a directory! Skipping transfer...")
                continue

                
# creating an optional index page
if "index" in config:
    with open("../" + config["index"], "r") as file:
        raw = file.read()
    html = gh_md_to_html.core_converter.markdown(raw)
    print(f" -> Converted '{config['index']}'.")
    with open("../docs/index.html", "w") as file:
        file.write(
            template
                .replace("%title%", config["index"])
                .replace("%extra%", extra)
                .replace("%content%", html)
        )
    print(f" -> Saved converted '{config['index']}' at '../docs/index.html'.")
