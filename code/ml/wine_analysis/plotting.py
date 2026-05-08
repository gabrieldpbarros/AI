import math
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame
from pathlib import Path

IMG_PATH = "data/imgs/"

def get_columns_qt(columns: list[str]) -> tuple[int, int]:
    total = len(columns)
    rows = 4
    cols = math.ceil(total / rows)
    return (rows, cols)

def boxplot(df: DataFrame, title: str, saving_name: str) -> None:
    plotting_df = df.drop("class", axis=1)

    plt.close("all")
    proportion = get_columns_qt(plotting_df.columns)
    plt.figure(figsize=(14, 8))

    for i, column in enumerate(plotting_df.columns):
        sub = plt.subplot(proportion[0], proportion[1], i+1)
        sub.boxplot(plotting_df[column].to_numpy())
        sub.set_xlabel("Eixo X")
        sub.set_ylabel("Valores")
        sub.set_title(f"Boxplot da feature {column}")

    plt.suptitle(title, horizontalalignment="center")
    plt.tight_layout()
    plt.savefig(
        Path(IMG_PATH) / saving_name,
        bbox_inches='tight'
    )
    plt.show()

def corr_matrix(df: DataFrame, title: str, saving_name:str) -> None:
    plotting_df = df.drop("class", axis=1)
    matrix = plotting_df.corr(method="pearson")

    plt.close("all")
    plt.figure(figsize=(20,16))
    sns.heatmap(
        matrix,
        annot=True,
        cmap="coolwarm",
        fmt=".1f",
        vmin=-1, vmax=1
    )
    plt.title(title)
    plt.savefig(Path(IMG_PATH) / saving_name)
    plt.show()

def pca(df: DataFrame, title: str, saving_name:str) -> None:
    plt.close("all")
    plt.figure(figsize=(10,8))
    sns.scatterplot(
        data=df,
        x='Principal Component 1',
        y='Principal Component 2',
        hue='Class', 
        palette='viridis'
    )
    plt.title(title)
    plt.savefig(Path(IMG_PATH) / saving_name)
    plt.show()

def show_elements_dist(df: DataFrame, title: str, saving_name:str) -> None:
    plt.close("all")
    plt.figure()
    sns.countplot(x="class", data=df)
    plt.title(title)
    plt.savefig(Path(IMG_PATH) / saving_name)
    plt.show()