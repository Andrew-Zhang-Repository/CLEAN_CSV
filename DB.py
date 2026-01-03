import psycopg2
import sys
import hash
import pytz
import os
# import cache
import time
import json
from datetime import datetime
from dotenv import load_dotenv

output_folder_text = "text_history"

load_dotenv("init.env")


host = os.getenv("POSTGRES_HOST")
db_name = os.getenv("POSTGRES_NAME")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
port = os.getenv("POSTGRES_PORT")


conn_string = f"host='{host}' dbname='{db_name}' user='{user}' password='{password}' port = {port}"


user_table = f'''CREATE TABLE IF NOT EXISTS Users(
	user_id SERIAL PRIMARY KEY,
	hash_type VARCHAR(20),
	pass_salt TEXT,
	email VARCHAR(100),
	password TEXT NOT NULL,
	date_joined DATE
	);
'''

file_table = '''
	CREATE TABLE IF NOT EXISTS File_info(
	file_id SERIAL PRIMARY KEY,
	user_id INTEGER NOT NULL, 
	file_name VARCHAR(80),
	file_size BIGINT,
	ai_text TEXT
	);
'''

def insert_user(email, password, option):


	query = '''INSERT INTO Users (hash_type, pass_salt, email, password, date_joined)
	VALUES (%s,%s,%s,%s,%s)
	RETURNING user_id;'''
	
	
	print("Connecting to database\n	->%s" %(conn_string))
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	
	if check_exists(email) == False:
		# alrdy exists
		return None
	
	load = hash.universal_hash(password,option)
	table_password = load[0]
	pass_salt = load[1]
	
	date = datetime.now(pytz.utc).strftime("%d/%m/%Y")
	data = (option, pass_salt, email, table_password,date)

	cursor.execute(query,data)

	id = cursor.fetchone()[0]

	conn.commit()
	conn.close()

	return id

def insert_file(id,path,text):

	query = '''INSERT INTO File_info (user_id, file_name, file_size, ai_text)
	VALUES (%s,%s,%s,%s)
	RETURNING file_name,file_size,ai_text, user_id;'''

	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()

	data = (id, path.strip("your_CSV_files/"), os.stat(path).st_size, text)
	cursor.execute(query,data)

	fetch = cursor.fetchone()

	redis_dic = {
		"file_name" : fetch[0],
		"file_size" : fetch[1],
		"ai_text" : fetch[2],
		"user_id" : str(fetch[3])
	}

	# cache.add_to_cache_files(redis_dic)
	

	conn.commit()
	conn.close()


	return 


def check_exists(email):

	
	
	query = f'''SELECT user_id 
		FROM Users
		WHERE email = '{email}' 
	'''
	
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	cursor.execute(query)

	result = cursor.fetchall()

	if result == []:
		# new user 
		return True
	
	return False
	


def log_on(email,password_attempt):

	query = f'''SELECT hash_type, pass_salt, password, user_id, date_joined
		FROM Users
		WHERE email = '{email}'
	'''

	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	cursor.execute(query)

	rows = cursor.fetchall()
	conn.close()

	outcome = None
	option = None
	salt = None
	pass_hash = None
	user_id = None
	date_joined = None

	if rows != []:
		# email found now check password

		load = rows[0]

		option = load[0]
		salt = load[1]
		pass_hash = load[2]
		user_id = load[3]
		date_joined = load[4]

		outcome = hash.universal_verify(password_attempt,pass_hash,salt,option)

	# user dictionary

	user_dic = {
		'email': email,
		'user_id': str(user_id),
		'date_joined' : date_joined
	}

	if outcome == True:
		# cache.add_to_cache(user_dic)
		return user_id

	return None

"""def get_all_cached_files(user_id):

    key = f"file_data_user:{user_id}"
    encoded_files = cache.r.lrange(key, 0, -1)
    decoded_files = [json.loads(f) for f in encoded_files]
    
    return decoded_files
"""

def get_user_files(id):

	
	query = f'''SELECT file_name, file_size, ai_text
		FROM File_info
		INNER JOIN Users
		ON File_info.user_id = Users.user_id
		where File_info.user_id = {id}
	'''

	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	cursor.execute(query)

	vector = cursor.fetchall()

	"""if get_all_cached_files(id) != []:
		get_text(get_all_cached_files(id),"redis")
	else:
		get_text(vector,None)
	"""
	
	conn.close()

	return vector 

def init_tables():

	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	cursor.execute(user_table)
	cursor.execute(file_table)
	conn.commit()

	# do one for files

def get_text(arr,option):

	if arr == []:
		return None

	
	content_blocks = []
	if option == "redis":
		

		counter = 0
		for i in arr:
			
			file_name = i["file_name"]
			file_size = i["file_size"]
			ai_text = i["ai_text"]

			content_blocks.append(f"submission{counter} \n file_name: {file_name}, file_size: {file_size} \nai_text: \n{ai_text}\n\n")

			counter+=1

	else:
		content_blocks = [f"submission{i} \n {''.join(map(str,"file_name: " + item[0])) + ''.join(map(str,", file_size: " + str(item[1]))) +  ''.join(map(str," \nai_text: \n" + item[2]))}\n\n" for i, item in enumerate(arr)]

	all_content = "".join(content_blocks)

	with open(f"{output_folder_text}/ai_text.txt{time.time()}",'w') as file:
		file.write(all_content)

	return None

init_tables()

# get_text([('',), ('GROWTOPIA GG',), ('GROWTOPIA GG',)])



# get_user_files(3)



# insert_user("brian@gmail.com","fella","sha512")

# insert_user("andrew@gmail.com","fella","sha256")

# insert_user("daniel@gmail.com","fella","argon2")

# log_on("andrew@gmail.com","fella")

"""GENERAL LOGIC: LET USERS USE THE WEB APP, UPON COMPLETION (MAYBE COUNT LIKE 6-7 COMPLETIONS) AND AFTER
EACH CYCLE PING TO USER IF THEY WANT AN ACCOUNT, IF YES THING KEEP USER DETAILS AND THEN KEEP THERE JUST
LOGGED CSV FILE DATA IN THE FILES TABLE. ELSE LET USER HAVE ACCESS TO EVERYTHING BUT THEIR USER DATA
AND FILE DATA WILL NOT BE STORED IN DB"""

# add remove duplicate email functionality