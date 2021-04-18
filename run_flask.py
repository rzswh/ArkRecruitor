import flask
from flask import request
from slack_bolt.adapter.flask import SlackRequestHandler
import os
import core
from slack import getApp

app = flask.Flask(__name__)
handler = SlackRequestHandler(getApp())

@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

@app.route('/refresh', methods=['GET'])
def get_tags():
    core.refresh_tags()
    return 'Tags Refreshed.'

@app.route('/image', methods=['POST'])
def handle_image():
    try:
        f = request.files['image']
    except KeyError as e:
        return 'No uploaded image', 400
    return core.response_from_image(f.read())

@app.route('/tags', methods=['POST'])
def handle_tags():
    try:
        tags = request.form['tags']
    except KeyError as e:
        return 'No tags', 400
    return core.response_from_tags(tags.split(','))

if __name__ == "__main__":
    app.run(port=int(os.environ.get("SLACK_BOT_PORT", 3000)))