--- 
### CLEAN_CSV

#### Summary
Input a csv file, choose to scan, analyse , scan for issues or all at once with langchain agents. And gives out a cleaned output of the CSV file.


---
#### Pre-requisites
Add google Oauth keys to ./streamlit/secrets.toml file, and change whatever is needed to environment files to fit your Postgres and Redis DBs. Also obtain an openai key in order for the agents to run. If no keys login, ai function is not available but default file cleaning is.

---
#### App Installation
```bash
Run these commands:

# RECOMMENDED 
docker compose up --build

# OR RUN LOCALLY (VERY TEDIOUS)

pip install -r requirements.txt
# Turn on postgres DB and redis DB
streamlit run main.py

```


---

#### General Information and Usage:
- AI models is hard coded to be openai gpt 4 mini for optimal speed, but users are free to change it to any.

- A lot of password hashing functions are availble besides current sha256 used in code, which are usable so more features can be extended/added to the user's will.

---

#### Image Examples
--- 


![Web page with no login or input](https://github.com/user-attachments/assets/7d396478-2f26-48d9-998f-5335c9e75cbc)
*Web page with no login or input*

![Web page with login but no input](https://github.com/user-attachments/assets/207f6f4c-f350-498f-a9e7-95a1e25809a6)
*Web page with login but no input*

![User info and history retrieval](https://github.com/user-attachments/assets/f649fc04-e748-4cad-ab14-88b330ca1dbf)
*User info and history retrieval*

![Process ran with no login](https://github.com/user-attachments/assets/0a2f132b-982b-43de-88f8-d0b8962379cb)
*Process ran with no login*

![Process ran with login](https://github.com/user-attachments/assets/a450f833-07e1-4ba5-93d4-f6ef0b3f7f38)
*Process ran with login*





