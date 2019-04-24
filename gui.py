# -*- coding:utf-8 -*-

import eel
from utils.dialog import Dialogs
from pathlib import Path
from tkinter.filedialog import askdirectory
import re
import json

config_dir = Path.home() / ".vocaloid_song_manager"
config_filename = "song_list.json"
shared_config_path = config_dir / "config.json"
if shared_config_path.exists():
    shared_config = json.loads(shared_config_path.read_text())
else:
    shared_config = {}
if not config_dir.exists():
    config_dir.mkdir(exist_ok=True, parents=True)
dialogs = Dialogs()
suffixes = [".mp3", ".wav", ".flac"]
separators = r"[【】\[\]「」()〈〉《》『』［］,・_]"
singers_info_path = Path(__file__).parents[0] / "resources/singers.json"
singers_info = json.loads(singers_info_path.read_text())
other_type_words = ["PV", "オリジナル", "カバー", "ＰＶ"]


@eel.expose
def set_settings(config):
    shared_config = config
    save_settings()


def save_settings():
    shared_config_path.write_text(json.dumps(shared_config))


@eel.expose
def set_rename_to(song_info_list):
    for song_info in song_info_list:
        song_info["renameTo"] = generate_filename(song_info["units"], song_info["name"])
    return song_info_list


@eel.expose
def save_song_info_list(song_info_list):
    if len(song_info_list) == 0:
        return
    for song_info in song_info_list:
        song_info["renameTo"] = generate_filename(song_info["units"], song_info["name"])
    save_path = Path(song_info_list[0]["path"]).parents[0] / config_filename
    save_path.write_text(json.dumps(song_info_list, indent=4))


def generate_filename(units, filename, join_str="__"):
    titles = "・".join([item["str"] for item in units if item["type"] == "title"])
    singers = "・".join([item["str"] for item in units if item["type"] == "singer"])
    authors = "・".join([item["str"] for item in units if item["type"] == "author"])
    filename_parts = [item for item in [titles, singers, authors] if len(item) > 0]
    suffix = Path(filename).suffix
    return join_str.join(filename_parts) + suffix


def decide_unit_contents(unit_str):
    unit_type = "title"
    singers = []
    for singer_info in singers_info:
        for alias in singer_info.get("aliases"):
            if alias in unit_str:
                unit_str = alias
                singers.append(singer_info.get("name"))
    singers = list(set(singers))
    if len(singers) > 0:
        unit_str = ",".join(singers)
        unit_type = "singer"
    else:
        for other_type_word in other_type_words:
            if other_type_word in unit_str:
                unit_type = "other"
    unit = {
        "str": unit_str,
        "type": unit_type
    }
    return unit


@eel.expose
def load_musics(open_dialog):
    if open_dialog:
        music_dir = dialogs.open_dialog(dialog_open_method=askdirectory)
        shared_config["last_opened"] = str(music_dir.absolute())
        save_settings()
    elif "last_opened" in shared_config:
        music_dir = Path(shared_config.get("last_opened"))
    else:
        return {}
    config_file_path = music_dir / config_filename
    if config_file_path.exists():
        music_info_list = json.loads(config_file_path.read_text())
        return music_info_list
    music_info_list = []
    for path_index, path in enumerate(music_dir.iterdir()):
        if path.suffix not in suffixes:
            continue
        music_info = {
            "index": path_index,
            "path": str(path.absolute()),
            "name": path.name
        }
        units = []
        split = enumerate(re.split(separators, path.name.replace(path.suffix, "")))
        for unit_index, unit_str in split:
            unit_str = unit_str.strip()
            if len(unit_str) == 0:
                continue
            unit = decide_unit_contents(unit_str)
            unit["index"] = unit_index
            units.append(unit)
        music_info["units"] = units
        music_info["renameTo"] = generate_filename(units, music_info["path"])
        music_info_list.append(music_info)
    return music_info_list


@eel.expose
def return_hello():
    return "Hello world!!"


def start_gui():
    eel.init('web')
    eel.start('index.html')


if __name__ == "__main__":
    start_gui()
