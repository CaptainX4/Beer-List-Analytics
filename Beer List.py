import certifi
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import ssl
import urllib.request as urllib2
import warnings
warnings.filterwarnings("ignore")
from io import StringIO

def Beer_List():
    # Define allowed variable options
    var_options = ["Territory", "Brewery", "Beer", "Zak", "Jon", "Had", "Style", "ABV", "SRC"]

    # Generic input validation helper
    def get_valid_input(prompt, valid_options):
        response = input(prompt)
        while response not in valid_options:
            print("Invalid input.\n")
            response = input(prompt)
        return response

    # Refactored query functions using get_valid_input
    def query(n):
        """
        n == 1: Asks for a single variable to test.
        n == 2: Asks for the X axis variable for a two-variable test.
        n == 3: Asks for a drinker (Jon or Zak) for testing against a variable.
        """
        if n == 1:
            return get_valid_input("What variable would you like to test? ", var_options)
        elif n == 2:
            print("What two variables would you like to test?\n"
                  "Options are \"Territory,\" \"Brewery,\" \"Beer,\" \"Zak,\" \"Jon,\" \"Had,\" \"Style,\" \"ABV,\" and \"SRC.\"")
            return get_valid_input("X axis variable: ", var_options)
        elif n == 3:
            print("Pick a drinker (Jon or Zak) and a variable you'd like to test against.\n"
                  "Options are \"Territory,\" \"Brewery,\" \"Beer,\" \"Style,\" \"ABV,\" and \"SRC.\"")
            return get_valid_input("Who's drinking? ", var_options)

    def query_2(m):
        """
        m == 1: Asks for the Y axis variable.
        m == 2: Asks for the variable to test.
        """
        if m == 1:
            return get_valid_input("Y axis variable: ", var_options)
        elif m == 2:
            return get_valid_input("Variable to test: ", var_options)

    print("Welcome to the Beer List Analysis Platform!\n"
          "\n"
          "Note, for tests that ask what variable you want to use, choices are:\n"
          "\"Territory,\" \"Brewery,\" \"Beer,\" \"Zak,\" \"Jon,\" \"Had,\" \"Style,\" \"ABV,\" and \"SRC.\"\n"
          "Depending on the analysis, some of these variables will not work.\n"
          "Please be patient. You are working with a lot of data. It takes a minute to load.")
    print()

    start = input("Press any key and hit enter to continue. ")
    if len(start) == 0:
        print()
    else:
        pass

    # ------------------------------
    # Data Loading and Cleaning
    # ------------------------------

    # Data Loading Helper Function
    def load_csv_from_url(url):
        context = ssl.create_default_context(cafile=certifi.where())
        data = urllib2.urlopen(url, context=context).read()
        data_str = data.decode("utf-8")
        return pd.read_csv(StringIO(data_str))
    
    # Data Cleaning Functions
    def clean_unamerican_data(df):
        cleanup_columns = ["Comments", "Country Total", "Zak Total", "Jon Total", "Maps Link"]
        df = df.drop(cleanup_columns, axis=1)
        # Exclude rows with unwanted "Country" values
        df = df[~df["Country"].isin(["US", "Total: this sheet", "Total: all sheets"])]
        df = df.dropna(how="all")
        return df.rename(columns={"Country": "Territory"})
    
    def clean_american_data1(df):
        cleanup_columns = ["Comments", "Zipcode"]
        df = df.drop(cleanup_columns, axis=1)
        df = df.drop(df.index[-1])
        df = df.dropna(how="all")
        return df.rename(columns={"State": "Territory"})
    
    def clean_american_data2(df):
        cleanup_columns = ["Comments", "Zipcode"]
        df = df.drop(cleanup_columns, axis=1)
        # Drop the first row and the last two rows
        df = df.drop(df.index[0])
        df = df.drop(df.index[-1])
        df = df.drop(df.index[-1])
        df = df.dropna(how="all")
        return df.rename(columns={"State": "Territory"})

    # URLs for the datasets
    url_unAm = "https://docs.google.com/spreadsheets/d/1W4F-UwW8jNdw9ZjL0hf_P53m6BWKU9Xszwt0a2TiyFU/export?format=csv&gid=0"
    url_Am1 = "https://docs.google.com/spreadsheets/d/1W4F-UwW8jNdw9ZjL0hf_P53m6BWKU9Xszwt0a2TiyFU/export?format=csv&gid=1"
    url_Am2 = "https://docs.google.com/spreadsheets/d/1W4F-UwW8jNdw9ZjL0hf_P53m6BWKU9Xszwt0a2TiyFU/export?format=csv&gid=2"

    # Load datasets using the helper
    Unamerican = load_csv_from_url(url_unAm)
    Am1_data = load_csv_from_url(url_Am1)
    Am2_data = load_csv_from_url(url_Am2)

    # Clean each dataset using the dedicated cleaning functions
    Unamerican = clean_unamerican_data(Unamerican)
    Am1_data = clean_american_data1(Am1_data)
    Am2_data = clean_american_data2(Am2_data)

    # Combine datasets for later use
    American = pd.concat([Am1_data, Am2_data], axis=0)
    All = pd.concat([Unamerican, Am1_data, Am2_data], axis=0)

    data_options = ["Unamerican", "American", "All"]
    data_choice = input("What Beer List data would you like to analyze?\n"
                        "Options are \"Unamerican,\" \"American,\" and \"All.\"\n"
                        "Your choice: ")
    print()

    while data_choice not in data_options:
        print("Invalid input.")
        data_choice = input("What Beer List data would you like to analyze?\n"
                            "Options are \"Unamerican,\" \"American,\" and \"All.\"\n"
                            "Your choice: ")
        print()
    else:
        if data_choice == "Unamerican":
            path = Unamerican
        elif data_choice == "American":
            path = American
        elif data_choice == "All":
            path = All

    # ------------------------------
    # Analysis & Visualization Functions
    # ------------------------------

    def anonymizer(sheet, feat_column):
        alist = sheet[feat_column].unique().tolist()
        incremental_list = list(range(1, len(alist) + 1))
        mapping = dict(zip(alist, incremental_list))
        sheet[feat_column] = sheet[feat_column].map(mapping)
        sheet[feat_column] = sheet[feat_column].astype("Int64")

    def preprocess(data):
        anonymizer(data, "Territory")
        anonymizer(data, "Brewery")
        anonymizer(data, "Style")
        anonymizer(data, "Added")
        anonymizer(data, "SRC")
        anonymizer(data, "Been To")

    def plot_distribution(data):
        x = query(1)
        asp = 50 if x == "Territory" else 1
        sns.displot(data[x], kde=True, height=6, aspect=asp)
        plt.title(f"Raw {x}")
        plt.show()
        preprocess(data)
        sns.displot(data[x], kde=True, height=6, aspect=asp)
        plt.title(f"Processed {x}")
        plt.show()

    def plot_heatmap(data):
        plt.rcParams["figure.figsize"] = [8, 8]
        sns.heatmap(data.corr(), color="k", annot=True)
        plt.show()

    def plot_histogram(data):
        plt.rcParams["figure.figsize"] = [8, 8]
        data.hist()
        plt.show()

    def plot_violin(data):
        x = query(2)
        y = query_2(1)
        plt.rcParams["figure.figsize"] = [8, 6]
        sns.violinplot(x=x, y=data[y], palette="bright", data=data)
        plt.xticks([0, 1], ["Negative", "Positive"])
        plt.show()

    def plot_scatter(data):
        x = query(2)
        y = query_2(1)
        data.reset_index(inplace=True)
        plt.rcParams["figure.figsize"] = [6, 6]
        sns.scatterplot(data=data, x=x, y=y)
        plt.title(f"{x} by {y}")
        plt.show()

    def plot_scatter_matrix(data):
        pd.plotting.scatter_matrix(data[["Territory", "Brewery", "Zak", "Jon", "Style", "SRC", "Been To", "Had"]],
                                     figsize=(10, 9),
                                     diagonal="hist",
                                     marker="o")
        plt.show()

    def plot_contour(data):
        x = query(2)
        y = query_2(1)
        sns.kdeplot(x=data[x], y=data[y], fill=True, cmap="viridis")
        plt.title(f"Contour Plot of {x} vs. {y}")
        plt.xlabel(f"{x}")
        plt.ylabel(f"{y}")
        plt.show()

    def plot_boxen(data):
        x = query(3)
        y = query_2(2)
        plt.figure(figsize=(8, 6))
        sns.boxplot(x=x, y=y, data=data)
        plt.title(f"Box Plot of {y} vs. {x}")
        plt.xticks([0, 1], ["Not Had", "Had"])
        plt.ylabel(y)
        plt.show()

    analysis_options = ["1", "2", "3", "4", "5", "6", "7", "8"]

    def testype():
        test_choice = input("What Beer List data would you like to analyze?\n"
                             "Options are: \"1\" for distribution plot\n"
                             "\"2\" for heatmap\n"
                             "\"3\" for histogram\n"
                             "\"4\" for scatter plot\n"
                             "\"5\" for scatter matrix\n"
                             "\"6\" for contour plot\n"
                             "\"7\" for violin plot\n"
                             "\"8\" for box plot\n"
                             "Your choice: ")
        print()
        while test_choice not in analysis_options:
            print("Invalid input.")
            test_choice = input("What Beer List data would you like to analyze?\n"
                                "Options are: \"1\" for distribution plot\n"
                                "\"2\" for heatmap\n"
                                "\"3\" for histogram\n"
                                "\"4\" for scatter plot\n"
                                "\"5\" for scatter matrix\n"
                                "\"6\" for contour plot\n"
                                "\"7\" for violin plot\n"
                                "\"8\" for box plot\n"
                                "Your choice: ")
            print()
        if test_choice == "1":
            plot_distribution(path)
        elif test_choice == "2":
            preprocess(path)
            plot_heatmap(path)
        elif test_choice == "3":
            preprocess(path)
            plot_histogram(path)
        elif test_choice == "4":
            preprocess(path)
            plot_scatter(path)
        elif test_choice == "5":
            preprocess(path)
            plot_scatter_matrix(path)
        elif test_choice == "6":
            preprocess(path)
            plot_contour(path)
        elif test_choice == "7":
            preprocess(path)
            plot_violin(path)
        elif test_choice == "8":
            preprocess(path)
            plot_boxen(path)

    # ------------------------------
    # Control Flow
    # ------------------------------

    def run_analysis_session(data):
        """Run analysis repeatedly until the user is finished with the current dataset."""
        while True:
            testype()
            again = input("Would you like to run another analysis on this data? (y/n) ").lower()
            while again not in ["y", "n"]:
                print("Invalid input.")
                again = input("Would you like to run another analysis on this data? (y/n) ").lower()
            if again == "n":
                break

    def ask_restart():
        """Ask whether to load different data or quit, and return the decision."""
        choice = input("Would you like to load different beer data or quit? (restart/quit) ").lower()
        while choice not in ["restart", "quit"]:
            print("Invalid input.")
            choice = input("Would you like to load different beer data or quit? (restart/quit) ").lower()
        return choice

    # Run an analysis session on the chosen dataset, then ask whether to restart or quit.
    run_analysis_session(path)
    decision = ask_restart()
    if decision == "restart":
        Beer_List()
    else:
        exit()

Beer_List()