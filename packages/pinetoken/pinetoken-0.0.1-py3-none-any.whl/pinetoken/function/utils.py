# utils.py
import os
import json
from pathlib import Path

CONFIG_DIR = os.path.join(Path.home(), ".pinetoken")
CONFIG_FILE = os.path.join(CONFIG_DIR, "pinetokeninit.opine")


def ensure_config_dir():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)


def file_exists():
    return os.path.exists(CONFIG_FILE)


def save_data(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_data():
    if not file_exists():
        return {}
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("❌ File korup atau format JSON tidak valid.")
        return {}


def get_config_path():
    return CONFIG_FILE

    # Copyright (c) 2025 openpineaplehub

    # Permission is hereby granted, free of charge, to any person obtaining a copy
    # of this software and associated documentation files (the "Software"), to deal
    # in the Software without restriction, including without limitation the rights
    # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons to whom the Software is
    # furnished to do so, subject to the following conditions: