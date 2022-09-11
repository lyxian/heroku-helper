from flask import Flask, request
import telebot
import time
import os

from utils import loadConfig, loadSecrets
from bot import createBot

configVars = loadSecrets() #loadConfig()
DEBUG_MODE = os.environ.get("DEBUG_MODE", True)

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
            return {'status': 'OK'}, 201
        else:
            return {'ERROR': 'Wrong password!'}, 400
    else:
        return {'ERROR': 'Nothing here!'}, 404

@app.route("/" + bot.token, methods=["POST"])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return {'status': 'OK'}, 201

@app.route('/getPass', methods=['GET', 'POST'])
def _getPass():
    if request.method == 'POST':
        required = ['app', 'password', 'key']
        password = os.getenv('PASSWORD') if not configVars else configVars['PASSWORD']
        if sorted(required) == sorted(request.json) and request.json['password'] == int(password):
            if request.json['app'] in configVars['encryptionStore']:
                appConfig = configVars['encryptionStore'][request.json['app']]
                if request.json['key'] == int(appConfig['PASSWORD']):
                    return {
                        'status': 'OK',
                        'KEY': appConfig['KEY']}, 201
                else:
                    return {
                        'status': 'NOT_OK',
                        'ERROR': 'Wrong password and parameters!'}, 401
            else:
                return {
                    'status': 'NOT_OK',
                    'ERROR': 'App not found in list!'}, 404
        else:
            return {
                'status': 'NOT_OK',
                'ERROR': 'Wrong password and parameters!'}, 401
    else:
        return {
            'status': 'NOT_OK',
            'ERROR': 'Nothing here!'}, 404

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
    app.run(debug=DEBUG_MODE, host="0.0.0.0", port=int(os.environ.get("PORT", 5005)))