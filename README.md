# Slack Face Stretcher

Bored of your normal static Slack picture? Face-Stretcher is a cronjob deployed on [Modal](https://modal.com) that will stretch your face to whimsically proportions in your Slack profile picture.

It grabs your current profile picture, stretches it horizontally, and then re-uploads it to Slack. And then, before the next stretching cycle, it smartly reverts your profile picture to its original form, so that it's ready to be stretched all over again!

![example](/example.gif)

## Installation

1. **Sign Up on Modal**

   - Create an account on [Modal](https://modal.com)

2. **Install Modal SDK**

   ```bash
   git clone https://github.com/1rgs/face-stretcher.git
   pip install modal
   modal deploy index.py
   ```

3. **Use your picture**
   - replace `/images/base.jpg` with your own picture

## Setting Up Slack Bot

### Create a Slack App

- Go to https://api.slack.com/apps and click Create New App.
- Select "From scratch" if asked how you want to create your app.
- Name your app and select your workspace.

### Setting Permissions

- Navigate to Features > OAuth & Permissions on the left pane. Under the Scopes > Bot Token Scopes section, add the following scopes: `users.profile:read`, `users.profile:write`
- On the same page, under the OAuth tokens for Your Workspace section, click "Install to Workspace" (or reinstall if it's already installed).
- Get Your Slack Token
- Go to Installed App Settings and then copy "User OAuth Token".

### Create a Modal Secret

- Follow the instructions here to create a Modal secret.
- Store it under "face-stretcher-secrets" and create a key-value pair with the key being SLACK_TOKEN and value being the "User OAuth Token" you copied earlier.
- Now you're all set to give your teammates a face full of laughter every hour! :joy:
