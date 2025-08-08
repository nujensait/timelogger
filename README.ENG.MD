**[Russian version](./README.MD)**

## Table of Contents
- [About project](#about-project)
- [Project structure](#project-structure)
- [Setup](#setup)
- [Usage](#usage)
- [Tests](#tests)
- [Contributing](#contributing)

# About project

TimeLogger is a script used to pare/save 
timelog files exported from other applications
(Toggl, TimePlanner, Habitify,etc.)

## Project structure

```
./
├── assets/            - Static files (CSS, JS, images)
├── cgi-bin/           - CGI scripts for request processing
├── common/            - Common functions and utilities
├── config/            - Configuration files
├── db/                - Database and related files
├── files/             - Uploaded files
├── import/            - Import files from other applications
├── scripts/           - Helper scripts
├── tests/             - Test scripts and files
└── tmp/               - Temporary files
```

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

## Tests

The project includes the following tests:

- `test_convert_tp_date.py` - tests for date conversion functions from various formats
- `test_exp.py` - tests for regular expressions handling
- `test_gcalexport.py` - tests for GcalExport class for Google Calendar API integration
- `test_logger.py` - tests for TimeLogger class for event logging
- `test_roundtime.py` - tests for time rounding functions

### Running Tests

#### Running all tests

```bash
make test
```

or

```bash
python3 -m pytest tests/ -v
```

#### Running a specific test

```bash
python3 -m pytest tests/test_roundtime.py -v
```

## Contributing
Pull requests are welcome. 
For major changes, please open an issue first to discuss what you would like to change.
My contacts are below.

## Author
Ikonnikov Mikhail [mishaikon@gmail.com](mailto:mishaikon@gmail.com)
