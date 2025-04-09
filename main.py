# main.py
import warnings
warnings.filterwarnings("ignore")

from data_loader import load_csv_from_url, clean_unamerican_data, clean_american_data1, clean_american_data2
from control_flow import run_analysis_session, ask_restart
import pandas as pd

def Beer_List():
    # Initial welcome message and prompt
    print("Welcome to the Beer List Analysis Platform!\n"
          "\n"
          "Note, for tests that ask what variable you want to use, choices are:\n"
          "\"Territory,\" \"Brewery,\" \"Beer,\" \"Zak,\" \"Jon,\" \"Had,\" \"Style,\" \"ABV,\" and \"SRC.\"\n"
          "Depending on the analysis, some of these variables will not work.\n"
          "Please be patient. You are working with a lot of data. It takes a minute to load.\n")
    input("Press any key and hit enter to continue. ")

    # URLs for the datasets
    url_unAm = "https://docs.google.com/spreadsheets/d/1W4F-UwW8jNdw9ZjL0hf_P53m6BWKU9Xszwt0a2TiyFU/export?format=csv&gid=0"
    url_Am1 = "https://docs.google.com/spreadsheets/d/1W4F-UwW8jNdw9ZjL0hf_P53m6BWKU9Xszwt0a2TiyFU/export?format=csv&gid=1"
    url_Am2 = "https://docs.google.com/spreadsheets/d/1W4F-UwW8jNdw9ZjL0hf_P53m6BWKU9Xszwt0a2TiyFU/export?format=csv&gid=2"

    # Load datasets
    Unamerican = load_csv_from_url(url_unAm)
    Am1_data = load_csv_from_url(url_Am1)
    Am2_data = load_csv_from_url(url_Am2)

    # Clean datasets
    Unamerican = clean_unamerican_data(Unamerican)
    Am1_data = clean_american_data1(Am1_data)
    Am2_data = clean_american_data2(Am2_data)

    # Combine datasets
    American = pd.concat([Am1_data, Am2_data], axis=0)
    All = pd.concat([Unamerican, Am1_data, Am2_data], axis=0)

    data_options = {"Unamerican": Unamerican, "American": American, "All": All}
    data_choice = input("What Beer List data would you like to analyze?\n"
                        "Options are \"Unamerican,\" \"American,\" and \"All.\"\n"
                        "Your choice: ")
    while data_choice not in data_options:
        print("Invalid input.")
        data_choice = input("What Beer List data would you like to analyze?\n"
                            "Options are \"Unamerican,\" \"American,\" and \"All.\"\n"
                            "Your choice: ")
    path = data_options[data_choice]

    # Run analysis session and restart if needed
    from control_flow import run_analysis_session, ask_restart
    run_analysis_session(path)
    decision = ask_restart()
    if decision == "restart":
        Beer_List()
    else:
        exit()

if __name__ == "__main__":
    Beer_List()

#NONESENSE