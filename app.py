# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import os
import sys
import random
import datetime
from argparse import ArgumentParser

import requests
from bs4 import BeautifulSoup

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent, TextSendMessage, StickerSendMessage, ImageSendMessage, LocationSendMessage, TextMessage
)

import phonetic as ph  # Assuming phonetic module is defined elsewhere

# Assuming settings is imported for LINE credentials (not provided in the snippet)
from your_module import settings

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
    except LineBotApiError:
        abort(400)

    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
            # Handle different message types based on the content
            msg = event.message.text.strip()

            if msg == 'hello' or msg == 'hi':
                line_bot_api.reply_message(
                    event.reply_token,
                    StickerSendMessage(package_id=789, sticker_id=10856)
                )
            elif msg.startswith('/'):
                # Handle dictionary lookup
                pass  # Placeholder for cambridge function
            elif msg == '猜一下':
                # Handle random number guessing
                pass
            elif msg == '求籤' or msg == '抽籤':
                # Handle fortune stick drawing
                pass
            elif msg == '最新消息' or msg == '今日新聞':
                # Handle fetching news
                pass
            # Add more message handlers as needed

    return 'OK'
if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
