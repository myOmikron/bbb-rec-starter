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

# BBB Settings
# Change this to your BBB server secrets. This can be done with bbb-conf --secret on the bbb server
BBB_ENDPOINT = "https://bbb.example.com/bigbluebutton/"
BBB_SECRET = "change_this"
```

## Installation

There is currently no python3.6 or higher available in Ubuntu 16.04, so you need to install it via ppa:
```
add-apt-repository ppa:deadsnakes/ppa
apt update && apt install python3.6 python3-pip
python3.6 -m pip install -r requirements.txt
sed -i 's/python3 /python3.6 /g' bbb-rec-starter.service
```
After that you can continue with the normal installation.

In order to deploy this project start the installer as root / sudo privileged user:

```
./install.sh
```


When you are done with the configuration, start the service with `systemctl start bbb-rec-starter`

## How to use the API

To start the recording for the meeting "English 101" where the moderatorPW is "StrongPassword":

`curl -X POST -d 'secret=your_big_blue_button_secret&meeting_id=English 101&password=StrongPassword' https://bbb.example.com/api/startRecording`

The call needs a few seconds to be executed so you may have to increase the timeout.

### Response

The API returns a json object with the following structure:

```
{
    "success":  bool,
    "result":   str
}
```

### Return Codes

Return Code | Reason
:---:       | ---
200         | Execution was successful
400         | Missing parameter
401         | Unauthorized
500         | Exception occured while using chromedriver
512         | Specified meeting hasn't started yet
513         | Wrong password for meeting specified
514         | The recording has already been started
515         | Recording is not enabled for specified meeting