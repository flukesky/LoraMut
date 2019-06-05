from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
from firebase import firebase
app = Flask(__name__)

line_bot_api = LineBotApi('yj/9tYYctUDA02QG085m0VtoQwvs9Rj9ILla+cHHSjgPuXdGKcq/7XOUeg1fdyuxu7PKHC01xTO7YpNtq1nd5Wv/fGgqn4CEnCs0Z10XQoLrNsDBmT77PX2LNYigGf9dG/cnASql6RiWnHXqPJLasAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('633a52a67555ad5d59e278c13206289b')

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/webhook", methods=['POST'])
def webhook():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
    

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    url1 = 'https://lora-mut-4aaab.firebaseio.com/'
    messenger = firebase.FirebaseApplication(url1)
    result1 = messenger.get('/device1',None)
    result = messenger.get('/device1',list(result1)[-1])
    date = result.get('date')
    time = result.get('time')
    humudity = result.get('humudity')
    rain = result.get('rain')
    status = result.get('status')
    temp = result.get('temperature')
    text1=event.message.text
    if str(text1) == "สภาพอากาศ":
        text1 = "ล่าสุดอัพเดท:"+ str(date) +"\nเวลา: "+str(time)+"\nความชื้น: "+str(humudity)+"%\nอุณหภูมิ: "+str(temp)+" องศาเซลเซียส\nปริมาณน้ำฝน: "+str(rain)+"%\n"+str(status)
    else:
        text1 = "โปรดพิมพ์ สภาพอากาศ ให้ถูกต้องหากต้องการดูสภาพอากาศ"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text1))


if __name__ == "__main__":
    app.run()
