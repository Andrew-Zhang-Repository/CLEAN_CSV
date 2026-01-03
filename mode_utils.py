# imports

import os, tempfile
import pandas as pd
from langchain_openai import ChatOpenAI

import openai


def summary(model_name, temperature, path, choice):
 

    # replace to path of csv file since we ignoring frontend 
    uploaded_file = path 

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        if len(df) > 50 :
            df = pd.read_csv(uploaded_file, nrows=50)

            # just summarise the first a 50 rows
      
        text = df.to_string()

        llm = ChatOpenAI(model_name=model_name, temperature=temperature)

        if choice == None:
            return None
        
        elif choice == "summary":


            final_prompt = f"Put the following text into a single concise summary in less than 60 words:\n\n{text}"
            result = llm.invoke(final_prompt)

        elif choice == "analysis":

            final_prompt = f"Analysis the following dataset/text in less than 60 words:\n\n{text}"
            result = llm.invoke(final_prompt)

        elif choice == "scan":
            
            final_prompt = f"Find issues within the dataset in less than 60 words:\n\n{text}"
            result = llm.invoke(final_prompt)



        return result.content

# leave analysis to stats from qsv library

# drop down for model type so long as user has API KEY TOKENS LEELLEL
# summary("gpt-4o-mini",0.0,"your_CSV_files/jobs.csv","analysis")
