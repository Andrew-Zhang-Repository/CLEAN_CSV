
from cleaner import trim
import pandas as pd
import time
import os
import argparse
import mode_utils
import DB

OUTPUT_FOLDER = "output_CSV"
DIFF_FOLDER = "diff_folder"
 
def main():

    parser = argparse.ArgumentParser(prog = "CSV Cleaner",description = "Cleans csvs with other added functions")

    parser.add_argument("-path","--path",required = True,type = str)
    parser.add_argument("-clean","--clean",required = False, type = bool)
    parser.add_argument("-mode","--mode", required = False, type = str)
    parser.add_argument("-diff","--diff", required = False, type = bool)
    parser.add_argument("-analysis","--analysis", required = False, type = bool)
    parser.add_argument("-summary","--summary", required = False, type = bool)
    parser.add_argument("-scan","--scan", required = False, type = bool)

    args = parser.parse_args()

    # unused shit make sure its used later  IMPORTANT IMPORTANT DONT FORGET
    mode = args.mode
    path = args.path
    clean = args.clean
    diff = args.diff
    analysis = args.analysis
    summary = args.summary
    scan = args.scan

    # Ai stuff here

    ai_text = get_ai_modes(analysis,summary,scan,path)

    
    
    # save headers before trimming
    df = pd.read_csv(path)
    header = df.columns
    header_list = header.tolist()
   
    trimmed = trim.clean_up_and_trim(path)
    trimmed.drop_duplicates()
    trimmed.columns = header_list


    # Remove trailing whitespaces
    for col in trimmed.columns:
        if trimmed[col].dtype == object:  
            trimmed[col] = trimmed[col].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)

    

    curr_time = time.time()
    file_name = "output"+str(curr_time)+".csv"
    output_file = os.path.join(OUTPUT_FOLDER, file_name)
    trimmed.to_csv(output_file, index=False)

    if diff == True:
        
        diff_time = time.time()
        diff_output = os.path.join(DIFF_FOLDER, "diff_output"+str(diff_time)+".csv") 
        os.popen(f"qsv diff {path} {output_file} --output {diff_output}")

    time.sleep(5)

    for i in os.listdir(OUTPUT_FOLDER):
        if i.endswith((".stats.csv.json",".stats.csv.data.jsonl",".stats.csv")):
            os.remove(os.path.join(OUTPUT_FOLDER,i))
    


    # if not logged in, if logged in based on front end shit

    """logged = DB.log_on("daniel@gmail.com","fella")
   

    if logged != None:

        # append to file table
        # DB.insert_file(logged,path,"GROWTOPIA GG")

        print(DB.get_user_files(logged))
    """


    

    return None


def get_ai_modes(analysis,summary,scan,path):

    return_str = ""

    if analysis != None:
        return_str += "ANALYSIS: \n\n" + mode_utils.summary("gpt-4o-mini",0.0,path,"analysis") + "\n\n"

    if summary != None:
        return_str += "SUMMARY: \n\n" + mode_utils.summary("gpt-4o-mini",0.0,path,"summary") + "\n\n"

    if scan != None:
        return_str += "SCAN: \n\n" + mode_utils.summary("gpt-4o-mini",0.0,path,"scan") + "\n\n"

    return return_str

if __name__ == "__main__":
    DB.init_tables()
    main()

    # Add sort arg and connect with the ai stuff and then add DB stuff

    



