from django.contrib import admin
from .models import *

class LectureAdmin(admin.ModelAdmin):

	list_display = ["__str__", "subject", "is_lab", "location",  "year", "weekly_count"]
	list_filter = ("teacher", "subject", "is_lab", "location",  "year", "weekly_count")


	class Meta:
		model = Lecture

class TimeTableAdmin(admin.ModelAdmin):

	list_display = ["tt_id", "tt_teacher", "id", "tt_subject", "tt_is_lab", "tt_location",  "tt_year", "tt_weekly_count"]
	list_filter = ("tt_id", "tt_teacher", "tt_subject", "tt_is_lab", "tt_location",  "tt_year", "tt_weekly_count")

	class Meta:
		model = TimeTable

class RefreshCountAdmin(admin.ModelAdmin):

	list_display = [ "name", "id", "tt_created"]

	class Meta:
		model = RefreshCount

admin.site.register(Lecture, LectureAdmin)
admin.site.register(TimeTable, TimeTableAdmin)
admin.site.register(RefreshCount, RefreshCountAdmin)