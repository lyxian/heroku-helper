from flask import Flask, request
import threading
import telebot
import time
import sys
import os

from bot import createBot

if len(sys.argv) == 2:
    DEBUG_MODE = eval(sys.argv[1])
else:
    DEBUG_MODE = True

app = Flask(__name__)
bot = createBot()

weburl = os.getenv("PUBLIC_URL") + bot.token

print(weburl)

@app.route("/stop", methods=["GET", "POST"])
def stop():
    if request.method == 'POST':
        password = os.getenv('PASSWORD', '1234')
        if 'password' in request.json and str(request.json['password']) == password:
            shutdown_hook = request.environ.get("werkzeug.server.shutdown")
            try:
                shutdown_hook()
                print("--End--")
            except:
                pass
            return {'status': 'OK'}, 204
        else:
            return {'ERROR': 'Wrong password!'}, 400
    else:
        return {'ERROR': 'Nothing here!'}, 404

@app.route("/" + bot.token, methods=["POST"])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return {'status': 'OK'}, 204

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == 'GET':
        bot.remove_webhook()
        try:
            bot.set_webhook(url=weburl)
            return {'status': 'Webhook set!'}, 204
        except:
            return {'status': 'Webhook not set...Try again...'}, 400
    else:
        return {'ERROR': 'Nothing here!'}, 404

def start():
    bot.remove_webhook()
    time.sleep(2)
    print("Setting webhook...", end=" ")
    try:
        bot.set_webhook(url=weburl)
        print("Webhook set!")
        return "Webhook set!"
    except Exception as e:
        msg = "Webhook not set...Try again..."
        print(f'Error={e}\n{msg}')
        return

if __name__ == "__main__":
    startThread = threading.Thread(target=start, daemon=True)
    startThread.start() # .join
    
    app.run(debug=DEBUG_MODE, host="0.0.0.0", port=int(os.environ.get("PORT", 5005)))