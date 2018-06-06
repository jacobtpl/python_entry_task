import csv
USERNAMES = []
PASSWORDS = []
with open('userpass.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		USERNAMES.append(row['username'])
		PASSWORDS.append(row['password'])
print('init done')
