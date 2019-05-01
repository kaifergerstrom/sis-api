import os
import json
import getpass

class SIS:

	def __init__(self):
		username = input("SIS Username: ")
		password = getpass.getpass(prompt='SIS Password: ')
		os.system("main.py --username {} --password {}".format(username, password))
		with open("courses.json", "r") as read_file:
			self.courses = json.load(read_file)


	def get_teachers(self):  # Returns an array of teachers
		teachers = []
		for key, course in self.courses.items():
			teachers.append(course['teacher'])
			teachers = list(set(teachers))
		return teachers


	def get_courses(self):
		courses = []
		for key, course in self.courses.items():
			courses.append(course['title'])
			courses = list(set(courses))
		return courses

SIS = SIS()
print(SIS.get_courses())






