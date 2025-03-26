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

    def dis():
        x = query(1)
        asp = 50 if x == "Territory" else 1
        sns.displot(path[x], kde=True, height=6, aspect=asp)
        plt.title(f"Raw {x}")
        plt.show()
        preprocess()
        sns.displot(path[x], kde=True, height=6, aspect=asp)
        plt.title(f"Processed {x}")
        plt.show()

    def anonymizer(sheet, feat_column):
        alist = sheet[feat_column].unique().tolist()

        def convert_to_incremental(original_list):
            return list(range(1, len(original_list) + 1))

        incremental_list = convert_to_incremental(alist)
        mapping = dict(zip(alist, incremental_list))
        sheet[feat_column] = sheet[feat_column].map(mapping)
        sheet[feat_column] = sheet[feat_column].astype("Int64")

    def preprocess():
        anonymizer(path, "Territory")
        anonymizer(path, "Brewery")
        anonymizer(path, "Style")
        anonymizer(path, "Added")
        anonymizer(path, "SRC")
        anonymizer(path, "Been To")

    char_to_remove = "%"
    path["ABV"] = path["ABV"].str.replace(char_to_remove, '', regex=False)
    path["ABV"] = path["ABV"].dropna()
    path["ABV"] = pd.to_numeric(path["ABV"], errors="coerce")

    clean = ["Beer"]
    path = path.drop(clean, axis=1)

    path["Zak"] = pd.to_numeric(path["Zak"], errors="coerce")
    path["Zak"] = path["Zak"].astype("Int64")
    path["Zak"] = path["Zak"].fillna(0)

    path["Jon"] = pd.to_numeric(path["Jon"], errors="coerce")
    path["Jon"] = path["Jon"].astype("Int64")
    path["Jon"] = path["Jon"].fillna(0)

    path["Had"] = path["Zak"].astype(str) + path["Jon"].astype(str)
    path["Had"].replace({"01": 0, "11": 1, "10": 2}, inplace=True)

    def heat():
        plt.rcParams["figure.figsize"] = [8, 8]
        sns.heatmap(path.corr(), color="k", annot=True)
        plt.show()

    def hist():
        plt.rcParams["figure.figsize"] = [8, 8]
        path.hist()
        plt.show()

    def violin():
        x = query(2)
        y = query_2(1)
        plt.rcParams["figure.figsize"] = [8, 6]
        sns.violinplot(x=x, y=path[y], palette="bright", data=path)
        plt.xticks([0, 1], ["Negative", "Positive"])
        plt.show()

    def scat():
        x = query(2)
        y = query_2(1)
        path.reset_index(inplace=True)
        plt.rcParams["figure.figsize"] = [6, 6]
        sns.scatterplot(data=path, x=x, y=y)
        plt.title(f"{x} by {y}")
        plt.show()

    def scat_mat():
        pd.plotting.scatter_matrix(path[["Territory", "Brewery", "Zak", "Jon", "Style", "SRC", "Been To", "Had"]],
                                   figsize=(10, 9),
                                   diagonal="hist",
                                   marker="o")
        plt.show()

    def contour():
        x = query(2)
        y = query_2(1)
        sns.kdeplot(x=path[x], y=path[y], fill=True, cmap="viridis")
        plt.title(f"Contour Plot of {x} vs. {y}")
        plt.xlabel(f"{x}")
        plt.ylabel(f"{y}")
        plt.show()

    def boxen():
        x = query(3)
        y = query_2(2)
        plt.figure(figsize=(8, 6))
        sns.boxplot(x=x, y=y, data=path)
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
        else:
            if test_choice == "1":
                dis()
            elif test_choice == "2":
                preprocess()
                heat()
            elif test_choice == "3":
                preprocess()
                hist()
            elif test_choice == "4":
                preprocess()
                scat()
            elif test_choice == "5":
                preprocess()
                scat_mat()
            elif test_choice == "6":
                preprocess()
                contour()
            elif test_choice == "7":
                preprocess()
                violin()
            elif test_choice == "8":
                preprocess()
                boxen()
    testype()

    print()

    again_options = ["y", "n"]

    def more():
        again = input("Would you like to run another analysis on this data? (y/n) ")
        while again not in again_options:
            print("Invalid input.")
            again = input("Would you like to run another analysis on this data? (y/n) ")
            print()
        else:
            if again == "y":
                testype()
                more()
            elif again == "n":
                tier2 = ["restart", "quit"]
                def tier_2():
                    restart = input("Would you like to load different beer data or quit? (restart/quit) ")
                    while restart not in tier2:
                        print("Invalid input.")
                        restart = input("Would you like to load different beer data or quit? (restart/quit) ")
                    else:
                        if restart == "restart":
                            Beer_List()
                        else:
                            exit()
                tier_2()
    more()

Beer_List()