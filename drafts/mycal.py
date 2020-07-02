today = datetime.datetime(2020,6,26)

today.get_weekday()



from cryptography.fernet import Fernet
key = Fernet.generate_key() #this is your "password"
cipher_suite = Fernet(key)
encoded_text = cipher_suite.encrypt(b"Hello stackoverflow!")
decoded_text = cipher_suite.decrypt(encoded_text)


a = "/Users/karlzipser/Library/Mobile\ Documents/com\~apple\~CloudDocs/constitution.pdf"

os.system("open "+a)



def check_date_validity(day,month,year,hour,minute):
	return True


def Event(
	day,
	month,
	year,
	hour,
	minute,
	title_str,
	description_str,
	category,priority
):
	D = {
		'day':day,
		'month':month,
		'hour':hour,
		'minute':minute,
		'title_str':title_str,
		'description_str':description_str,
		'category':category,
		'priority':priority,
	}

	if not is_valid_date(day,month,year,hour,minute):
		return False

	def __save():
		pass



