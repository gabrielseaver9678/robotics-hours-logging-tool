import meetingsbase

def help_command ():
	print("""
=== HELP ===
del [meeting date] [meeting label]: Deletes a given meeting's record.
desc [meeting date] [meeting label]: Describes a meeting given its date and label.
   The date should be in the format mm-dd-yyyy.
edit [meeting date] [meeting label]: Edits a given meeting's record.
exit: Exits the interactive robotics hours prompt.
help: Displays this list of commands and their functionality.
hours [name]: Displays everyone's individual hours if no arguments are given,
   or one individual person's hours if a name is given as an argument.
log: Records information about a meeting.
meetings [name]: Provides a list of all the logged meetings dates and labels if no
   arguments are given, or all the meetings an individual person participated in if
   a name is given as an argument.
quit: Same as 'exit'.""")

def __accept_meeting_argument (args):
	# Check for correct number of arguments
	if len(args) != 2:
		print("Provide the date and meeting label as arguments.\nUse 'help' for further help with this command.")
		return None
	
	# Check for valid given date
	if not meetingsbase.is_valid_date(args[0]):
		print("'{} is not a valid date. Use the format mm-dd-yyyy.'".format(args[0]))
		return None
	args[1] = args[1].lower()
	
	# Gets the meeting
	meeting = meetingsbase.get_meeting(args[0], args[1])
	if meeting == None:
		print("No meeting was found with the given label and date. Please ensure your label and date are correct and try again.")
		return None
	
	return meeting

def describe_meeting_command (args):
	meeting = __accept_meeting_argument(args)
	if meeting == None:
		return
	
	# Describes the meeting
	meetingsbase.describe_meeting(meeting)

def log_command ():
	meetingsbase.create_meeting_entry()

def delete_command (args):
	meeting = __accept_meeting_argument(args)
	if meeting == None:
		return
	
	# Describes the meeting
	delete_meeting = meetingsbase.get_yes_no("Are you sure you want to delete the meeting from {} labeled as '{}'? ".format(meetingsbase.get_written_date(args[0]), args[1]))
	if delete_meeting:
		print("Okay. Deleting the meeting...")
		meetingsbase.delete_meeting(meeting)
	else:
		print("Okay. Not deleting the meeting.")

def edit_command (args):
	meeting = __accept_meeting_argument(args)
	if meeting == None:
		return
	
	meetingsbase.edit_meeting(meeting)
	
	if meetingsbase.get_yes_no("Save the changes made to this meeting? "):
		meetingsbase.save_meetings_data()
	else:
		print("Okay. Not saving changes.")

def __str_len (string: str, length: int):
	return string + " " * (length - len(string))

def hours_command (args):
	name = " ".join(args).strip().upper()
	mins_list = meetingsbase.get_all_mins()
	
	if name != "":
		for person in mins_list:
			if person["name"] == name:
				hours = int(person["mins"] / 60)
				mins = person["mins"] % 60
				print("{} hours, {} minutes".format(hours, mins))
				return
		print("No hours were found for a person named '{}'.".format(name))
	else:
		for person in mins_list:
			hours = int(person["mins"] / 60)
			mins = person["mins"] % 60
			print(__str_len(person["name"], 22) + "{} hours, {} minutes".format(hours, mins))

def list_meetings_command (args):
	name = " ".join(args).strip().upper()
	
	if name == "":
		meetingsbase.list_meetings()
	else:
		meetings = meetingsbase.get_persons_meetings(name)
		if len(meetings) == 0:
			print("The given person has not logged into any meetings.")
		else:
			meetingsbase.list_meetings(meetings=meetings, person=name)

# Receives user input, processes it, and outputs to the console. Returns False if the user uses the exit or quit command, True otherwise
def receive_input (user_in):
	# Get usable info from input
	input_parts = user_in.split(" ")
	command = input_parts[0]
	args = input_parts[1:]
	
	if command == "del":
		delete_command(args)
	elif command == "desc":
		describe_meeting_command(args)
	elif command == "edit":
		edit_command(args)
	elif command == "exit":
		return False
	elif command == "help":
		help_command()
	elif command == "hours":
		hours_command(args)
	elif command == "log":
		log_command()
	elif command == "meetings":
		list_meetings_command(args)
	elif command == "quit":
		return False
	else:
		print("Unknown command: '{}'. Use 'help' for a list of commands.".format(command))
	
	print("")
	return True

def start_console ():
	print("\nWelcome to the interactive robotics hours logging tool. Use 'help' for a list of commands.")
	receive_another_command = True
	while receive_another_command:
		receive_another_command = receive_input(input("> "))

if __name__ == "__main__":
	start_console()