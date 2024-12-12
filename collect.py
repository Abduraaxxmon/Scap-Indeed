import time

import pandas as pd
import os



def collect_into_dataframe(name_companies, job_titles, location_jobs, post_dates, skills, logo_urls,country,job,salary_list):
    country_list = [country] * len(name_companies)
    job_title_from_list=[job]*len(name_companies)
    sourses= ["indeed.com"]*len(name_companies)
    # ID,Posted_date,Job Title from List,Job Title,Company,Company Logo URL,Country,Location,Skills,Salary Info,Source
    data = {
        "id":range(1,len(name_companies)+1),
        "Posted_date": post_dates,
        "Job Title from List": job_title_from_list,
        "Job Title": job_titles,
        "Company": name_companies,
        "Company Logo URL": logo_urls,
        "Country": country_list,
        "Location": location_jobs,
        "Skills": skills,
        "Salary Info": salary_list,
        "Source": sourses,
    }

    # Convert the dictionary into a DataFrame
    df = pd.DataFrame(data)
    file_name_skills = f"{job} skills"
    create_skills_cross_join_csv(jobs_df=df, file_name=file_name_skills,folder_name="Skills data")

    return df




def save_dataframe_to_csv(df, file_name, folder_name="data"):
    try:

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        file_name_csv=f"{file_name}.csv"
        # Construct the full file path
        file_path = os.path.join(folder_name, file_name_csv)

        # Save the DataFrame to the specified path
        df.to_csv(file_path, index=False)
        print(f"DataFrame successfully saved to {file_path}")

    except Exception as e:
        print(f"An error occurred while saving the DataFrame: {e}")



def create_skills_cross_join_csv(jobs_df, file_name, folder_name="data"):

    try:
        # Prepare an empty list for the expanded rows
        expanded_rows = []

        # Iterate over each job row
        for _, row in jobs_df.iterrows():
            skills_list = row['Skills'].split(', ')  # Split skills string into a list
            for skill in skills_list:
                expanded_row = {
                    "Posted_date": row["Posted_date"],
                    "Job Title": row["Job Title from List"],
                    "Country": row["Country"],
                    "Company": row["Company"],
                    "Skill": skill
                }
                expanded_rows.append(expanded_row)

        # Convert the expanded rows into a DataFrame
        expanded_df = pd.DataFrame(expanded_rows)

        # Save the expanded DataFrame to a CSV file
        save_dataframe_to_csv(expanded_df, file_name, folder_name)
    except Exception as e:
        print(f"An error occurred during the skills cross-join process: {e}")

# Function to translate text to English


def to_one_csv():
    # Define the directory where the CSV files are located
    input_directory = r"E:\forCoding\pycharm\indeed\Skills data"
    output_file = r"E:\forCoding\pycharm\all_data_skills.csv"

    # Initialize an empty list to store dataframes
    dataframes = []

    # Iterate through all files in the directory
    for file in os.listdir(input_directory):
        if file.endswith(".csv"):
            file_path = os.path.join(input_directory, file)
            # Read each CSV file into a DataFrame
            df = pd.read_csv(file_path)
            dataframes.append(df)

    # Concatenate all dataframes into one
    merged_df = pd.concat(dataframes, ignore_index=True)
    if 'id' in merged_df.columns:
        merged_df = merged_df.drop('id', axis=1)

    # Save the merged dataframe to a new CSV file
    merged_df.to_csv(output_file, index=False,na_rep="NA")

    print(f"Merged {len(dataframes)} files into {output_file}")


# Call the function

