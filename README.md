# bbb-rec-starter
This repository is meant to expose the startRecording functionality of bbb. It uses a headless browser to join the specific meeting and pushes the startRecording Button.

## Requirements

```
apt install python3 python3-pip chromium
python3 -m pip install -r requirements.txt
```

## Setup Configuration

In order to get the api to work you have to modify following files:


`bbb_rec_starter/bbb_rec_starter/settings.py`
```
[...]

SECRET_KEY = 'change_this'

[...]

# Add the hosts which are allowed to access the api
ALLOWED_HOSTS = []

[...]

# BBB Settings
# Change this to your BBB server secrets. This can be done with bbb-conf --secret on the bbb server
BBB_ENDPOINT = "https://bbb.example.com/bigbluebutton/"
BBB_SECRET = "change_this"
```

## How to use the API

The server listens on port 8000 in the default configuration.

To start the recording for the meeting "English 101" where the moderatorPW is "StrongPassword":

`curl -X POST 'secret=your_big_blue_button_secret&meeting_id=English 101&password=StrongPassword' https://bbb.example.com:8000/startRecording`

The call needs a few seconds to be executed so you may have to increase the timeout.
