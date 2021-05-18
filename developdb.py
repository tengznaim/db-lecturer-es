import json

with open('db.json') as f:
	data = json.load(f)

data = data['What do you want to know about Database subject?']['I want to develop a database']

db_rules = []
db_rules.extend(dict(rule=rule) for rule in data['sql']) 
db_rules.extend(dict(rule=rule) for rule in data['nosql']) 

print('Type Y for yes, N for no, nothing for not concern.')
for rule in db_rules:
	rule['ans'] = input(f'{rule["rule"]} :')

result_db = None
for rule in db_rules:
	if rule['ans'] == 'Y':
		if rule['rule'] in data['sql']:
			if result_db is None:
				result_db = 'sql'
			elif result_db != 'sql':
				result_db = 'Not valid'
				break
		else:
			if result_db is None:
				result_db = 'nosql'
			elif result_db != 'nosql':
				result_db = 'Not valid'
				break
	elif rule['ans'] == 'N':
		if rule['rule'] in data['sql']:
			if result_db is None:
				result_db = 'nosql'
			elif result_db == 'sql':
				result_db = 'Not valid'
				break
		else:
			if result_db is None:
				result_db = 'sql'
			elif result_db == 'nosql':
				result_db = 'Not valid'
				break

print(result_db)
