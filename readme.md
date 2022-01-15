# About TimeLogger 

TimeLogger is a script used to pare/save 
timelog files exported from other applications
(Toggl, TimeLoggoer, etc.)

## Usage

Run local http webserver:
```bash
python -m http.server
```
Open file upload page:
http://localhost:8000/upload.html

Upload file (previously imported from other apps) via upload form.
File parsing will run automatically.
All events stored in file will be:
- saved into DB 
  - added to your google calendar

## Contributing
Pull requests are welcome. 
For major changes, please open an issue first to discuss what you would like to change.
Write to me: [mishaikon@gmail.com](mailto:mishaikon@gmail.com)
