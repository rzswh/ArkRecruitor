import slack
import os
from core import response_from_image
import run_flask

if __name__ == "__main__":
    # slack.set_callback(response_from_image)
    run_flask.app.run(host='0.0.0.0', port=int(os.environ.get("SLACK_BOT_PORT", 3000)))
