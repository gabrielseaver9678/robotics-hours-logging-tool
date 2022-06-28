import json, re

__meetings_file = "meetings.json"

__meetings = []

__months = [
	"January",
	"February",
	"March",
	"April",
	"May",
	"June",
	"July",
	"August",
	"September",
	"October",
	"November",
	"December",
]

has_loaded_data = False
def __meeting_sort_date_func (meeting):
	date = meeting["date"].split("-")
	month = int(date[0])
	day = int(date[1])
	year = int(date[2])
	return year * 10000 + month * 100 + day

def __organize_meetings_data ():
	global has_loaded_data
	if not has_loaded_data:
		has_loaded_data = True
		__load_meetings_data()
	
	__meetings.sort(key=__meeting_sort_date_func)

def __load_meetings_data ():
	global __meetings
	
	with open(__meetings_file, "r") as file:
		__meetings = json.load(file)

def save_meetings_data ():
	print("Saving meetings data...")
	with open(__meetings_file, "w") as file:
		json.dump(__meetings, file)
	print("Saved successfully.")

def is_valid_date (string: str):
	# Valid date: m-dd-yy
	return re.match(r"([1-9]|1[0-2])-([12]?[0-9]|3[01])-(20[0-9][0-9])$", string)

def is_valid_time (string: str):
	# Valid time: [1-12]:[0-59] am/pm
	return re.match(r"([1-9]|1[0-2]):[0-5][0-9] [ap]m$", string)

def get_meeting_date ():
	# Keep trying to get a valid meeting date until one is obtained
	meeting_date = input("Meeting date: (mm-dd-yyyy) ")
	while not is_valid_date(meeting_date):
		print("Invalid meeting date. Try again.")
		meeting_date = input("Meeting date: (mm-dd-yyyy) ")
	return meeting_date

def get_valid_time (prompt: str):
	# Keep trying to get a valid time until one is obtained
	time_answer = input(prompt)
	while not is_valid_time(time_answer):
		print("Invalid time. Try again using the format of '1:23 pm'.")
		time_answer = input(prompt)
	return time_answer

def get_integer (prompt: str):
	num = input(prompt)
	while not num.isdigit():
		print("Invalid integer. Try again.")
		num = input(prompt)
	return int(num)

def get_yes_no (prompt: str):
	ans = input(prompt).lower().strip()
	while ans != "yes" and ans != "no":
		print("Invalid answer. Try again, answering 'yes' or 'no'.")
		ans = input(prompt)
	return ans == "yes"

# Gets one person's hours information for the meeting
def __get_individual_info ():
	return {
		"name" : input("Name: ").upper().strip(),
		"login" : get_valid_time("Log in time: "),
		"logout" : get_valid_time("Log out time: "),
	}

# Gets the name for a meeting
def __get_meeting_label ():
	# If the meeting was general-purpose, don't give a special name
	was_general_meeting = get_yes_no("Was this a general-purpose meeting? ")
	if was_general_meeting:
		return "general-purpose"
	
	# Otherwise, get the name for the meeting
	return input("In that case, what was the purpose of the meeting? ").lower().strip().replace(" ", "-")

def get_written_date (date):
	date_parts = date.split("-")
	month = __months[int(date_parts[0])-1]
	day = int(date_parts[1])
	year = int(date_parts[2])
	return "{} {}, {}".format(month, day, year)

# Gets all the info about a meeting
# Usage note: this may return None if the user decides to stop logging the meeting
def __get_meeting_entry ():
	# Get and display meeting date
	meeting_date_confirmed = False
	meeting_date = None
	while not meeting_date_confirmed:
		meeting_date = get_meeting_date()
		meeting_date_confirmed = get_yes_no("Confirm: the meeting was on {}? ".format(get_written_date(meeting_date)))
		print("")
	
	meeting_label = __get_meeting_label()
	print("")
	
	if get_meeting(meeting_date, meeting_label) != None:
		print("A meeting on {} already exists with the label '{}'.".format(get_written_date(meeting_date), meeting_label))
		print("It is possible you have already logged the hours from this meeting.")
		print("Delete the old meeting from the record or try again with a different meeting label.")
		return None
	
	# Get number of people present at the meeting
	num_people = get_integer("Number of people at the meeting: ")
	
	# Keep getting individual people's hours until we have everyone 
	people = []
	while len(people) < num_people:
		people.append(__get_individual_info())
		print("")
	
	# Edit the meeting info
	meeting = { "date" : meeting_date, "label" : meeting_label, "people" : people }
	edit_meeting(meeting)
	
	return meeting

def __receive_edit_meeting_input (meeting, user_in):
	if user_in == "edit":
		name = input("Name: ").strip().upper()
		for person in meeting["people"]:
			if person["name"] == name:
				meeting["people"].remove(person)
				print("\nEDITING {}'S ENTRY".format(name))
				meeting["people"].append(__get_individual_info())
				return True
		print("A person by that name did not log into the meeting.")
	elif user_in == "add":
		print("\nADDING A NEW PERSON")
		meeting["people"].append(__get_individual_info())
	elif user_in == "del":
		name = input("Name: ").strip().upper()
		for person in meeting["people"]:
			if person["name"] == name:
				print("\nDELETED {}'S ENTRY".format(name))
				meeting["people"].remove(person)
				return True
		
		print("A person by that name did not log into the meeting.")
	elif user_in == "done":
		return False
	else:
		print("Invalid option. Use 'edit', 'add', 'del', or 'done' if you are finished.")
	return True

def __edit_meeting_redisplay_info (meeting):
	print("Meeting Hours:")
	for person in meeting["people"]:
		print(__str_len(person["name"], 22) + " {} - {}".format(person["login"], person["logout"]))
	print("")

def edit_meeting (meeting):
	__edit_meeting_redisplay_info(meeting)
	
	print("Use 'edit' to edit a person's information in the meeting,")
	print("'add' to add a new person for the meeting, or 'del' to delete")
	print("a person's information from the meeting. Use 'done' when you")
	print("are finished editing the meeting record.")
	
	continue_editing = __receive_edit_meeting_input(meeting, input("edit> "))
	while continue_editing:
		print("\n")
		__edit_meeting_redisplay_info(meeting)
		print("Use 'edit', 'add', 'del', or 'done'.")
		continue_editing = __receive_edit_meeting_input(meeting, input("edit> "))

def create_meeting_entry ():
	global __meetings
	
	# Get meeting data and stop running if the user didn't complete it
	meeting = __get_meeting_entry()
	print("")
	if meeting == None:
		return
	
	# Ensure the user wants to save the meeting data
	should_save = get_yes_no("Save the given meeting data? ")
	if should_save:
		__organize_meetings_data()
		__meetings.append(meeting)
		save_meetings_data()
	else:
		print("Ok. Not saving the meeting data.")

# Adds spaces to the end of a string to make it a given length
def __str_len (string: str, length: int):
	return string + " " * (length - len(string))

# Lists all meetings in the console
def list_meetings (meetings=None):
	__organize_meetings_data()
	if meetings == None:
		meetings = __meetings
	print("==== MEETINGS LIST ====")
	print(__str_len("DATE", 11) + "| LABEL")
	for meeting in meetings:
		print(__str_len(meeting["date"], 11) + "| " + meeting["label"])
	print("Total: {} meetings".format(len(meetings)))

def get_persons_meetings (name):
	meetings = []
	for meeting in __meetings:
		for person in meeting["people"]:
			if person["name"] == name:
				meetings.append(meeting)
				break
	return meetings

# Gets a meeting from the list given a date and label. Returns None if no meeting with given date and label is found.
def get_meeting (meeting_date, meeting_label):
	__organize_meetings_data()
	for meeting in __meetings:
		if meeting["date"] == meeting_date and meeting["label"] == meeting_label:
			return meeting
	return None

def describe_meeting (meeting):
	print("Meeting was on {}, labeled '{}'.".format(get_written_date(meeting["date"]), meeting["label"]))
	print("There were {} people who logged in during the meeting:\n".format(len(meeting["people"])))
	
	print(__str_len("NAME", 22) + " | LOG-IN TIME | LOG-OUT TIME")
	print("="*53)
	for person in meeting["people"]:
		print(__str_len(person["name"], 22) + " | " + __str_len(person["login"], 11) + " | " + person["logout"])

def __time_to_mins (time: str):
	# Get useful info from the time string
	time_parts = time.split()
	hours_mins = time_parts[0].split(":")
	hour = int(hours_mins[0])
	mins = int(hours_mins[1])
	is_pm = time_parts[1].lower() == "pm"
	
	# Account for the fact that 12:00 am is really 0:00 am and 12:00 pm is really 0:00 pm
	if hour == 12:
		hour = 0
	
	# Get minutes since midnight
	mins_since_midnight = hour * 60 + mins
	if is_pm:
		mins_since_midnight += 12 * 60
	
	return mins_since_midnight

def delete_meeting (meeting):
	global __meetings
	
	__organize_meetings_data()
	if meeting != None:
		# Remove the meeting and return it
		__meetings.remove(meeting)
		save_meetings_data()
		return meeting
	else:
		return None

# Gets the number of hours a person was logged in for at a meeting
def get_mins (person):
	return __time_to_mins(person["logout"]) - __time_to_mins(person["login"])

def get_all_mins ():
	mins_dict = {}
	
	__organize_meetings_data()
	for meeting in __meetings:
		for person in meeting["people"]:
			if person["name"] in mins_dict.keys():
				mins_dict[person["name"]] += get_mins(person)
			else:
				mins_dict[person["name"]] = get_mins(person)
	
	mins_list = []
	for name, mins in mins_dict.items():
		mins_list.append({"name" : name, "mins" : mins})
	
	mins_list.sort(key=lambda person: -person["mins"])
	
	return mins_list