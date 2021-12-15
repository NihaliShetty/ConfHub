#import all the necessary libraries
import urllib.request 
from bs4 import BeautifulSoup
import pandas as pd

month_mapping = {'January':'01', 'February':'02', 'March':'03', 'April':'04', 'May':'05', 'June':'06',
				 'July':'07', 'August':'08', 'September':'09', 'October':'10', 'November':'11', 'December':'12', }

main_page = 'https://conferencealerts.com/'
country_page = urllib.request.urlopen(main_page)
soup = BeautifulSoup(country_page, "lxml")
all_div_tags = soup.find_all('div', class_='row topic-names no-margin-left no-margin-right margin-bottom-2 margin-top-2')


subdiv = []
for right_div in all_div_tags:
	subdiv.extend(right_div.find_all('div', class_='col-xs-6 text-left padding-5 no-margin'))

subdiv_links = []
for div in subdiv:
	try:
		temp = div.find_all('a')[0]['href']
		subdiv_links.append(temp)
		if 'Transport' in temp:
			break
	except:
		continue

subdiv_links = [link.split('?')[1] for link in subdiv_links]
print(len(subdiv_links))

conf3_list = []
for div in subdiv_links:
	try:
		category = div.split('=')[1].strip()
		page = urllib.request.urlopen(main_page+'topic-listing.php?page=1&ipp=All&'+div)
		soup1 = BeautifulSoup(page, "lxml")
		a_tags = soup1.find_all('a')
		adv_links = []
		for link in a_tags:
			try:
				if 'show-event?' in link['href']:
					adv_links.append(link['href'])
			except:
				continue

		for link in adv_links:
			try:
				our_link = main_page+link
				adv_page = urllib.request.urlopen(our_link)
				soup2 = BeautifulSoup(adv_page, "lxml") 

				name = soup2.find('span', {'id':'eventNameHeader'}).text.strip()
				date = soup2.find('span', {'id':'eventDate'}).text.split()
				date = date[-1].strip() + '-' + month_mapping[date[-2].strip()] + '-' + date[0][:2]
				loc_country = soup2.find('span', {'id':'eventCountry'}).text.split(',')
				location = loc_country[0].strip()
				country = loc_country[-1].strip()
				website = soup2.find('span', {'id':'eventWebsite'})
				website = website.find('a')['href']
				about_conf = soup2.find('span', {'id':'eventDescription'}).text.strip()
				organizer = soup2.find('span', {'id':'eventOrganiser'}).text.split(':')[1].strip()
				deadline = soup2.find('span', {'id':'eventDeadline'}).text.split()
				deadline = deadline[-1] + '-' + month_mapping[deadline[-2]] + '-' + deadline[-3][:-2]
				organizer_email = "No Information Provided"

				conf3_list.append([date, our_link, name, organizer, category, location, country, website, organizer_email, deadline, about_conf])
			except:
				continue    
	except:
		continue
	print(div + ' - done')

	
df = pd.DataFrame(conf3_list, columns=['Date', 'Link', 'Name', 'Category', 'Organizer', 'Location', 'Country', 'Website', 'Deadline', 'About_Conf'])
df.to_csv('conf3.csv', header=True, index=False)    


