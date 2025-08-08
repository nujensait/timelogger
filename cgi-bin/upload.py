#!/usr/bin/env python3
# Upload file to server
# @source https://www.tutorialspoint.com/file-upload-example-in-python
# @see also: big files uploading: http://cgi.tutorial.codepoint.net/big-file-upload

print("Content-type: text/html\n");

import cgi
import cgitb
import os
import sqlite3
import sys

from ..config import config
from logger import TimeLogger

# upload file from form
def upload_file(form):
    fileitem = form['filename']
    filename = fileitem.filename

    # Test if the file was uploaded
    if filename:
        # strip leading path from file name to avoid directory traversal attacks
        fn = os.path.basename(filename)
        # If you run the above script on Unix/Linux, then you need to take care of replacing file separator as follows, otherwise on your windows machine above open() statement should work fine.
        # fn = os.path.basename(fileitem.filename.replace("\\", "/"))
        open('../files/' + fn, 'wb').write(fileitem.file.read())
        message = 'Файл "' + fn + '" успешно загружен.'
        res = 1
    else:
        message = 'Ошибка загрузки файла'
        res = 0

    # uploading result message
    print("""\
        <p><i>%s</i></p>
    """ % (message))

    return ('../files/' + fn) if res else ""


# show file uploading form
def show_upload_form():
    print("""\
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="../assets/style.css">
    </head>
    <body>
        <h2>Time Logger</h2>
        <form action="/cgi-bin/upload.py" method="post" enctype="multipart/form-data" class="uploadForm">
            <div class="center_div">
                <p><h4>Импорт событий</h4></p>
            </div>
            <p><label>Тип:</label> 
            <select name="filetype">
                <option value="timeplanner">Time Planner (html)</option>
            </select></p>
            <p><label>Файл:</label> 
            <input type="file" name="filename" value=""/></p>
            <div class="center_div">
                <p><input type="submit" value="Загрузить" class="btn"/></p>
            </div>
        </form>
    </body>
    </html>
    """)

# import data from uploaded file
def import_file(file):

    logger = TimeLogger()

    conn = sqlite3.connect(config.sqlite3_db_path)
    cursor = conn.cursor()

    # parse events from file
    events = logger.parse_html(conn, file)

    # print imported events
    logger.print_events(events)

    # parse events
    events_dict = logger.create_events_dict(events)

    # save events to calendar
    #logger.create_calendar_events(events_dict)

    # close DB connection
    conn.close()


########################################################################################################################

# enable CGI
cgitb.enable()

# Windows needs stdio set for binary mode.
# @see http://cgi.tutorial.codepoint.net/file-upload
try:
    import msvcrt
    msvcrt.setmode(0, os.O_BINARY)  # stdin  = 0
    msvcrt.setmode(1, os.O_BINARY)  # stdout = 1
except ImportError:
    pass

sys.path.insert(0, os.getcwd())

form = cgi.FieldStorage()

if "filename" in form:
    show_upload_form()
    file = upload_file(form)
    import_file(file)
else:
    show_upload_form()
