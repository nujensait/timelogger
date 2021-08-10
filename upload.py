#!C:\Users\ikonnikov\AppData\Local\Programs\Python\Python36-32\python.exe
# Upload file to server
# @source https://www.tutorialspoint.com/file-upload-example-in-python

import cgi, os
import cgitb; cgitb.enable()
import sys
from logger import TimeLogger
import sqlite3
import config

# upload file from form
def upload_file(form):
    fileitem = form['filename']
    filename = fileitem.filename

    # Test if the file was uploaded
    if filename:
       # strip leading path from file name to avoid directory traversal attacks
       fn = os.path.basename(filename)
       # If you run the above script on Unix/Linux, then you need to take care of replacing file separator as follows, otherwise on your windows machine above open() statement should work fine.
       #fn = os.path.basename(fileitem.filename.replace("\\", "/"))
       open('./files/' + fn, 'wb').write(fileitem.file.read())
       message = 'The file "' + fn + '" was uploaded successfully'
       res = 1
    else:
       message = 'No file was uploaded'
       res = 0

    # uploading result message
    print("""\
        <p><i>%s</i></p>
    """ % (message))

    return ('./files/' + fn) if res else ""

# show file uploading form
def show_upload_form():
    print("""\
    <html>
    <body>
        <h2>TimeLogger</h2>
        <form action="upload.py" method="post" enctype="multipart/form-data">
            <p><label>File type:</label> 
            <select name="filetype">
                <option value="timeplanner">Time Planner (html)</option>
            </select></p>
            <p><label>File:</label> 
            <input type="file" name="filename" value=""/></p>
           <p><input type="submit" value="Upload" /></p>
        </form>
    </body>
    </html>
    """)

# import data from uploaded file
def import_file(file):

    logger = TimeLogger()

    conn = sqlite3.connect(config.sqlite3_db_path)
    cursor = conn.cursor()

    # parse events
    events = logger.create_events_dict(conn, file)

    # save events to calendar
    logger.create_events(events)

########################################################################################################################

print("Content-type: text/html\n")

# Windows needs stdio set for binary mode.
# @see http://cgi.tutorial.codepoint.net/file-upload
try:
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
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
