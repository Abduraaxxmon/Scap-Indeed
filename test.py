import pandas as pd
import os


def to_one_csv():
    input_directory = r"E:\forCoding\pycharm\indeed\pythonProject1\2024-12-11 data"
    output_file = r"E:\forCoding\pycharm\indeed\pythonProject1\2024-12-11 all data.csv"

    dataframes = []
    for file in os.listdir(input_directory):
        if file.endswith(".csv"):
            file_path = os.path.join(input_directory, file)
            df = pd.read_csv(file_path)

            # Drop the old 'ID' column if it exists
            if 'ID' in df.columns:
                df.drop('id', axis=1, inplace=True)

            dataframes.append(df)
    # if 'id' in merged_df.columns:
    #     merged_df = merged_df.drop('id', axis=1)
    # Concatenate all dataframes with ignore_index=True to get a new continuous index
    merged_df = pd.concat(dataframes, ignore_index=True)

    # Save the merged DataFrame to a CSV, with a new index starting from 1
    merged_df.index += 1  # Shift index to start from 1
    merged_df.drop("id", axis=1, inplace=True)
    merged_df.to_csv(output_file, index=True, index_label='ID', na_rep="NA")
    print(f"Merged {len(dataframes)} files into {output_file}")


import os
import re

def save_dataframe_to_csv(dataframe, file_name, folder_name):
    """Save a DataFrame to a CSV file in the specified folder."""
    os.makedirs(folder_name, exist_ok=True)  # Ensure the folder exists
    file_path = os.path.join(folder_name, file_name)
    dataframe.to_csv(file_path, index=False)
    print(f"DataFrame saved successfully to {file_path}")


def read_and_expand_jobs_csv(folder_name="data_skills"):

    input_file_path = r"E:\forCoding\pycharm\indeed\pythonProject1\2024-12-11 all data.csv"
    output_file_name = r"E:\forCoding\pycharm\indeed\pythonProject1\data_skills.csv"

    try:
        # Read the CSV file
        jobs_df = pd.read_csv(input_file_path)

        expanded_rows = []

        # Iterate over each job row
        for _, row in jobs_df.iterrows():
            # Check if 'Skills' exists and is not NaN
            if pd.notna(row.get('Skills')):
                # Use regex to split on ',' followed by any amount of whitespace
                skills_list = re.split(r',\s*', str(row['Skills']).replace('amp;', ''))
                for skill in skills_list:
                    expanded_row = {
                        "Posted_date": row["Posted_date"],
                        "Job Title from List": row.get("Job Title from List", ""),  # Using "Job Title" column directly
                        "Country": row["Country"],
                        "Company": row["Company"],
                        "Skill": skill.strip()  # Remove any leading/trailing whitespace
                    }
                    expanded_rows.append(expanded_row)

        # Convert the expanded rows into a DataFrame
        expanded_df = pd.DataFrame(expanded_rows)

        # Save the expanded DataFrame to a CSV file
        save_dataframe_to_csv(expanded_df, output_file_name, folder_name)

    except Exception as e:
        print(f"An error occurred while processing the CSV file: {e}")


# Example usage, assuming you have a DataFrame 'jobs_df' ready
# create_skills_cross_join_csv(jobs_df, "cross_joined_skills.csv")
read_and_expand_jobs_csv()