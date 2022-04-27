from test import bot, append_chat_log, chat_tone
from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)
app.static_folder = 'static'
app.config['SECRET_KEY'] = '89djhff9lhkd93'


@app.route("/")
def home():
    session.clear()
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    incoming_msg = request.args.get('msg')
    chat_log = session.get('chat_log')
    answer = bot(incoming_msg, chat_log)
    session['chat_log'] = append_chat_log(incoming_msg, answer,
                                          chat_log)

    tone = chat_tone(incoming_msg)
    return jsonify([answer, tone])


if __name__ == "__main__":
    app.run(debug=True)
