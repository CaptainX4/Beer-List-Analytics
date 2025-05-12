# control_flow.py
from analysis import (plot_distribution, plot_heatmap, plot_histogram, plot_violin,
                      plot_scatter, plot_scatter_matrix, plot_contour, plot_boxen, preprocess, log_tree)
from input_handlers import query, query_2

analysis_options = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


def testype(path):
    print()
    test_choice = input("What Beer List data would you like to analyze?\n"
                        "Options are:\n"
                        "\"1\" for distribution plot\n"
                        "\"2\" for heatmap\n"
                        "\"3\" for histogram\n"
                        "\"4\" for scatter plot\n"
                        "\"5\" for scatter matrix\n"
                        "\"6\" for contour plot\n"
                        "\"7\" for violin plot\n"
                        "\"8\" for box plot\n"
                        "\"9\" for logistic regression with decision tree\n"
                        "Your choice: ")
    print()
    while test_choice not in analysis_options:
        print("Invalid input.")
        test_choice = input("What Beer List data would you like to analyze?\n"
                            "Options are:\n"
                            "\"1\" for distribution plot\n"
                            "\"2\" for heatmap\n"
                            "\"3\" for histogram\n"
                            "\"4\" for scatter plot\n"
                            "\"5\" for scatter matrix\n"
                            "\"6\" for contour plot\n"
                            "\"7\" for violin plot\n"
                            "\"8\" for box plot\n"
                            "\"9\" for logistic regression with decision tree\n"
                            "Your choice: ")
        print()

    # Make a copy of the data to avoid modifying the original
    data_copy = path.copy()

    # Preprocess the data and get the processed version
    processed_data = preprocess(data_copy)

    if test_choice == "1":
        plot_distribution(processed_data)
    elif test_choice == "2":
        plot_heatmap(processed_data)
    elif test_choice == "3":
        plot_histogram(processed_data)
    elif test_choice == "4":
        plot_scatter(processed_data)
    elif test_choice == "5":
        plot_scatter_matrix(processed_data)
    elif test_choice == "6":
        plot_contour(processed_data)
    elif test_choice == "7":
        plot_violin(processed_data)
    elif test_choice == "8":
        plot_boxen(processed_data)
    elif test_choice == "9":
        log_tree(processed_data)


def run_analysis_session(path):
    while True:
        testype(path)
        again = input("Would you like to run another analysis on this data? (y/n) ").lower()
        while again not in ["y", "n"]:
            print("Invalid input.")
            again = input("Would you like to run another analysis on this data? (y/n) ").lower()
        if again == "n":
            break


def ask_restart():
    choice = input("Would you like to load different beer data or quit? (restart/quit) ").lower()
    while choice not in ["restart", "quit"]:
        print("Invalid input.")
        choice = input("Would you like to load different beer data or quit? (restart/quit) ").lower()
    return choice