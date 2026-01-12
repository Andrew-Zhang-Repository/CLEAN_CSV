# imports

import os, tempfile
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
import openai
import io


def summary(model_name, temperature, path, choice):
 

   
    uploaded_file = path 

    if uploaded_file is not None:


        llm = ChatOpenAI(model_name=model_name, temperature=temperature)

        agent = create_pandas_dataframe_agent(llm,path,verbose=True,allow_dangerous_code=True,agent_executor_kwargs={"handle_parsing_errors": True},handle_parsing_errors=True)

        result = None
      

        if choice == None:
            return None
        
        elif choice == "summary":


            result = agent.invoke("Give a summary of the csv file in less than 60 words. Do not take too long for time limit to hit though.")

        elif choice == "analysis":

            result = agent.invoke("Analyze the csv file in less than 60 words. Do not take too long for time limit to hit though.")

        elif choice == "scan":
            
            result = agent.invoke("Scan the csv file and spot any issues such as formatting, and other mistakes in less than 60 words. Do not take too long for time limit to hit though.")


        return result["output"]


# leave analysis to stats from qsv library

# drop down for model type so long as user has API KEY TOKENS LEELLEL
# summary(,0.0,"your_CSV_files/jobs.csv","analysis")



