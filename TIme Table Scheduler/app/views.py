from django.shortcuts import render,redirect,HttpResponse
from app.models import *
from app.forms import *
from app.scheduler import scheduler_8
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import xlsxwriter, xlrd, xlwt


def index(request):

	return render(request, 'index.html', {})

def accept(request):

	form = LectureForm(request.POST)

	if request.method == 'POST':	
		data = request.POST.get
		if form.is_valid():
			form.save()
	
	
	return render(request, 'accept_data.html', {'form': LectureForm()})

def printf(request):

	objects = Lecture.objects.all()

	return render(request, 'printf.html', {'objects': objects})

def tt_generator(request):

	'''	
	classes = ["SY(A)", "SY(B)", "TY(A)", "TY(B)"]
	rooms_avail = [204, 205, 204, 205]
	labs_avail = [1, 2, 1, 2]
	classroom = 4
	no_of_lectures = 8
	week_days = 6														

	years_ = []

	for i in range(4):

		no_of_subjects = input("Enter Number of Subjects in %s" % classes[i])
		objs = []

		for j in range(no_of_subjects):

			uid = j
			print "Accepting lecture #",j+1
-			teacher = raw_input("Enter Teacher Name: ")
			subject = raw_input("Enter Subject Name: ")
			weekly_count = input("Number of Lectures per week: ")
			is_lab = input("Practical or Lecture(0 or 1): ")
			year = classes[i]
			daily_count = 1
			if is_lab == 0:
				location = rooms_avail[i]
			else:
				location = labs_avail[i]
			lec_object = Lecture(uid, teacher, subject, weekly_count, is_lab, year, daily_count, location)
			objs.append(lec_object)

		years_.append(objs)

	for j in range(4):
		iterator = number_of_subjects[j]
		for k in range(iterator):
			# print years_[j][k]
			pass
	'''

	context = {}

	SY_A_l = Lecture.objects.filter(year="SY_A")
	SY_B_l = Lecture.objects.filter(year="SY_B")
	TY_A_l = Lecture.objects.filter(year="TY_A")
	TY_B_l = Lecture.objects.filter(year="TY_B")

	years_ = [SY_A_l, SY_B_l, TY_A_l, TY_B_l]
	classroom = 4
	no_of_lectures = 8
	week_days = 6
	
	time_table = scheduler_8.Classrooms(classroom, week_days, no_of_lectures, years_)
	if time_table == -1:
		return redirect('/demo/')

	for i in range(len(years_)):
			cur_class = years_[i]
			for j in cur_class:
				if j.weekly_count != 0:
					return redirect('/demo/')
	
	RefreshCount(name="ID").save()
	Refresh_Count = RefreshCount.objects.last()
	print( Refresh_Count)
	tt_count = 0
	for tt in time_table:				# Saving the time table
		tt_count += 1
		print (tt_count)
		if tt_count == 1:
			temp_year = "SY_A"
		if tt_count == 2:
			temp_year = "SY_B"
		if tt_count == 3:
			temp_year = "TY_A"
		if tt_count == 4:
			temp_year = "TY_B"
		for row in tt:
			for col in row:
				if col == -1:
					tt_store = TimeTable(tt_teacher="-1", tt_subject="-1", tt_location=-1, tt_weekly_count="-1", tt_is_lab="-1", tt_year=temp_year, tt_id =str(Refresh_Count))
					tt_store.save()
				elif col == 0:
					tt_store = TimeTable(tt_teacher="0", tt_subject="0", tt_location=0, tt_weekly_count="0", tt_is_lab="0", tt_year=temp_year, tt_id =str(Refresh_Count))
					tt_store.save()
				elif col == -923:
					tt_store = TimeTable(tt_teacher="-923", tt_subject="-923", tt_location="-923", tt_weekly_count="-923", tt_is_lab="-923", tt_year=temp_year, tt_id =str(Refresh_Count))
					tt_store.save()
				else:
					tt_store = TimeTable(tt_teacher=col.teacher, tt_subject=col.subject, tt_location=col.location, tt_weekly_count=col.weekly_count, tt_is_lab=col.is_lab, tt_year=col.year, tt_id =str(Refresh_Count))
					tt_store.save()

	context['time_table'] = time_table

	if request.method == 'POST' :
		data = request.POST.get

		if (data("viewAs")):
			return viewAs(request)

	return render(request, 'tt_display.html', context)

def savedTT(request):

	saved_tt_ids = list(RefreshCount.objects.all())

	no_of_tt = 0
	list_of_ids = []
	for i in saved_tt_ids:
		temp = []
		no_of_tt += 1
		list_of_ids.append(i.id)

	if request.method == 'POST':
		data = request.POST.get
		if data("tt"):
			accepted_tt = data("tt")
			print (accepted_tt)
			print_tt = TimeTable.objects.filter(tt_id=accepted_tt).values()

			SY_A = [x for x in print_tt if x['tt_year'] == "SY_A"]
			SY_B = [x for x in print_tt if x['tt_year'] == "SY_B"]
			TY_A = [x for x in print_tt if x['tt_year'] == "TY_A"]
			TY_B = [x for x in print_tt if x['tt_year'] == "TY_B"]
			temp_tt_list = [SY_A, SY_B, TY_A, TY_B]

			SY_A_L = []			
			SY_B_L = []
			TY_A_L = []
			TY_B_L = []
			
			printable_tt = [SY_A_L, SY_B_L, TY_A_L, TY_B_L]
			
			for classs in xrange(len(temp_tt_list)):
				for row in xrange(6):
					temp = []
					for col in xrange(8):
						if len(temp_tt_list[classs]) != 0:
							temp.append(temp_tt_list[classs].pop(0))
					printable_tt[classs].append(temp)			


			context = { 'time_table': printable_tt, 'list_of_ids': list_of_ids, 'tt_id': data("tt")}
			return render(request, 'savedtt.html', context)

	context = {'list_of_ids': list_of_ids}
	return render(request, 'savedtt.html', context)

def viewAs(request):

	saved_tt_ids = list(RefreshCount.objects.all())

	no_of_tt = 0
	list_of_ids = []
	for i in saved_tt_ids:
		temp = []
		no_of_tt += 1
		list_of_ids.append(i.id)

	teachers_options = TimeTable.objects.all()

	t_list = []	 # Teachers List
	l_list = []  # Classroom & Labs List

	for i in teachers_options:
		if i.tt_teacher not in [u'0', u'-1', u'-923']:
			t_list.append(i.tt_teacher)
		if i.tt_location not in [u'0', u'-1', u'-923']:
			l_list.append(i.tt_location)


	print (t_list)

	class_count = 0
	teachers_list = []

	for _ in range(1):
		temp = []
		for row in range(6):
			temprow = []
			for column in range(8):
				temprow.append(-1)
			temp.append(temprow)
		teachers_list.append(temp)

	if request.method == 'POST' :

		data = request.POST.get
		accepted_teacher = data("viewas_teacher")
		accepted_location = data("viewas_location")

		if (data("viewas_teacher")):
			print ("tt_id") , " #################################### "
			saved_tt_mat_list = []
			saved_tt = list(TimeTable.objects.filter(tt_id=data("tt_id")).values())

			for _ in range(4):
				temp = []
				for row in range(6):
					temprow = []
					for column in range(8):
						temprow.append(saved_tt.pop(0))
					temp.append(temprow)
				saved_tt_mat_list.append(temp)

			while class_count != 4:
				for row in range(6):
					temprow = []
					for column in range(8):
						print ("Here I'm : Current Class Count:", class_count, "row , col :", row,column)
						if saved_tt_mat_list[class_count][row][column]['tt_teacher'] == accepted_teacher:
							teachers_list[0][row][column] = saved_tt_mat_list[class_count][row][column]
						else:
							pass
				class_count +=1
			return render(request, 'viewAs.html', { 'saved_tt': saved_tt_mat_list, 'teachers_options': set(l_list), 'accepted_teacher':accepted_teacher, 'teachers_table': teachers_list , 'teachers_option0': set(t_list) ,'list_of_ids': list_of_ids })

		if (data("viewas_location")):

			saved_tt_mat_list = []
			saved_tt = list(TimeTable.objects.filter(tt_id=data("tt_id")).values())

			for _ in range(4):
				temp = []
				for row in range(6):
					temprow = []
					for column in range(8):
						temprow.append(saved_tt.pop(0))
					temp.append(temprow)
				saved_tt_mat_list.append(temp)
			
			while class_count != 4:
				for row in range(6):
					temprow = []
					for column in range(8):
						if saved_tt_mat_list[class_count][row][column]['tt_location'] == accepted_location:
							teachers_list[0][row][column] = saved_tt_mat_list[class_count][row][column]
							print (teachers_list[0][row][column])
						else:
							pass
				class_count +=1
			return render(request, 'viewAs.html', { 'saved_tt': saved_tt_mat_list, 'teachers_options': set(l_list), 'accepted_location':accepted_location, 'teachers_table': teachers_list , 'teachers_option0': set(t_list),'list_of_ids': list_of_ids })


	return render(request, 'viewAs.html', { 'teachers_options': set(l_list) , 'teachers_option0': set(t_list), 'list_of_ids': list_of_ids })

def temp_handler(myfile):

	print (myfile)

	book = xlrd.open_workbook('media/%s' % myfile)

	print (book.sheet_names())

	first_sheet = book.sheet_by_index(0)

	cell = first_sheet.cell(1,2).value

	num_cols = first_sheet.ncols

	teach_names = first_sheet.col_values(0)
	subj_names = first_sheet.col_values(1)
	week_count = first_sheet.col_values(2)
	prac_lec = first_sheet.col_values(3)
	year_name = first_sheet.col_values(4)
	location = first_sheet.col_values(5)
	for loc in location:
		print (type(loc), loc)
	for index in xrange(len(first_sheet.col_values(0))):
		if type(location[index]) == float:
			location[index] = int(location[index])
		save_db = Lecture(teacher=teach_names[index], subject=subj_names[index], location=str(location[index]), weekly_count=week_count[index], is_lab=prac_lec[index], year=year_name[index])
		print (index, "--> ", teach_names[index], subj_names[index], week_count[index], prac_lec[index], year_name[index])
		save_db.save()

def simple_upload(request):

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        if uploaded_file_url:
        	print ("true")
        	temp_handler(myfile)
        	objects = Lecture.objects.all()
        	return render(request, 'printf.html', {'objects': objects})

    return render(request, 'simple_upload.html')

def home(request):

	return render(request, 'home.html')

def export_into_excel(request):

	if request.method == 'POST':
		data = request.POST.get
		print ("I could reach here")
		if data("id"):
			accepted_tt = data("id")
			print ("Data -->", accepted_tt)

	response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
	response['Content-Disposition'] = "attachment; filename=TTScheduler.xlsx"

	workbook = xlsxwriter.Workbook(response, {'in_memory': True})

	header_format = workbook.add_format({
			'bold': True,
			'align': 'center'
			})

	merge_format = workbook.add_format({
		'bold':     True,
	    'border':   6,
	    'align':    'center',
	    'valign':   'vcenter'
	    })

	for sheets in range(4):

		if sheets == 0:
			sheet = workbook.add_worksheet('Second Year A')
			sheet.merge_range('B4:I4', "SYCO [A] Time Table 2016-2017", header_format)
		if sheets == 1:
			sheet = workbook.add_worksheet('Second Year B')
			sheet.merge_range('B4:I4', "SYCO [B] Time Table 2016-2017", header_format)
		if sheets == 2:
			sheet = workbook.add_worksheet('Third Year A')
			sheet.merge_range('B4:I4', "TYCO [A] Time Table 2016-2017", header_format)
		if sheets == 3:
			sheet = workbook.add_worksheet('Third Year B')
			sheet.merge_range('B4:I4', "TYCO [B] Time Table 2016-2017", header_format)

		sheet.merge_range('B2:I2', "MAHARASHTRA ACADEMY OF ENGINEERING AND EDUCATIONAL RESEARCH'S", header_format)
		sheet.merge_range('B3:I3', "MIT POLYTECHNIC, PUNE 38", header_format)

		columns = ['Days/\nTime', '08:00 - 09:00', '09:00 - 10:00', '10:00 - 11:00' , '11:00 - 12:00', '12:00 - 12:30', '12:30 - 01:30', '01:30 - 02:30' ]
		rows = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

		sheet.set_column(1,8, 20)					# Column Width SET
		for row_height in range(7, 18, 2):			# Row Height SET
			sheet.set_row(row_height,30)

		col_num = 1
		for row_num in range(7, len(rows)+12, 2):
			sheet.merge_range(row_num, col_num, row_num+1, col_num, rows.pop(0), merge_format)

		row_num = 6
		sheet.set_row(row_num,30)

		for row in range(5):
			for col_num in range(1, len(columns)+1):
				sheet.write(row_num,  col_num, columns.pop(0), merge_format)
		
		timetable = list(TimeTable.objects.filter(tt_id=accepted_tt).values())

		timetable_excel = []

		for _ in range(4):
			temp = []
			for row in range(6):
				temprow = []
				for column in range(8):
					temprow.append(timetable.pop(0))
				temp.append(temprow)
			timetable_excel.append(temp)

		cols_num = 2
		rows_num = 7

		for rows in range(6):
			for cols in range(8):

				if str(timetable_excel[sheets][rows][cols]['tt_subject']) == "-923" or str(timetable_excel[sheets][rows][cols]['tt_subject']) == "-1" or str(timetable_excel[sheets][rows][cols]['tt_subject']) == "0":
					pass
				else:
					print_data = timetable_excel[sheets][rows][cols]['tt_subject'] + "-" + timetable_excel[sheets][rows][cols]['tt_teacher'] + "\n" + timetable_excel[sheets][rows][cols]['tt_location']
					sheet.merge_range(rows_num, cols_num, rows_num+1, cols_num, print_data, merge_format)
					cols_num += 1

				if str(timetable_excel[sheets][rows][cols]['tt_subject']) == "-1":
					sheet.merge_range(rows_num, cols_num, rows_num+1, cols_num, "--OFF--", merge_format)
					cols_num += 1

				if str(timetable_excel[sheets][rows][cols]['tt_subject']) == "0":
					sheet.merge_range(rows_num, cols_num, rows_num+1, cols_num, "--Break--", merge_format)
					cols_num += 1

			rows_num += 2
			cols_num = 2

	workbook.close()

	return response

def learn_more(request):

	return render(request, 'learn_more.html', {})
