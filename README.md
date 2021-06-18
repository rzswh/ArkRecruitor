# ArkRecruitor: 明日方舟公开招募助手

这是一个自动识别游戏内屏幕截图，返回公招结果的 Web 后端服务。本程序集成了一个 Slack Bot 插件。

## 安装

你需要安装 Python 3 (Python 3.8.5 测试通过)，并运行以下命令安装依赖（`pip`在某些系统中需替换为`pip3`）

```
pip -r requirements.txt
```

以下命令启动一个单纯的 Web 服务器，并可以指定端口（如7890）：

```
PORT=7890 gunicorn run_flask:app
```

想运行 Slack Bot 功能，按照[设置 Slack Bot](#设置-slack-bot) 一节进行设置，然后运行如下命令
```
SLACK_BOT_TOKEN="xoxb-xxxxxxx" SLACK_SIGNING_SECRET="xxxxxxx" gunicorn run_flask:app
```

你也可以从提供的 Dockerfile 中创建一个 Docker 镜像。

## 使用方法

### Slack Bot 接口

添加 Slack Bot 之后，可以通过向 Bot 私聊共享图片的方式，获得识别结果。比如，手机截屏后将其通过 Slack 共享，发送给 Bot，等待数秒之后 Bot 私聊文字返回的结果。

### Web API 接口

- 向 `/image` 以 `POST` 方法发送表单，表单的 `image` 字段为图片内容。服务器将识别结果以纯文字直接返回。
- 向 `/tags` 以 `POST` 方法发送表单，表单的 `tags` 字段为 `,` 分割的标签，标签支持模糊匹配。服务器将识别结果以纯文字直接返回。
- 以 `GET` 方法访问 `/refresh`，服务器刷新公开招募列表。

## 设置 Slack Bot

> 为什么选择Slack？ ~~首先是我自己想用~~ 它的API是开放的 ~~点名批评TX~~ ，并且容易从国内访问。

在 Slack.com 创建一个自己的账户，通过 [Your Apps](https://api.slack.com/apps) 创建一个自己的 APP 。创建后进入 APP 管理界面，进行如下操作：

- 在左侧切换到 `OAuth & Permissions` 栏目，在 `Scopes` --> `Bot Token Scopes` 栏目增添 `chat:write` 和 `files:read` 这两个权限。
- 在左侧切换到 `Event Subscriptions` 栏目，打开事件订阅开关，在下方 `Subscribe to bot events` 折叠面板中添加 `file_shared` 事件。`Request URL`常常需要更改，请根据你本地测试环境或部署环境填入本服务的事件订阅入口，形如 `https://<domain>/slack/events`。

## 部署提示

本项目提供 `Procfile`，可以直接部署到 Heroku 上。也可以构建 docker 镜像来部署到云服务上。记住在服务环境中设置环境变量 `SLACK_BOT_TOKEN` 和 `SLACK_SIGNING_SECRET` 。

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

You could also build a docker image from provided Dockerfile.

## Setup Slack Bot

> Why Slack is chosen? It has open API, and it is easily accessed from mainland China.

Create your own account on Slack.com if you do not have one yet. Create a channel of your own, and create an app by [Your Apps](https://api.slack.com/apps).

Do the following settings:
- In page `OAuth & Permissions`, add `chat:write` and `files:read` scope to Bot Token Scopes.
- In page `Event Subscriptions`, enable events, and subscribe to bot event `file_shared`. Leave `Request URL` for your local test or deployment.

## Deployment Guide

You can directly deploy this project on Heroku with `Procfile` provided. You can also deploy it using docker image. Remember to set environment variables `SLACK_BOT_TOKEN` and `SLACK_SIGNING_SECRET`.