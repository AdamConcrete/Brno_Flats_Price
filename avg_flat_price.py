from  urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd
import numpy as np


my_url = 'https://www.bezrealitky.cz/vypis/nabidka-prodej/byt/jihomoravsky-kraj/okres-brno-mesto/3-kk?_token=c8C6FsT_Gtn70QmvHrWLpOM-4nhqBPiY1j570QEAi1o'
# openning the connection and grabing the html from the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
#html parser
page_soup = soup(page_html, "html.parser")
#Grabs each flat
containers = page_soup.findAll("div", {"class":"product__body"})

flat_name = []
flat_price = []
flat_location = []
#Grab the data of each flat and store them into lists
for container in containers:
	#Grabs the name of the item
#	flat_name  += container.p.text.split()
	#Grabs the price of each flat
	flat_price += (container.span.strong.text).split()
	#Grabs the location of the flat
#	flat_location += container.a.strong.text.split('Jihomoravský kraj')


#Clean the flat price and change the format into int
flat_price = [element for element in flat_price if element!= 'Kč']
flat_price = [int(element.replace('.', '')) for element in flat_price ]

#Clean the flat name data
#flat_name = [i+j+k+l+m for i,j,k,l,m in zip(flat_name[::5],flat_name[1::5], flat_name[2::5],flat_name[3::5],flat_name[4::5])]

#Clean flat location data
#flat_location = list(filter(None, flat_location))


#Change the three lists into nested dictionary
from collections import defaultdict
flats = defaultdict(dict)
for x, y in zip(flat_name, flat_price):
     flats[x] = y
flats = dict(flats)
#print(flats)

#Construct a data frame
flat_data = pd.DataFrame(list(flats.items()), columns=['Name','Price'])

#Find the average price of a flat in Brno
flat_price_avg = np.around(flat_data["Price"].mean(), decimals=2)

print (f'The average price of a 3kk flat in Brno is: {flat_price_avg} Kč')

