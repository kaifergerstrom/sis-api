from bs4 import BeautifulSoup, SoupStrainer
import requests
import collections
import json
import argparse


class SISpy:
	# Links for pages in SIS
	p_login = "https://sisstudent.fcps.edu/SVUE/"
	p_gradebook = "https://sisstudent.fcps.edu/SVUE/PXP2_Gradebook.aspx?AGU=0"

	gradebook = {}

	def __init__(self):
		with requests.Session() as s:  # Create a requests session
			page = s.get(self.p_login)  # Navigate to the login page
			s_login = BeautifulSoup(page.content, features="html.parser")  # Create a parser for the gradebook

			# Prepare the data to post to the login form (apsx)
			data = {}
			data['ctl00$MainContent$username'] = ""
			data['ctl00$MainContent$password'] = ""
			data["__VIEWSTATE"] = s_login.select_one("#__VIEWSTATE")["value"]
			data["__VIEWSTATEGENERATOR"] = s_login.select_one("#__VIEWSTATEGENERATOR")["value"]
			data["__EVENTVALIDATION"] = s_login.select_one('#__EVENTVALIDATION')['value']

			# Post data to form, open the gradebook with session
			s.post(self.p_login, data=data)
			r_gradebook = s.get(self.p_gradebook)

			s_grades = BeautifulSoup(r_gradebook.content, "html.parser")  # Create a parser for the gradebook

SISpy = SISpy()