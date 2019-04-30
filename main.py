from bs4 import BeautifulSoup, SoupStrainer
import requests
import collections
import json


def get_grade_links(soup):  # Ugly function to compile all the links to other quarters into an dictionary
	quarters = {}
	for link in links.find_all('a'):
		quarters[link.text] = link['href']
	selected = links.find("li", {"class": "selected"})
	quarters[selected.text] = gradebook_page.split("/")[-1]
	return quarters

# Links for pages in SIS
login_page = "https://sisstudent.fcps.edu/SVUE/"
gradebook_page = "https://sisstudent.fcps.edu/SVUE/PXP_Gradebook.aspx?AGU=0"


with requests.Session() as s:  # Create a requests session

	page = s.get(login_page)  # Navigate to the login page
	login_soup = BeautifulSoup(page.content, features="html.parser")  # Create a parser for the gradebook

	# Prepare the data to post to the login form (apsx)
	data = {}
	data['username'] = input("SIS Username: ")
	data['password'] = input("SIS Password: ")
	data["__VIEWSTATE"] = login_soup.select_one("#__VIEWSTATE")["value"]
	data["__VIEWSTATEGENERATOR"] = login_soup.select_one("#__VIEWSTATEGENERATOR")["value"]
	data["__EVENTVALIDATION"] = login_soup.select_one('#__EVENTVALIDATION')['value']

	# Post data to form, open the gradebook with session
	s.post(login_page, data=data)
	gradebook = s.get(gradebook_page)

	soup = BeautifulSoup(gradebook.content, "html.parser")  # Create a parser for the gradebook

	links = soup.find("div", {"class": "heading_breadcrumb"})
	links = get_grade_links(links)
	
	courses = collections.defaultdict(dict)  # Parent dictionary for course data

	for key, link in links.items():

		url = "https://sisstudent.fcps.edu/SVUE/{}".format(link)
		page = s.get(url)  # Navigate to the login page
		link_soup = BeautifulSoup(page.content, "html.parser")

		# Find the table storing grade data and skip first row (header)
		table = link_soup.find("table", {"class": "info_tbl"})
		rows = iter(table.find_all('tr'))
		next(rows)
		
		for row in rows:  # Loop through all the rows

			cells = row.findAll("td")

			# Iterate over cells in table and construct dictionary format
			course = {}
			course["period"] = cells[0].text.strip()
			course["title"] = cells[1].text.strip()
			course["teacher"] = cells[4].text.strip()
			course["grades"] = cells[5].text.strip()
			course["final_mark"] = cells[7].text.strip()

			courses[key][course["period"]] = course

	with open('courses.json', 'w+') as outfile:  # Save formatted json file
		json.dump(courses, outfile, indent=4)
		print('Finished and saved to "courses.json"')