# analysis.py
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from input_handlers import query, query_2  # Import from input_handlers if needed

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