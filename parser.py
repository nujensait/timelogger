# Parse htmluseng Bautiful Soap
# @source https://python-scripts.com/beautifulsoup-html-parsing
#!/usr/bin/python3

from bs4 import BeautifulSoup

with open("import/time_planner_logged_activities_2021.html", encoding="utf8") as f:
    contents = f.read()

    soup = BeautifulSoup(contents, 'lxml')

    print(soup.head)
