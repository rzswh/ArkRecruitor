# ArkRecruitor: Arknight Public Recruitment Helper

A Web backend to automatically recognize tags from screenshot. Slack bot plugin is integrated.

## Installation

All you need is Python 3 (Tested on Python 3.8.5) and its dependencies:

```
pip3 -r requirements.txt
```

Start a bare server on specific port (e.g. 7890) by:

```
PORT=7890 gunicorn run_flask:app
```

Start a slack bot web service by following [Setup Slack Bot](#setup-slack-bot) section and run the following command:
```
SLACK_BOT_TOKEN="xoxb-xxxxxxx" SLACK_SIGNING_SECRET="xxxxxxx" gunicorn run_flask:app
```

You could also build a docker image from provided Dockerfile from `docker` branch.

## Setup Slack Bot

> Why Slack is chosen? It has open API, and it is easily accessed from mainland China.

Create your own account on Slack.com if you do not have one yet. Create a channel of your own, and create an app by [Your Apps](https://api.slack.com/apps).

Do the following settings:
- In page `OAuth & Permissions`, add `chat:write` and `files:read` scope to Bot Token Scopes.
- In page `Event Subscriptions`, enable events, and subscribe to bot event `file_shared`. Leave `Request URL` for your local test or deployment.

## Deployment Guide

You can directly deploy this project on Heroku with `Procfile` provided. You can also deploy it using docker image. Remember to set environment variables `SLACK_BOT_TOKEN` and `SLACK_SIGNING_SECRET`.