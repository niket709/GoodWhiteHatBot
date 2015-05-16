#from bs4 import BeautifulSoup
import urllib2, urllib, os
from collections import OrderedDict
#import socks
import socket
#test
def Get_URLs(google_search, start):
	URLs = list()
	
	req = urllib2.Request('http://www.google.com/search?q=' + urllib.quote(google_search,'') + '&filter=0&num=' + str(start))
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	source = urllib2.urlopen(req).read()
	for i in source.split('<h3 class=\"r\">'):
		URLs.append(i.split('\"')[1].replace('/url?q=','').split('&')[0])
		
	return URLs

def whois(url):
    whois = os.popen('whois ' + url + ' | grep -E "Email|Phone|Fax|Street|City|State|Country"')
    whois = whois.read()
    return whois

def get_info(URLS):
    stripped_urls = list()
    for i in range(len(URLS)):
        try:
            stripped_urls.append([urls[i].split('/')[2].split('/')[0].replace('www.',''),''])
        except:
            lol = ''

    unique = []
    [unique.append(item) for item in stripped_urls if item not in unique]
    stripped_urls = unique

    for i in stripped_urls:
        if '.' not in i[0]:
            stripped_urls.remove(i)

    for i in range(len(stripped_urls)):
        stripped_urls[i][1] = whois(stripped_urls[i][0])
		#stripped_urls[i][1] = "Whois Data here"

    return stripped_urls

#Setup proxy so Google doesn't force authentication
#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1080)
#socket.socket = socks.socksocket

#Get dork URLs and info
dork = raw_input('Enter your Google dork:\n')
start = input('How many entries would you like to search?\n')

start = int(start)

urls = Get_URLs(dork, start)
full_info = get_info(urls)

#SMTP email scripts
for i in range(len(full_info)):
    print 'Would you like to contact?:'
    print full_info[i][0] + ':'
    for j in urls:
        if full_info[i][0] in j:
            print '- ' + j

    email_status = raw_input('(y/n)\n')
    if email_status == 'y':
        full_info[i].append(True)
    elif email_status == 'n':
        full_info[i].append(False)
    else:
        print 'Unrecognized string, setting email status to False'
        full_info[i].append(False)

import smtplib
# Make this more than a test
sender = 'sender@send.com'
username = 'sender@send.com'#kinda not needed
password = 'urpasswordbruh'
receiver = 'test@test.com'

server = smtplib.SMTP_SSL('104.219.248.40',465)
server.ehlo()
server.login(username, password)

for i in full_info:
    if i[2]:
        msg = "\r\n".join([
          "From: makemeavar",
          "To: makemeavar",
          "Subject: Python Single Google Search",
          "",
          "Email sent by Aaron's Google Dork Bot, in real life you would have emailed " + i[0] + " from the Google dork " + dork,
          "Gathered info:",
          i[0],
          i[1],
          str(i[2])
          ])

        server.sendmail(sender, receiver, msg)
        print "sent email!"
    else:
        print "Email status False"
server.close()








