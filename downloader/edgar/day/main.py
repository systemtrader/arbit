import datetime
import math
import urllib
import io
import csv


def getForm4URLs(date):
    print('Composing the URL of the master file...')
    date = datetime.date(date.year, date.month, date.day)
    year = str(date.year)
    quarter = 'QTR' + str(1 + math.ceil(date.month / 4))
    date = date.strftime('%Y%m%d')
    url = 'https://www.sec.gov/Archives/edgar/daily-index/'+ year + '/' + quarter + '/master.' + date + '.idx'
    print('The URL of the master file is ' + url)

    print('Downloading the master file...')
    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode('utf-8')

    print('Parsing the master file...')
    form4URLs=[]
    file = io.StringIO(text)
    reader = csv.reader(file, delimiter='|')
    for row in reader:
        if len(row) != 5:
            # This is a header
            pass
        elif row[2] == '4':
            # This is a Form 4
            form4URLs.append('https://www.sec.gov/Archives/' + row[4])

    return form4URLs

def run(event, context):
    date = event['date']
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    form4URLs=getForm4URLs(date)

    # Download and parse each Form 4
    print('We have ' + str(len(form4URLs)) + ' Form 4 URLs for the date ' + str(date))
    i=0
    for url in form4URLs:
        print(url)
        
        #invoke SQS somehow...

        i+=1
        if i>100:
            break