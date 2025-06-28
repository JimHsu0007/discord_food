from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    LocationMessage,
)

app = Flask(__name__)

# 填上你的 channel access token & secret
line_bot_api = LineBotApi('你的Channel Access Token')
handler = WebhookHandler('你的Channel Secret')


def fetch_foodpanda_recommendations(lat, lon):
    """Return Foodpanda restaurant recommendations near a location.

    This is a placeholder implementation. Replace it with real API calls if
    Foodpanda provides a public API.
    """
    sample_restaurants = [
        {"name": "示範餐廳 1", "address": "台北市大安區"},
        {"name": "示範餐廳 2", "address": "台北市信義區"},
    ]
    return sample_restaurants


@app.route("/recommend", methods=["GET"])
def recommend():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if not lat or not lon:
        return jsonify({"error": "lat and lon parameters are required"}), 400

    restaurants = fetch_foodpanda_recommendations(lat, lon)
    return jsonify({"restaurants": restaurants})

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text in ("餐廳推薦", "推薦餐廳", "附近餐廳"):
        reply = "請傳送您的位置給我，我會回傳 Foodpanda 推薦餐廳。"
    else:
        reply = f"你說了：{event.message.text}"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )


@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    lat = event.message.latitude
    lon = event.message.longitude
    restaurants = fetch_foodpanda_recommendations(lat, lon)
    if restaurants:
        items = [
            f"{idx + 1}. {r['name']} - {r['address']}" for idx, r in enumerate(restaurants)
        ]
        reply_text = "Foodpanda 推薦餐廳:\n" + "\n".join(items)
    else:
        reply_text = "很抱歉，找不到附近的餐廳。"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text),
    )

if __name__ == "__main__":
    app.run(port=5000)
