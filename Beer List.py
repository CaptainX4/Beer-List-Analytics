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
    var_options = ["Territory", "Brewery", "Beer", "Zak", "Jon", "Had", "Style", "ABV", "SRC"]

    print("Welcome to the Beer List Analysis Platform!\n"
          "\n"
          "Note, for tests that ask what variable you want to use, choices are:\n"
          "\"Territory,\" \"Brewery,\" \"Beer,\" \"Zak,\" \"Jon,\" \"Had,\" \"Style,\" \"ABV,\" and \"SRC.\"\n"
          "Depending on the analysis, some of these variables will not work.\n"
          "Please be patient. You are working with a lot of data. It takes a minute to load.")
    print()

    start = input("Press any key and hit return to continue. ")

    if len(start) == 0:
        print()
    else:
        pass

        print()

        url_unAm = "https://docs.google.com/spreadsheets/d/1W4F-UwW8jNdw9ZjL0hf_P53m6BWKU9Xszwt0a2TiyFU/export?format=csv&gid=0"
        url_Am1 = "https://docs.google.com/spreadsheets/d/1W4F-UwW8jNdw9ZjL0hf_P53m6BWKU9Xszwt0a2TiyFU/export?format=csv&gid=1"
        url_Am2 = "https://docs.google.com/spreadsheets/d/1W4F-UwW8jNdw9ZjL0hf_P53m6BWKU9Xszwt0a2TiyFU/export?format=csv&gid=2"

        context = ssl.create_default_context(cafile = certifi.where())
        data = urllib2.urlopen(url_unAm, context = context).read()

        data_str = data.decode("utf-8")
        Unamerican = pd.read_csv(StringIO(data_str))
        cleanup_unAm = ["Comments", "Country Total", "Zak Total", "Jon Total", "Maps Link"]
        Unamerican = Unamerican.drop(cleanup_unAm, axis = 1)
        Unamerican = Unamerican[Unamerican["Country"] != "US"]
        Unamerican = Unamerican[Unamerican["Country"] != "Total: this sheet"]
        Unamerican = Unamerican[Unamerican["Country"] != "Total: all sheets"]
        Unamerican = Unamerican.dropna(how = "all")
        Unamerican = Unamerican.rename(columns = {"Country": "Territory"})

        context = ssl.create_default_context(cafile = certifi.where())
        data = urllib2.urlopen(url_Am1, context = context).read()

        data_str = data.decode("utf-8")
        Am1_data = pd.read_csv(StringIO(data_str))
        cleanup_Am1 = ["Comments", "Zipcode"]
        Am1_data = Am1_data.drop(cleanup_Am1, axis = 1)
        Am1_data = Am1_data.drop(Am1_data.index[-1])
        Am1_data = Am1_data.dropna(how = "all")
        Am1_data = Am1_data.rename(columns = {"State": "Territory"})

        context = ssl.create_default_context(cafile = certifi.where())
        data = urllib2.urlopen(url_Am2, context = context).read()

        data_str = data.decode("utf-8")
        Am2_data = pd.read_csv(StringIO(data_str))
        cleanup_Am2 = ["Comments", "Zipcode"]
        Am2_data = Am2_data.drop(cleanup_Am2, axis = 1)
        Am2_data = Am2_data.drop(Am2_data.index[0])
        Am2_data = Am2_data.drop(Am2_data.index[-1])
        Am2_data = Am2_data.drop(Am2_data.index[-1])
        Am2_data = Am2_data.dropna(how = "all")
        Am2_data = Am2_data.rename(columns = {"State": "Territory"})

        American = pd.concat([Am1_data, Am2_data], axis = 0)
        All = pd.concat([Unamerican, Am1_data, Am2_data], axis = 0)

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
            sns.displot(path["Territory"], kde = True, height = 6, aspect = 50)
            plt.title("Raw Territory")
            plt.show()

            sns.displot(path["Been To"], kde = True)
            plt.show()

            sns.displot(path["Style"], kde = True)
            plt.show()

            sns.displot(path["Brewery"], kde = True)
            plt.show()

            # sns.displot(path["Beer"], kde = True)
            # plt.show()

        def anonymizer(sheet, feat_column):
            alist = sheet[feat_column].unique().tolist()

            def convert_to_incremental(original_list):
                return list(range(1, len(original_list) + 1))

            incremental_list = convert_to_incremental(alist)

            mapping = dict(zip(alist, incremental_list))

            sheet[feat_column] = sheet[feat_column].map(mapping)
            sheet[feat_column] = sheet[feat_column].astype("Int64")
            return mapping
            # print(mapping)

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
        path["ABV"] = pd.to_numeric(path["ABV"], errors = "coerce")

        clean = ["Beer"]
        path = path.drop(clean, axis = 1)

        path["Zak"] = pd.to_numeric(path["Zak"], errors = "coerce")
        path["Zak"] = path["Zak"].astype("Int64")
        # nan_counts_column = path["Zak"].isna().sum()
        # print("NaN counts per column:\n", nan_counts_column)
        path["Zak"] = path["Zak"].fillna(0)

        path["Jon"] = pd.to_numeric(path["Jon"], errors = "coerce")
        path["Jon"] = path["Jon"].astype("Int64")
        # nan_counts_column = path["Jon"].isna().sum()
        # print("NaN counts per column:\n", nan_counts_column)
        path["Jon"] = path["Jon"].fillna(0)

        path["Had"] = path["Zak"].astype(str) + path["Jon"].astype(str)

        path["Had"].replace({"01": 0, "11": 1, "10": 2}, inplace = True)

        #Heat Map
        def heat():
            plt.rcParams["figure.figsize"] = [8, 8]
            sns.heatmap(path.corr(), color = "k", annot = True)
            plt.show()

        #Histogram
        def hist():
            plt.rcParams["figure.figsize"] = [8, 8]
            path.hist()
            plt.show()

        #Violin Plot
        def violin():
            print("What two variables would you like to test?")
            x = input("X axis variable: ")
            y = input("Y axis variable: ")
            plt.rcParams["figure.figsize"] = [8, 6]
            sns.violinplot(x = x, y = path[y], palette = "bright", data = path)
            plt.title(f"Violin Plot of {x} vs. {y}")
            plt.show()

        #Distribution Plot
        def dis_2():
            sns.displot(path["Territory"], kde = True)
            plt.title("Anonymized Territory Data")
            plt.show()

            sns.displot(path["Brewery"], kde = True)
            plt.show()

            sns.displot(path["Style"], kde = True)
            plt.show()

            sns.displot(path["ABV"], kde = True)
            plt.show()

        #Scatter Plot
        def scat():
            # scat_opt = ["Territory", "Brewery", "Beer", "Zak,\" \"Jon,\" \"Had,\" \"Style,\" \"ABV,\" and \"SRC.
            print("What two variables would you like to test?")
            # scat_var_x = input("X axis variable: ")
            x = input("X axis variable: ")
            y = input("Y axis variable: ")
            path.reset_index(inplace = True)
            plt.rcParams["figure.figsize"] = [6, 6]
            sns.scatterplot(data = path, x = x, y = y)
            plt.title(f"{x} by {y}")
            plt.show()

        #Scatter Matrix
        def scat_mat():
            pd.plotting.scatter_matrix(path[["Territory", "Brewery", "Zak", "Jon", "Style", "SRC", "Been To", "Had"]],
                                       figsize = (10, 9),
                                       diagonal = "hist",
                                       marker = "o")
            plt.show()

        #Contour Plot
        def contour():
            print("What two variables would you like to test?")

            # getting input and saving it into a variable for labels
            x_var = input("X axis variable: ")
            y_var = input("Y axis variable: ")

            # taking input and getting the actual data to plot
            x = path[x_var]
            y = path[y_var]

            sns.kdeplot(x=x, y=y, fill=True, cmap="viridis")

            plt.title(f"Contour Plot of {x_var} vs. {y_var}")
            plt.xlabel(x_var)
            plt.ylabel(y_var)
            plt.show()

        # Box Plot
        def box():
            # print("Would you like to test Jon's data, or Zak's?")
            JZ = input("Would you like to test Jon's data, or Zak's? ")

            # y = path[input("Y axis variable: ")]
            # path["Attrition"] = df["Attrition"].apply(lambda x: 1 if x == "Yes" else 0)

            def create_boxplots(path, columns, target = JZ):
                for col in columns:
                    plt.figure(figsize = (8, 6))
                    sns.boxplot(x = target, y = col, data = path)
                    # plt.title(f"Box Plot of {col} vs. Attrition")
                    plt.xticks([0, 1], ["No", "Yes"])
                    plt.ylabel(col)
                    plt.show()

            columns_to_plot = ["Territory",
                               "Brewery",
                               "Had",
                               "Style",
                               "ABV",
                               "SRC"]

            create_boxplots(path, columns_to_plot)

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
                    preprocess()
                    dis_2()
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
                    box()
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
                if again == "n":
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