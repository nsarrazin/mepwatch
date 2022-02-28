import requests
from bs4 import BeautifulSoup
from datetime import datetime

START_URL = "https://www.europarl.europa.eu/doceo/document/PV-9-2022-02-17-TOC_EN.html"
FILE = "raw/attendance.csv"

url = START_URL
f = open(FILE, "w")

f.write("date;location;members\n")

while True:
    #open page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    #find attendance page
    links = soup.findAll(name="a", href=True)
    try:
        attendance       = list(filter(lambda link: link.text != None and "Attendance" in link.text, list(links)))[0]
        
        page_attendance = requests.get("https://www.europarl.europa.eu" + attendance['href'])
        soup_attendance = BeautifulSoup(page_attendance.content, "html.parser")

        # extract data from attendance page
        paragraphs = soup_attendance.findAll("p", class_="contents")
        header = soup_attendance.findAll("td", class_="doc_title", text=True)[0].text

        # format data
        attendees = paragraphs[1].text.split(", ")
        date, location = header.split(" - ")
        date = datetime.strptime(date, "%A, %d %B %Y").date().isoformat()
        
        print(date, location)
        # write data
        f.write(f"{date};{location};{';'.join(attendees)}\n")
    except IndexError:
        print("No attendance sheet !")

    #go to next page
    try:
        next_button = list(filter(lambda link: link.text != None and "Previous" in link.text, list(links)))[0]
        url = "https://www.europarl.europa.eu" + next_button['href']
    except IndexError:
        print("Done !")
        break