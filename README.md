# bbb-rec-starter
This repository is meant to expose the startRecording functionality of bbb.

It uses a headless browser to join the specific meeting and pushes the startRecording Button. This was a design decision in order to change as few code as possible to keep the maintainability high. This project does not touch any of the original files, so it is possible to install it on the same server bigbluebutton runs on.

## Setup Configuration

Clone the project and modify the `settings.py` to match your needs.


`bbb_rec_starter/bbb_rec_starter/settings.py`
```
[...]

SECRET_KEY = 'change_this'

[...]

# Add the hosts which are allowed to access the api
ALLOWED_HOSTS = []

[...]

RCP_TIME_DELTA = 5
RCP_SECRET = "change_this"

# BBB Settings
# Change this to your BBB server secrets. This can be done with bbb-conf --secret on the bbb server
BBB_ENDPOINT = "https://bbb.example.com/bigbluebutton/"
BBB_SECRET = "change_this"
```

## Installation

In order to deploy this project start the installer as root / sudo privileged user:

```
./install.sh
```

When you are done with the configuration, start the service with `systemctl start bbb-rec-starter`

## How to use the API
- Method: `POST`
- Endpoint: `/bigbluebutton/api/scheduleRecording`

Authentication is done via [RCP](https://github.com/myOmikron/rcp). The endpoint `scheduleRecording` is used as salt.

| Parameter  | Description                                                  |
|------------|--------------------------------------------------------------|
| checksum   | Checksum generated via RCP                                   |
| meeting_id | The ID of the meeting the recording should be scheduled for  |

### Response

The API returns a json object with the following structure:

```json
{
    "success":  bool,
    "message":   str
}
```
