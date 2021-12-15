#import all the necessary libraries
import urllib.request 
from bs4 import BeautifulSoup
import pandas as pd


main_page = 'https://www.allconferencealert.com/'
country_page = urllib.request.urlopen(main_page)
soup = BeautifulSoup(country_page, "lxml")
all_div_tags = soup.find_all('div', class_='topic-detail')

right_div = all_div_tags[3]
href = [element['href'] for element in right_div.find_all('a', class_='confrence')]
print(len(href))

months = ['?date=2019-12', '?date=2020-01', '?date=2020-02', '?date=2020-03', '?date=2020-04']
conf2_list = []

for hf in href:
	category = hf.replace('-', ' ')[:-5]
	for mnth in months:
		try:
			m = mnth.split('-')[1]
			y = mnth.split('-')[0][-4:]
			
			cat_page = urllib.request.urlopen(main_page+hf+mnth)
			soup1 = BeautifulSoup(cat_page, 'lxml')
			all_a_tags = soup1.find_all('a', class_='topic-confr')
			
			for a_tag in all_a_tags:
				try:
					link = a_tag['href']
					
					temp = a_tag.text.split('-')
					date = y + '-' + m + '-' + temp[0].strip()[:-2]
					name = ' '.join(i.strip() for i in temp[1:-1])
					location = temp[-1].split(',')[0].strip()
					country = temp[-1].split(',')[1].strip()

					adv_cat = urllib.request.urlopen(link)
					soup2 = BeautifulSoup(adv_cat, 'lxml')
					conf_info = soup2.find_all('p', class_='abt_contnt')[0].text.strip()
					conf_website = soup2.find_all('a', class_='conf_select')[0].text.strip()

					heading = soup2.find_all('div', class_='col-md-12 cus_heading')[1]
					temp1 = heading.find_all('li')
					conf_organizer = temp1[1].find('span').text.strip()
					conf_email = temp1[4].text.split(':')[1].strip()
					deadline = temp1[7].text.split(':')[1].strip()
					#deadline = '-'.join(deadline.split('-'))

					conf2_list.append([date, link, name, category, conf_organizer, location, country, conf_website, conf_email, deadline, conf_info])	
				except:
					continue
		except:
			continue

	print(hf + ' - done')

df = pd.DataFrame(conf2_list, columns=['Date', 'Link', 'Name','Organizer' ,'Category',  'Location', 'Country', 'Website', 'Organizer_Email', 'Deadline', 'About_Conf'])
df.to_csv('conf2.csv', header=True, index=False)
	

