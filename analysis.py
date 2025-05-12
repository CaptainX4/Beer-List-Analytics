# analysis.py
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from input_handlers import query, query_2, collect_responses
from sklearn import tree
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


# Global dictionary to store mappings
LABEL_MAPPINGS = {}


def anonymizer(sheet, feat_column):
    """
    Anonymize a column but keep track of the original values.
    
    Parameters:
    sheet: DataFrame containing the data
    feat_column: Column name to anonymize
    
    Returns:
    sheet: The DataFrame with anonymized values
    """
    # Skip if column doesn't exist
    if feat_column not in sheet.columns:
        return sheet
    
    # Get unique values
    alist = sheet[feat_column].unique().tolist()
    alist = [x for x in alist if pd.notna(x)]  # Filter out NA values
    
    if len(alist) == 0:
        return sheet
    
    # Create mapping
    incremental_list = list(range(1, len(alist) + 1))
    mapping = dict(zip(alist, incremental_list))
    reverse_mapping = dict(zip(incremental_list, alist))
    
    # Store the mapping in the global dictionary
    LABEL_MAPPINGS[feat_column] = mapping
    LABEL_MAPPINGS[f"{feat_column}_reverse"] = reverse_mapping
    
    # Apply mapping
    sheet[feat_column] = sheet[feat_column].map(mapping)
    sheet[feat_column] = sheet[feat_column].astype("Int64")
    
    # Instead of dropna(), filter directly
    sheet = sheet[~sheet[feat_column].isna()]
    
    return sheet


def preprocess(data):
    """Preprocess the data for analysis."""
    # Apply anonymization to each column
    data = anonymizer(data, "Territory")
    data = anonymizer(data, "Brewery")
    data = anonymizer(data, "Style")
    # data = anonymizer(data, "Added")  # Commented out in original
    data = anonymizer(data, "SRC")
    data = anonymizer(data, "Been To")

    # Process ABV column
    char_to_remove = "%"
    data["ABV"] = data["ABV"].str.replace(char_to_remove, '', regex=False)
    # Fix the issue by filtering rather than using dropna()
    data = data[~data["ABV"].isna()]
    data["ABV"] = pd.to_numeric(data["ABV"], errors="coerce")

    # Drop Beer column
    clean = ["Beer"]
    data.drop(clean, axis=1, inplace=True)

    # Process Zak and Jon columns
    data["Zak"] = pd.to_numeric(data["Zak"], errors="coerce")
    data["Zak"] = data["Zak"].astype("Int64")
    data["Zak"] = data["Zak"].fillna(0)

    data["Jon"] = pd.to_numeric(data["Jon"], errors="coerce")
    data["Jon"] = data["Jon"].astype("Int64")
    data["Jon"] = data["Jon"].fillna(0)

    # Create Had column
    data["Had"] = data["Zak"].astype(str) + data["Jon"].astype(str)
    data["Had"].replace({"01": 0, "11": 1, "10": 2}, inplace=True)
    
    # Process Added column
    data["Added"] = pd.to_datetime(data["Added"], dayfirst=False, errors='coerce')
    
    return data


def plot_distribution(data):
    asp = 3
    sns.displot(data[collect_responses(0,"")], kde=True, height=6, aspect=asp)
    plt.show()


def plot_heatmap(data):
    plt.rcParams["figure.figsize"] = [8, 8]
    sns.heatmap(data.corr(), color="k", annot=True)
    plt.show()


def plot_histogram(data):
    plt.rcParams["figure.figsize"] = [8, 8]
    data[collect_responses(0,"")].hist()
    plt.show()


def plot_scatter(data):
    x = query(2)
    y = query_2(1)
    data = data.reset_index(drop=True)
    plt.rcParams["figure.figsize"] = [6, 6]
    sns.scatterplot(data=data, x=x, y=y)
    plt.title(f"{x} by {y}")
    plt.show()


def plot_scatter_matrix(data):
    pd.plotting.scatter_matrix(
        data[["Territory", "Brewery", "Zak", "Jon", "Style", "Added", "SRC", "Been To", "Had"]],
        figsize=(10, 9),
        diagonal="hist",
        marker="o")
    plt.show()


def plot_contour(data):
    x = query(2)
    y = query_2(1)
    sns.kdeplot(x = data[x], y = data[y], fill = True, cmap = "viridis")
    plt.title(f"Contour Plot of {x} vs. {y}")
    plt.xlabel(f"{x}")
    plt.ylabel(f"{y}")
    plt.show()


def plot_violin(data):
    textify = collect_responses(1, "4,5,6,9")

    def list_to_string(arg, separator=""):
        return separator.join(map(str, textify))

    var_string = list_to_string(textify, ", ")
    print(f"For x, the best variables to use are {var_string}.")
    print()
    x = query(2)
    y = query_2(1)
    plt.rcParams["figure.figsize"] = [8, 6]
    num_ticks = len(data[x].values.unique())
    plt.locator_params(axis='x', nbins=num_ticks)
    data = data.reset_index(drop=True)  # Reset index to ensure uniqueness
    
    # Create the violin plot
    ax = sns.violinplot(x=x, y=y, palette="bright", data=data)
    
    # Get unique values for x-axis
    unique_vals = sorted(data[x].unique())
    
    # If we have a mapping for this column, apply it
    if f"{x}_reverse" in LABEL_MAPPINGS:
        reverse_mapping = LABEL_MAPPINGS[f"{x}_reverse"]
        
        # Create labels from mapping
        labels = [str(reverse_mapping.get(int(val), val)) for val in unique_vals]
        
        # Set the ticks and labels
        plt.xticks(range(len(unique_vals)), labels, rotation=45, ha='right')
    
    plt.show()


def plot_boxen(data):
    x = query(3)
    y = query_2(2)
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=x, y=y, data=data)
    
    # If we have a mapping for Had column, use specific labels
    if x == "Had":
        plt.xticks([0, 1, 2], ["Jon Only", "Both", "Zak Only"])
    # If we have a mapping for this column, apply it
    elif f"{x}_reverse" in LABEL_MAPPINGS:
        reverse_mapping = LABEL_MAPPINGS[f"{x}_reverse"]
        
        # Get unique values
        unique_vals = sorted(data[x].unique())
        
        # Create labels from mapping
        labels = [str(reverse_mapping.get(int(val), val)) for val in unique_vals]
        
        # Set the ticks and labels
        plt.xticks(range(len(unique_vals)), labels, rotation=45, ha='right')
    
    plt.title(f"Box Plot of {y} vs. {x}")
    plt.ylabel(y)
    plt.show()


def log_tree(data):
    data = data.dropna()
    X = data[collect_responses(0,"")]
    y = data[query(4)]
    print()
    deep = int(input("How many levels would you like the tree to be?\n"
                     "Note: Too many layers can create overfitting of data.\n"
                     "Too few can lead to underfitting. Number of layers: "))

    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.3,
                                                        random_state=0)

    model = LogisticRegression()

    model.fit(X_train, y_train)

    predict = model.predict(X_test)

    print(pd.DataFrame(confusion_matrix(y_test, predict),
                       columns=["Predicted No", "Predicted Yes"],
                       index=["Actual No", "Actual Yes"]))
    print(classification_report(y_test, predict))

    accuracy = accuracy_score(y_test, predict)
    print("Accuracy:", accuracy)

    dt = DecisionTreeClassifier(max_depth=deep)
    dt_model = dt.fit(X_train, y_train)

    plt.figure(figsize=(10, 8))
    tree.plot_tree(dt_model,
                   feature_names=list(X.columns),
                   class_names=["Not Had", "Had"])
    plt.show()