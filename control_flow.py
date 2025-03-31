# control_flow.py
from analysis import (plot_distribution, plot_heatmap, plot_histogram, plot_violin,
                      plot_scatter, plot_scatter_matrix, plot_contour, plot_boxen, preprocess, log_tree)
from input_handlers import query, query_2

analysis_options = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

def testype(path):
    test_choice = input("What Beer List data would you like to analyze?\n"
                         "Options are: \"1\" for distribution plot\n"
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
                            "Options are: \"1\" for distribution plot\n"
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
    elif test_choice == "9":
        preprocess(path)
        log_tree(path)

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
