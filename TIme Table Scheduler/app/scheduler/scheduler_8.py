
'''

Lists

'''
from multiprocessing import Queue
import random

BREAKS = [2, 5, 8]

def print_table(classroom, mat_list, week_days, no_of_lectures):							# Printing the Table

	days = ["Monday   ", "Tuesday  ", "Wednesday", "Thursday ", "Friday   ", "Saturday "]

	classes = ["SY(A)", "SY(B)", "TY(A)", "TY(B)"]

	for c in range(classroom):

		print (" ******************* #%s ******************** " % classes[c])

		mat = mat_list[c]

		for i in range(week_days):
			print (days[i]),
			for j in range(no_of_lectures):
				if j not in BREAKS:	
					if mat[i][j] == -1:
						print ("**OFF** | "),
					else:
						print (mat[i][j].subject + "," + str(mat[i][j].is_lab) + "," + str(mat[i][j].location) + " | "),
			

def has_duplicates(l):
	if len(l) != len(set(l)):
		return True
	else:
		return False

def checker(mat_list, sizex, sizey):

	for i in range(sizex):
		for j in range(sizey):
				temp_list = []
				for mat in mat_list:
					if mat[i][j] != 0 and mat[i][j] != -1:
						temp_list.append(mat[i][j])
						if has_duplicates(temp_list) == True:
							print ("Same Teacher Multiple Classroom Error found at :", i, j)
							return False
	print ("All Good.")

def set_lab(current_classroom, current_week_day, current_lecture, inputs_lectures, inputs_labs, yrs, mat, mat_list, q_avail_lab_list, q_avail_class_list, called_from_lect=0):

	cur_lab_list = []
	same_index_teachers = []
	same_index_location = []
	current_lecture_increment = 1

	if current_lecture+1 not in BREAKS and current_lecture not in BREAKS:

		for kk in range(current_classroom):
			mat_old = mat_list[kk]
			if mat_old[current_week_day][current_lecture] != -1:
				same_index_teachers.insert(len(same_index_teachers), mat_old[current_week_day][current_lecture].teacher)
				same_index_location.insert(len(same_index_location), mat_old[current_week_day][current_lecture].location)
			if mat_old[current_week_day][current_lecture+1] != -1:
				same_index_teachers.insert(len(same_index_teachers), mat_old[current_week_day][current_lecture+1].teacher)
				same_index_location.insert(len(same_index_location), mat_old[current_week_day][current_lecture+1].location)
				
		for i in range(2):

			inputs_labs.sort(key=lambda x: x.weekly_count, reverse=True)

			count_teachers = len(inputs_labs)
			#count_location = q_avail_lab_list.qsize()
#a			for kk in range(current_classroom):
#a
#a				mat_old = mat_list[kk]
#a				if mat_old[current_week_day][current_lecture] != -1:
#a					same_index_teachers.insert(len(same_index_teachers), mat_old[current_week_day][current_lecture].teacher)
#a					same_index_location.insert(len(same_index_location), mat_old[current_week_day][current_lecture].location)

			current_teacher = inputs_labs.pop(0)
			
			while count_teachers!=0:
				if current_teacher.teacher in same_index_teachers or current_teacher.daily_count == 0 or current_teacher.weekly_count == 0:
					inputs_labs.insert(len(inputs_labs), current_teacher)
					current_teacher = inputs_labs.pop(0)
				count_teachers -= 1
			
#			current_teacher.location = q_avail_lab_list.get()

#			while count_location!=0:
#				if current_teacher.location in same_index_location:
#					q_avail_lab_list.put(current_teacher.location)
#					current_teacher.location = q_avail_lab_list.get()
#				count_location-=1

			if current_teacher.teacher in same_index_teachers or current_teacher.daily_count == 0 or current_teacher.weekly_count == 0:
				inputs_labs.insert(len(inputs_labs), current_teacher)
#				q_avail_lab_list.put(current_teacher.location)
				if current_lecture_increment == 0:
					current_lecture -= 1
				mat[current_week_day][current_lecture] = -1
				break

			# Missing constraint to add new teacher if insufficient teachers

			#mat[current_week_day][current_lecture] = current_teacher
			# print mat[current_week_day][current_lecture]
			#current_teacher.daily_count -= 1
			#current_teacher.weekly_count -= 1
			#lab_teachers.put(current_teacher)
			#q_avail_lab_list.put(current_teacher.location)
			
			cur_lab_list.append(current_teacher)

			if current_lecture_increment == 1 :
				current_lecture +=1
				current_lecture_increment = 0

		if len(cur_lab_list) == 2:
			current_lecture -= 1
			for lab in range(len(cur_lab_list)):
				current_teacher = cur_lab_list[lab]
				mat[current_week_day][current_lecture + lab] = current_teacher
				# print mat[current_week_day][current_lecture + lab]
				current_teacher.daily_count -= 1
				current_teacher.weekly_count -= 1
				if current_teacher.weekly_count > 2:
					inputs_labs.insert(1,current_teacher)
				else:
					inputs_labs.insert(len(inputs_labs), current_teacher)
#				q_avail_lab_list.put(current_teacher.location)
		else:
			for lab in range(len(cur_lab_list)):
				current_teacher = cur_lab_list[lab]
				inputs_labs.insert(len(inputs_labs), current_teacher)
		#		q_avail_lab_list.put(current_teacher.location)
			if called_from_lect == 0:
				print ("Invoking Set Lecture from inside Set Lab"),
				set_lect(current_classroom, current_week_day, current_lecture, inputs_lectures, inputs_labs, yrs, mat, mat_list, q_avail_lab_list, q_avail_class_list, called_from_lab=1)		
	
	else:

		if called_from_lect == 0:
			print ("Invoking Set Lecture from inside Set Lab"),
			set_lect(current_classroom, current_week_day, current_lecture, inputs_lectures, inputs_labs, yrs, mat, mat_list, q_avail_lab_list, q_avail_class_list, called_from_lab=1)

	
def set_lect(current_classroom, current_week_day, current_lecture, inputs_lectures, inputs_labs, yrs, mat, mat_list, q_avail_lab_list, q_avail_class_list, called_from_lab=0):


	if current_lecture not in BREAKS:

		count_teachers = len(inputs_lectures)
		#count_location = q_avail_class_list.qsize()

		same_index_teachers = []
		same_index_location = []

		inputs_lectures.sort(key=lambda x: x.weekly_count, reverse=True)

		for kk in range(current_classroom):

			mat_old = mat_list[kk]
			if mat_old[current_week_day][current_lecture] != -1:
				same_index_teachers.insert(len(same_index_teachers), mat_old[current_week_day][current_lecture].teacher)
				same_index_location.insert(len(same_index_location), mat_old[current_week_day][current_lecture].location)
		
		while count_teachers >= 0:
			current_teacher = inputs_lectures.pop(0)
			if current_teacher.teacher in same_index_teachers or current_teacher.daily_count == 0 or current_teacher.weekly_count == 0:
				inputs_lectures.insert(len(inputs_lectures), current_teacher)
			else:
				break
			count_teachers -= 1

		# Missing constraint to add new teacher if insufficient teachers
		
		if count_teachers < 0:
			print ("Count Teacher got zero"),
			if called_from_lab == 0:
				print ("Invoking Set Lab from Set Lecture"),
				set_lab(current_classroom, current_week_day, current_lecture, inputs_lectures, inputs_labs, yrs, mat, mat_list, q_avail_lab_list, q_avail_class_list, called_from_lect=1)
			return

	#	while count_location >= 0:
	#		current_teacher.location = q_avail_class_list.get()
	#		if current_teacher.location in same_index_location:
	#			q_avail_class_list.put(current_teacher.location)
	#		else:
	#			break
	#		count_location -= 1

	#	if count_location < 0:
	#		print "Count Location got zero",
	#		return

		mat[current_week_day][current_lecture] = current_teacher
		# print mat[current_week_day][current_lecture]
		current_teacher.daily_count = 0
		current_teacher.weekly_count -= 1
		inputs_lectures.insert(len(inputs_lectures), current_teacher)
	#	q_avail_class_list.put(current_teacher.location)

def replinish_daily_count(current_classroom, week_days, yrs):

	for i in range(len(yrs[current_classroom])):
		yrs[current_classroom][i].daily_count = 1

def pick_next(current_classroom, current_week_day, current_lecture, inputs_lectures, inputs_labs, yrs, mat, mat_list, q_avail_lab_list, q_avail_class_list):

	if current_classroom == 0:

		choice = random.randint(0,1)
		
		if choice == 0 :
			print ("Trying to set lecture ===>"),
			set_lect(current_classroom, current_week_day, current_lecture, inputs_lectures, inputs_labs, yrs, mat, mat_list, q_avail_lab_list, q_avail_class_list)
		else:
			print ("Trying to set lab ===>"),
			set_lab(current_classroom, current_week_day, current_lecture, inputs_lectures, inputs_labs, yrs, mat, mat_list, q_avail_lab_list, q_avail_class_list)

	if current_classroom == 1 or current_classroom == 3:

		if mat_list[current_classroom-1][current_week_day][current_lecture] == -1:
			choice = random.randint(0,1)			
			if choice == 0 :
				print ("Trying to set lecture ===>"),
				set_lect(current_classroom, current_week_day, current_lecture, inputs_lectures, inputs_labs, yrs, mat, mat_list, q_avail_lab_list, q_avail_class_list)
			else:
				print ("Trying to set lab ===>"),
				set_lab(current_classroom, current_week_day, current_lecture, inputs_lectures, inputs_labs, yrs, mat, mat_list, q_avail_lab_list, q_avail_class_list)

		elif mat_list[current_classroom-1][current_week_day][current_lecture].is_lab == 0:
			print ("Trying to set lecture ===>"),
			set_lect(current_classroom, current_week_day, current_lecture, inputs_lectures, inputs_labs, yrs, mat, mat_list, q_avail_lab_list, q_avail_class_list)
		else:
			print ("Trying to set lab ===>"),
			set_lab(current_classroom, current_week_day, current_lecture, inputs_lectures, inputs_labs, yrs, mat, mat_list, q_avail_lab_list, q_avail_class_list)

	if current_classroom == 2:

		if mat_list[current_classroom-1][current_week_day][current_lecture] == -1:
			choice = random.randint(0,1)			
			if choice == 0 :
				print ("Trying to set lecture ===>"),
				set_lect(current_classroom, current_week_day, current_lecture, inputs_lectures, inputs_labs, yrs, mat, mat_list, q_avail_lab_list, q_avail_class_list)
			else:
				print ("Trying to set lab ===>"),
				set_lab(current_classroom, current_week_day, current_lecture, inputs_lectures, inputs_labs, yrs, mat, mat_list, q_avail_lab_list, q_avail_class_list)

		elif mat_list[current_classroom-1][current_week_day][current_lecture].is_lab == 0:
			print ("Trying to set lab ===>"),
			set_lab(current_classroom, current_week_day, current_lecture, inputs_lectures, inputs_labs, yrs, mat, mat_list, q_avail_lab_list, q_avail_class_list)
		else:
			print ("Trying to set lecture ===>"),
			set_lect(current_classroom, current_week_day, current_lecture, inputs_lectures, inputs_labs, yrs, mat, mat_list, q_avail_lab_list, q_avail_class_list)

def Classrooms(classroom , week_days , no_of_lectures , classlist):

	SY_A,SY_B,TY_A,TY_B = [],[],[],[]

	classes = ["SY(A)", "SY(B)", "TY(A)", "TY(B)"]

	avail_class_list = [204,205,402]
	avail_lab_list = [1,2,3]

	q_avail_class_list = Queue();
	q_avail_lab_list = Queue();

	for i in range(len(avail_class_list)):
		q_avail_class_list.put(avail_class_list[i])

	for i in range(len(avail_lab_list)):
		q_avail_lab_list.put(avail_lab_list[i])

	SY_A = classlist[0]
	SY_B = classlist[1]
	TY_A = classlist[2]
	TY_B = classlist[3]

	yrs = [SY_A, SY_B, TY_A, TY_B]

	mat_list = []

	for c in range(classroom):				# Creating Empty Tables
		mat = []
		for i in range(week_days):
			temp = []
			for j in range(no_of_lectures):
				if j in [5,8]:
					temp.append(00)
				elif j == 2:
					temp.append(-923)
				else:
					temp.append(-1)
			mat.append(temp)
		mat_list.append(mat)

	# teachers = Queue();
	# lab_teachers = Queue();

	for current_classroom in range(classroom):

		inputs_lectures = []
		inputs_labs = []
		#teachers.queue.clear()
		#lab_teachers.queue.clear()
		for current_lecture in range(len(yrs[current_classroom])):
			if yrs[current_classroom][current_lecture].is_lab == 0:
				inputs_lectures.append(yrs[current_classroom][current_lecture])

		#for k in xrange(len(inputs_lectures)):
		#	teachers.put(inputs_lectures[k])												# Queue for Lectures

		for current_lecture in range(len(yrs[current_classroom])):
			if yrs[current_classroom][current_lecture].is_lab == 1:
				inputs_labs.append(yrs[current_classroom][current_lecture])

		#for k in xrange(len(inputs_labs)):
		#	lab_teachers.put(inputs_labs[k])											# Queue for Lab

		mat = mat_list[current_classroom]

		for current_week_day in range(week_days):

			replinish_daily_count(current_classroom, week_days, yrs)

			for current_lecture in range(no_of_lectures):

				if mat[current_week_day][current_lecture] == -1 and current_lecture not in BREAKS:

					pick_next(current_classroom, current_week_day, current_lecture, inputs_lectures, inputs_labs, yrs, mat, mat_list, q_avail_lab_list, q_avail_class_list)
					if mat[current_week_day][current_lecture] == -1:
						print ("UNSET", current_week_day, current_lecture)
					else:
						print ("SET")

	for i in range(len(classlist)):
		cur_class = classlist[i]
		for j in cur_class:
			if j.weekly_count != 0:
				print ("Subject:", j.subject, "Weekly Count:", j.weekly_count, "IS LAB:", j.is_lab, "Year:", j.year)
				# assert(False)
	

	print_table(classroom, mat_list, week_days, no_of_lectures)
	checker(mat_list, week_days, no_of_lectures)
	return mat_list