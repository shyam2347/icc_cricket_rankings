from datetime import date
from datetime import timedelta
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import sys
import time

START_DATE = 5
START_MONTH = 1
START_YEAR = 1971

def getUrlResponse(url):
    return requests.get(url)

def getNextDay(curr_date):
    return curr_date + timedelta(days=1)

def getWebResponseFromIccRankings(curr_date):
    url = "http://www.relianceiccrankings.com/datespecific/odi/?stattype=batting&day=" + str(curr_date.day) + \
          "&month=" + str(curr_date.month) + "&year=" + str(curr_date.year);
    #print('Url: ', url)
    response = getUrlResponse(url)
    if response.status_code != 200:
        print('Error reading from URL: ', url)
        sys.exit()
    return BeautifulSoup(response.text, "html.parser")

def testReadFile():
    with open('/tmp/a.txt') as f:
        soup_response = BeautifulSoup(f.read(), "html.parser")
        row_number = 0
        with open('filename', 'w') as myfile:
            for tr in table_rows:
                row_number = row_number + 1
                if row_number < 3:
                    # Skipping header and title rows.
                    continue
                td = tr.find_all('td')
                # We are interested only in the first 3 columns.
                row = [i.text.strip() for i in td[:3]]
                line = ",".join(row)
                print(line)
                myfile.writelines(line + '\n')
        #print(soup_response.find('table'))

def storeWebDataInCSV(curr_date):
    soup_response = getWebResponseFromIccRankings(curr_date)
    table = soup_response.find('table')
    table_rows = table.find_all('tr')
    row_number = 0
    filename = 'csv/' + str(curr_date.year) + '_' + str(curr_date.month) + '_' + str(curr_date.day) + '.csv'
    with open(filename, 'w') as myfile:
        for tr in table_rows:
            row_number = row_number + 1
            if row_number < 3:
                # Skipping header and title rows.
                continue
            td = tr.find_all('td')
            # We are interested only in the first 3 columns.
            row = [i.text.strip() for i in td[:3]]
            line = ",".join(row)
            #print(line)
            myfile.writelines(line + '\n')

def main():
    curr_day = date(START_YEAR, START_MONTH, START_DATE)
    today_day = date.today()
    count = 0
    while True:
        print('Curr day: ', curr_day)
        storeWebDataInCSV(curr_day)
        curr_day = getNextDay(curr_day)
        if curr_day >  today_day:
            break;
        #time.sleep(5)
        count = count + 1
    print('Total days count: ', count)

def test():
    url = "http://www.relianceiccrankings.com/datespecific/odi/?stattype=batting&day=14&month=02&year=1980";
    response = getUrlResponse(url)
    if response.status_code != 200:
        print('Error reading from URL')
        sys.exit()
    soup = BeautifulSoup(response.text, "html.parser")
    with open('/tmp/a.txt', 'w') as f:
        f.write(soup.prettify())

if __name__ == '__main__':
     main()
