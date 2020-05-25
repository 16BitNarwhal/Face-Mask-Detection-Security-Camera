from os import path

while True:
	print("Day (YYYY-MM-DD): ")
	inp = raw_input()
	script_dir = path.dirname(__file__)
	rel_path = "logs/" + inp + ".txt"
	file_dir = path.join(script_dir, rel_path)
	try:
		file_log = open(file_dir, 'r')
		content = file_log.read()
		print(content)
		file_log.close()
	except IOError:
		print("No files from " + inp + "\n")
