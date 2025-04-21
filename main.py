# main.py
import warnings
warnings.filterwarnings("ignore")

from data_loader import load_csv_from_url, clean_unamerican_data, clean_american_data1, clean_american_data2
from control_flow import run_analysis_session, ask_restart
import pandas as pd


Beer_text = "\033[32m\033[1m"
Jon_text = "\033[31m\033[1m"
Zak_text = "\033[34m\033[1m"
UNDER = "\033[4m"
RESET = "\033[0m"

def Beer_List():
    print()
    print(f"{Beer_text}{UNDER}Welcome to the Beer List Analysis Platform!{RESET}\n"
          "\n"
          "We're dealing with a lot of data. Please be patient;\n"
          "it might take a minute to load.\n")


    # URLs for the datasets
    url_unAm = "https://docs.google.com/spreadsheets/d/1W4F-UwW8jNdw9ZjL0hf_P53m6BWKU9Xszwt0a2TiyFU/export?format=csv&gid=0"
    url_Am1 = "https://docs.google.com/spreadsheets/d/1W4F-UwW8jNdw9ZjL0hf_P53m6BWKU9Xszwt0a2TiyFU/export?format=csv&gid=1"
    url_Am2 = "https://docs.google.com/spreadsheets/d/1W4F-UwW8jNdw9ZjL0hf_P53m6BWKU9Xszwt0a2TiyFU/export?format=csv&gid=2"

    # Load datasets
    Unamerican = load_csv_from_url(url_unAm)
    Am1_data = load_csv_from_url(url_Am1)
    Am2_data = load_csv_from_url(url_Am2)

    # Get beer totals
    total_total = int(Unamerican["Beer"].iloc[-1])
    Zak_total = int(Unamerican["Zak"].iloc[-1].replace(",", ""))
    Jon_total = int(Unamerican["Jon"].iloc[-1].replace(",", ""))

    # Clean datasets
    Unamerican = clean_unamerican_data(Unamerican)
    Am1_data = clean_american_data1(Am1_data)
    Am2_data = clean_american_data2(Am2_data)

    # Combine datasets
    American = pd.concat([Am1_data, Am2_data], axis=0)
    All = pd.concat([Unamerican, Am1_data, Am2_data], axis=0)

    print(f"There are currently {Beer_text}{total_total:,}{RESET} beers on the list.\n"
          f"{Jon_text}Jon{RESET} has had {Jon_text}{Jon_total:,}{RESET} beers, and {Zak_text}Zak{RESET} has had {Zak_text}{Zak_total:,}{RESET}.\n")
    input("Press any key and hit enter to continue: ")
    print()

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