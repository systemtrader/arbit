#import edgar.mail
#edgar.mail.run()

'''
import edgar.form4

filename = 'I:/arbitdata/edgar/data/98246/0000098246-12-000006.txt'
transactions = edgar.form4.parse(filename)
print(transactions)
'''

'''
import edgar.sql
mySql = edgar.sql.sql()
mySql.drop_table()
mySql.create_table()
'''

'''
import edgar.downloader
edgar.downloader.run()
'''

'''
import google.sql
mySql= google.sql.sql()
mySql.drop_table()
mySql.create_table()
'''

'''
import datetime
symbol = 'tibx'
now = datetime.datetime.now()
google.fundamentals.run(symbol, mySql, now)
fundamentals = mySql.fetch(datetime.date.today(), symbol)
print(fundamentals)
'''