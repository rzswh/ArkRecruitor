# ArkRecruitor: Arknight Public Recruitment Helper

A Web backend to automatically recognize tags from screenshot. Slack bot plugin is integrated.

## Installation

All you need is Python 3 (Tested on Python 3.8.5) and its dependencies:

```
pip -r requirements.txt
```

Start a bare server on specific port (e.g. 7890) by:

```
SLACK_BOT_PORT=7890 python3 main.py
```

Follow [Setup Slack Bot](#setup-slack-bot) Section and run the following command:
```
SLACK_BOT_TOKEN="xoxb-xxxxxxx" SLACK_SIGNING_SECRET="xxxxxxx" SLACK_BOT_PORT=8080 python3 main.py
```

You can also build a docker image from provided Dockerfile.

## Setup Slack Bot

> Why Slack is chosen? It has open API, and it is easily accessed from mainland China.

Create your own account on Slack.com if you do not have one yet. Create a channel of your own.