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


def anonymizer(sheet, feat_column):
    # Create the mapping as before
    alist = sheet[feat_column].unique().tolist()
    incremental_list = list(range(1, len(alist) + 1))
    mapping = dict(zip(alist, incremental_list))
    reverse_mapping = dict(zip(incremental_list, alist))
    
    # Store the mapping as an attribute of the dataframe
    if not hasattr(sheet, 'value_mappings'):
        sheet.value_mappings = {}
    
    # Store both forward and reverse mappings
    sheet.value_mappings[feat_column] = mapping
    sheet.value_mappings[f"{feat_column}_reverse"] = reverse_mapping
    
    # Map values to their anonymized versions
    sheet[feat_column] = sheet[feat_column].map(mapping)
    sheet[feat_column] = sheet[feat_column].astype("Int64")
    
    # Instead of using dropna() which changes indices, filter the dataframe directly
    sheet = sheet[~sheet[feat_column].isna()]
    
    return sheet  # Return the modified dataframe


# Helper function to apply original labels to axes
def apply_original_labels(data, ax, column, axis='x'):
    """Apply original labels to a plot axis if the column was anonymized.
    
    Parameters:
    - data: The dataframe containing the data
    - ax: The matplotlib axis object
    - column: The column name that might have been anonymized
    - axis: 'x' or 'y' to specify which axis to modify
    """
    if hasattr(data, 'value_mappings') and f"{column}_reverse" in data.value_mappings:
        # Get the mapping from numeric ID to original value
        reverse_mapping = data.value_mappings[f"{column}_reverse"]
        
        # Get current tick positions and labels
        if axis == 'x':
            ticks = ax.get_xticks()
            # Only apply to ticks that correspond to actual data values
            valid_ticks = [tick for tick in ticks if tick.is_integer() and int(tick) in reverse_mapping]
            if valid_ticks:
                # Create labels using the original values
                labels = [reverse_mapping.get(int(tick), '') for tick in valid_ticks]
                ax.set_xticks(valid_ticks)
                ax.set_xticklabels(labels, rotation=45, ha='right')
        elif axis == 'y':
            ticks = ax.get_yticks()
            valid_ticks = [tick for tick in ticks if tick.is_integer() and int(tick) in reverse_mapping]
            if valid_ticks:
                labels = [reverse_mapping.get(int(tick), '') for tick in valid_ticks]
                ax.set_yticks(valid_ticks)
                ax.set_yticklabels(labels)


def preprocess(data):
    # Apply anonymization to each column and update the dataframe
    data = anonymizer(data, "Territory")
    data = anonymizer(data, "Brewery")
    data = anonymizer(data, "Style")
    # data = anonymizer(data, "Added")  # Commented out as in original
    data = anonymizer(data, "SRC")
    data = anonymizer(data, "Been To")

    # Process ABV column
    char_to_remove = "%"
    data["ABV"] = data["ABV"].str.replace(char_to_remove, '', regex=False)
    # Fix: Drop rows where ABV is NA from the entire dataframe
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
    
    # Return the processed data
    return data


def plot_distribution(data):
    selected_vars = collect_responses(0,"")
    asp = 3
    
    # Create plots for each selected variable
    for var in selected_vars:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.histplot(data[var], kde=True, ax=ax)  # Using histplot instead of displot for more control
        
        # Apply original labels if available
        apply_original_labels(data, ax, var, axis='x')
        
        plt.title(f"Distribution of {var}")
        plt.tight_layout()
        plt.show()


def plot_heatmap(data):
    plt.rcParams["figure.figsize"] = [8, 8]
    fig, ax = plt.subplots(figsize=(8, 8))
    sns.heatmap(data.corr(), color="k", annot=True, ax=ax)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.show()


def plot_histogram(data):
    plt.rcParams["figure.figsize"] = [8, 8]
    selected_vars = collect_responses(0,"")
    
    # Create the histogram
    fig, axes = plt.subplots(len(selected_vars), 1, figsize=(8, 6*len(selected_vars)))
    
    # Handle case of single variable (axes won't be an array)
    if len(selected_vars) == 1:
        axes = [axes]
    
    # Plot each variable
    for i, (var, ax) in enumerate(zip(selected_vars, axes)):
        data[var].hist(ax=ax)
        ax.set_title(f"Histogram of {var}")
        
        # Apply original labels if available
        apply_original_labels(data, ax, var, axis='x')
    
    plt.tight_layout()
    plt.show()


def plot_scatter(data):
    x = query(2)
    y = query_2(1)
    data = data.reset_index(drop=True)
    plt.rcParams["figure.figsize"] = [6, 6]
    
    # Create the scatter plot
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.scatterplot(data=data, x=x, y=y, ax=ax)
    
    # Apply original labels if available
    apply_original_labels(data, ax, x, axis='x')
    apply_original_labels(data, ax, y, axis='y')
    
    plt.title(f"{x} by {y}")
    plt.tight_layout()
    plt.show()


def plot_scatter_matrix(data):
    # Scatter matrix is more complex to modify for original labels
    # We'll keep this function unchanged for now
    pd.plotting.scatter_matrix(
        data[["Territory", "Brewery", "Zak", "Jon", "Style", "Added", "SRC", "Been To", "Had"]],
        figsize=(10, 9),
        diagonal="hist",
        marker="o")
    plt.title("Scatter Matrix")
    plt.tight_layout()
    plt.show()


def plot_contour(data):
    x = query(2)
    y = query_2(1)
    
    # Create the contour plot
    fig, ax = plt.subplots()
    sns.kdeplot(x=data[x], y=data[y], fill=True, cmap="viridis", ax=ax)
    
    # Apply original labels if available
    apply_original_labels(data, ax, x, axis='x')
    apply_original_labels(data, ax, y, axis='y')
    
    plt.title(f"Contour Plot of {x} vs. {y}")
    plt.xlabel(f"{x}")
    plt.ylabel(f"{y}")
    plt.tight_layout()
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
    
    # Reset index to avoid any potential duplicate index issues
    data = data.reset_index(drop=True)
    
    plt.rcParams["figure.figsize"] = [8, 6]
    num_ticks = len(data[x].values.unique())
    plt.locator_params(axis='x', nbins=num_ticks)
    
    # Create the violin plot
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.violinplot(x=x, y=y, palette="bright", data=data, ax=ax)
    
    # Apply original labels if available
    apply_original_labels(data, ax, x, axis='x')
    apply_original_labels(data, ax, y, axis='y')
    
    plt.title(f"{x} by {y}")
    plt.tight_layout()
    plt.show()


def plot_boxen(data):
    x = query(3)
    y = query_2(2)
    
    # Create the boxplot
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x=x, y=y, data=data, ax=ax)
    
    # Apply original labels if available
    apply_original_labels(data, ax, x, axis='x')
    apply_original_labels(data, ax, y, axis='y')
    
    # Handle special case for "Had" column (maintain original behavior)
    if x == "Had":
        plt.xticks([0, 1], ["Not Had", "Had"])
    
    plt.title(f"Box Plot of {y} vs. {x}")
    plt.ylabel(y)
    plt.tight_layout()
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
    
    # Get the feature names
    feature_names = list(X.columns)
    
    # Try to get original feature names if they were anonymized
    if hasattr(data, 'value_mappings'):
        feature_names_display = []
        for col in X.columns:
            if col in data.value_mappings:
                # Show some sample values for this feature
                mapping = data.value_mappings[f"{col}_reverse"]
                samples = ", ".join([str(mapping.get(key, key)) for key in list(mapping.keys())[:3]])
                feature_names_display.append(f"{col} ({samples}...)")
            else:
                feature_names_display.append(col)
        
        # Use the enhanced feature names if available
        tree.plot_tree(dt_model,
                      feature_names=feature_names_display,
                      class_names=["Not Had", "Had"])
    else:
        # Fall back to original approach
        tree.plot_tree(dt_model,
                      feature_names=feature_names,
                      class_names=["Not Had", "Had"])
    
    plt.tight_layout()
    plt.show()