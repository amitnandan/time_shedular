from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm


class Lecture(models.Model):

	YEAR_IN_SCHOOL_CHOICES = (
        ("SY_A", 'Second Year: A'),
        ("SY_B", 'Second Year: B'),
        ("TY_A", 'Third Year: A'),
        ("TY_B", 'Third Year: B'), )
	CATEGORY = (
		(0, 'Lecture'),
		(1, 'Practical'))
	teacher = models.CharField(max_length = 140)
	subject = models.CharField(max_length = 140)
	weekly_count = models.IntegerField()
	daily_count = models.IntegerField(default=1)
	is_lab = models.IntegerField(choices=CATEGORY)
	year = models.CharField(max_length=52, choices=YEAR_IN_SCHOOL_CHOICES)
	location = models.CharField(max_length=10, default="", blank=True)
	
	def __str__(self):
		return self.teacher

class RefreshCount(models.Model):

	name = models.CharField(max_length=10, blank=True)
	id = models.AutoField(primary_key=True)
	tt_created = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return str(self.id)

class TimeTable(models.Model):

	YEAR_IN_SCHOOL_CHOICES = (
        ("SY_A", 'Second Year: A'),
        ("SY_B", 'Second Year: B'),
        ("TY_A", 'Third Year: A'),
        ("TY_B", 'Third Year: B'), )
	CATEGORY = (
		(0, 'Lecture'),
		(1, 'Practical'))

	tt_teacher = models.CharField(max_length = 140,	default="", blank=True)
	tt_subject = models.CharField(max_length = 140, blank=True)
	tt_weekly_count = models.IntegerField(blank=True)
	tt_is_lab = models.IntegerField(choices=CATEGORY, blank=True)
	tt_year = models.CharField(max_length=52, choices=YEAR_IN_SCHOOL_CHOICES, blank=True)
	tt_location = models.CharField(max_length=10, default="", blank=True)
	tt_id = models.IntegerField(blank=False)

	def __str__(self):
		return self.tt_teacher

