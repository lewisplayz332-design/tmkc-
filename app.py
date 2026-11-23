# language: Python, file: app.py, runtime: Python 3.10+
import os
import time
import threading
import random
import requests
from flask import Flask, request, jsonify, render_template_string
from instagrapi import Client

app = Flask(__name__)

STATE = {
    "total_sent": 0,
    "live_accounts": 0,
    "sessions": [],
    "proxy": "",
    "target": "",
    "gc_link": "",
    "is_running": False,
    "logs": []
}

try:
    with open("index.html", "r", encoding="utf-8") as f:
        HTML_TEMPLATE = f.read()
except Exception:
    HTML_TEMPLATE = "<h1>index.html missing</h1>"

# --- FULL PAYLOAD DATA ---
PAYLOAD_LIST = [
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝘼𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝙰𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💚 \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🩵 \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🖤 \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🤍 \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  ❤️ \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  🧡 \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💛 \n \n \n",
    "{target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n    {target} 𝙇𝙀𝙒𝙄𝙎 𝘽𝘼𝙰𝙋 𝘽𝙊𝙇 𝙍𝙉𝘿𝙔𝙆𝙀 ➬  💜 \n \n \n"
]

def log_msg(msg):
    timestamp = time.strftime("%H:%M:%S")
    STATE["logs"].append(f"[{timestamp}] {msg}")
    if len(STATE["logs"]) > 100:
        STATE["logs"].pop(0)

# --- KEEP ALIVE ---
def keep_alive():
    url = os.environ.get("RENDER_EXTERNAL_URL")
    if not url:
        return
    while True:
        time.sleep(300) # 5 minutes
        try:
            requests.get(url, timeout=15)
        except Exception:
            pass

if not any(t.name == "KeepAlive" for t in threading.enumerate()):
    t = threading.Thread(target=keep_alive, name="KeepAlive", daemon=True)
    t.start()

# --- SPAM ENGINE ---
def spam_worker():
    log_msg("🔥 Spam Engine Started")
    
    try:
        raw_id = STATE['gc_link'].split('/t/')[-1].replace('/', '').split('?')[0]
        thread_id = str(raw_id).strip()
    except:
        log_msg("❌ Invalid GC Link. Stopping.")
        STATE['is_running'] = False
        return

    clients = []
    for s in STATE["sessions"]:
        cl = Client()
        if STATE['proxy']:
            cl.set_proxy(STATE['proxy'])
        
        try:
            cl.login_by_sessionid(s["session_id"])
            clients.append({"client": cl, "username": s["username"]})
            log_msg(f"✅ Auth OK: @{s['username']}")
        except Exception as e:
            log_msg(f"❌ Auth failed for @{s['username']}: {str(e)[:30]}")

    if not clients:
        log_msg("❌ No valid clients. Stopping.")
        STATE['is_running'] = False
        return

    while STATE["is_running"]:
        for c in clients:
            if not STATE["is_running"]:
                break
            
            cl = c["client"]
            uname = c["username"]
            
            # Pick a random string from the payload list
            template = random.choice(PAYLOAD_LIST)
            
            # Replace {target} with the actual target name from the dashboard
            payload_text = template.format(target=STATE['target'])
            
            try:
                cl.direct_send(payload_text, thread_ids=[thread_id])
                STATE["total_sent"] += 1
                log_msg(f"📨 @{uname} sent payload. Next in 5.5s.")
            except Exception as e:
                log_msg(f"❌ @{uname} failed: {str(e)[:40]}")
                if "login_required" in str(e).lower() or "challenge" in str(e).lower():
                    log_msg(f"⚠️ @{uname} session invalid. Stopping.")
                    STATE["is_running"] = False
                    break
                    
        # 5.5 second delay between sends
        time.sleep(6.5)

    STATE['is_running'] = False
    log_msg("🛑 Spam Engine Stopped")

# --- ROUTES ---

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/state', methods=['GET'])
def get_state():
    STATE["live_accounts"] = len(STATE["sessions"])
    return jsonify(STATE)

@app.route('/api/session', methods=['POST'])
def add_session():
    data = request.json
    sid = data.get('session_id', '').strip().replace('"', '').replace("'", "")
    if sid.startswith("sessionid="):
        sid = sid.replace("sessionid=", "")
    
    if not sid:
        return jsonify({"error": "Empty session"}), 400
    if any(s["session_id"] == sid for s in STATE["sessions"]):
        return jsonify({"error": "Session already added"}), 400

    try:
        cl = Client()
        if STATE.get('proxy'):
            cl.set_proxy(STATE['proxy'])
            
        cl.login_by_sessionid(sid)
        uname = cl.username
        
        STATE["sessions"].append({"session_id": sid, "username": uname})
        log_msg(f"✅ Authenticated: @{uname}")
        return jsonify({"status": "ok", "username": uname})
    except Exception as e:
        log_msg(f"❌ Auth failed: {str(e)[:30]}")
        return jsonify({"error": f"Auth failed: {str(e)[:40]}"}), 400

@app.route('/api/session/<sid>', methods=['DELETE'])
def remove_session(sid):
    STATE['sessions'] = [s for s in STATE['sessions'] if s["session_id"] != sid]
    return jsonify({"status": "ok"})

@app.route('/api/config', methods=['POST'])
def update_config():
    data = request.json
    STATE['proxy'] = data.get('proxy', STATE['proxy'])
    STATE['target'] = data.get('target', STATE['target'])
    STATE['gc_link'] = data.get('gc_link', STATE['gc_link'])
    return jsonify({"status": "ok"})

@app.route('/api/toggle', methods=['POST'])
def toggle_spam():
    data = request.json
    
    if data.get('running') and not STATE['sessions']:
        return jsonify({"error": "No sessions added"}), 400
    if data.get('running') and (not STATE['gc_link'] or not STATE['target']):
        return jsonify({"error": "Missing GC Link or Target"}), 400
        
    STATE['is_running'] = data.get('running', False)
    
    if STATE['is_running']:
        t = threading.Thread(target=spam_worker, daemon=True)
        t.start()
    else:
        log_msg("Stopping engine...")
        
    return jsonify({"status": "ok", "is_running": STATE['is_running']})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)