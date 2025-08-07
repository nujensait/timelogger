**[Russian version](./README.MD)**

## Table of Contents
- [About project](#about-project)
- [Setup](#setup)
- [Usage](#usage)
- [Contributing](#contributing)

# About project

TimeLogger is a script used to pare/save 
timelog files exported from other applications
(Toggl, TimePlanner, Habitify,etc.)

## Setup

Update pip:
```bash
pip install --upgrade pip
python -m pip install --upgrade pip
```

Setup required modules first:
```bash
pip install --upgrade google-api-python-client 
pip install bs4
pip install wheel
pip install lxml
```

## Usage

Run local http webserver:
```bash
python -m http.server
```
Open file upload page:
http://localhost:8000/upload.py
OR (if you use WAMP like OSPanel):
http://timelogger/upload.py

Upload file (previously imported from other apps) via upload form.
File parsing will run automatically.
All events stored in file will be:
- saved into DB 
  - added to your google calendar

## Contributing
Pull requests are welcome. 
For major changes, please open an issue first to discuss what you would like to change.
My contacts are below.

## Author
Ikonnikov Mikhail [mishaikon@gmail.com](mailto:mishaikon@gmail.com)
