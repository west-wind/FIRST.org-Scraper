#
# FIRST.org vCard crawler
# 
# AUTHOR: Alex John, B

from bs4 import BeautifulSoup, SoupStrainer, re
import requests, csv

def regEx(comments):
    uri = ''
    extractedURL = re.search(r"\/members\/teams\/.*$", comments)
    if extractedURL != None:
        uri = extractedURL.group().replace(".", "").encode('ascii')
    return uri

def writeToCSV(rowValue, filename):
	with open(filename, "a") as inp_file:
		writer = csv.writer(inp_file)
		writer.writerow(rowValue)

url = "https://www.first.org/members/teams/?#"

page = requests.get(url)    
data = page.text
soup = BeautifulSoup(data)

writeToCSV(["Team Name","Official Team Name","Country","E-mail","Team vCard Link","Regular Telephone","Emergency Telephone"],"CERT_TEAMS_CONTACT_INFO.csv")
for link in soup.find_all('a'):
    sub = link.get('href')
    sub_new = regEx(sub)
    if sub_new != None and sub_new != '':
    	url_new = "https://www.first.org" + sub_new
    	try:
    		teamName, officialName, country, regTelephone, telephone, email = '','','','','',''
    		print "\nGetting data from: ",url_new
    		page = requests.get(url_new)    
    		data = page.text
    		soup = BeautifulSoup(data)
    		new = [s for div in soup.select('.vcard') for s in div.stripped_strings]
    		y = [q.encode('ascii', 'ignore') for q in new]
    		a = 0
    		for i in y:
    			a+=1
    			if i == "Team name":
    				index = y.index(i)
    				q = index + 1
    				teamName = y[q]
    			elif i == "Official team name":
    				index1 = y.index(i)
    				r = index1 + 1
    				officialName = y[r]
    			elif i == "Country of team":
    				index2 = y.index(i)
    				s = index2 + 1
    				country = y[s]
    			elif i == "Regular telephone number":
    				index4 = y.index(i)
    				v = index4 + 1
    				regTelephone = "T:" + str(y[v])
    			elif i == "Emergency telephone number":
    				index3 = y.index(i)
    				t = index3 + 1
    				telephone = "T:" + str(y[t])
    			elif i == "E-mail address":
    				index3 = y.index(i)
    				u = index3 + 1
    				email = y[u]
    		writeToCSV([teamName,officialName,country,email,url_new,regTelephone,telephone],"CERT_TEAMS_CONTACT_INFO.csv")
    	except Exception as e:
    		print e
    		pass
