from app import testcases
from app.models import Lecture
DATA = testcases.DATA

for i in DATA:
	year = i['year']
	for sub in i['subjects']:
		sub_name = sub['name']
		teacher = sub['teacher_name']
		weekly_count = sub['weekly_count']
		daily_count = sub['daily_count']
		is_lab = sub['is_lab']
		location = sub['location']

		lec_object = Lecture(teacher=teacher, subject=sub_name, weekly_count=weekly_count, daily_count=daily_count,
								is_lab=is_lab, year=year, location=location)

		lec_object.save()