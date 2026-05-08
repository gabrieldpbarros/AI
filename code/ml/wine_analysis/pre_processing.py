import pandas as pd
from pathlib import Path
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from plotting import boxplot, corr_matrix, pca, show_elements_dist

PATH = "data/wine/wine.data"
FEATURES = [
    "class",
    "Alcohol",
 	"Malic acid",
 	"Ash",
	"Alcalinity of ash",
 	"Magnesium",
	"Total phenols",
 	"Flavanoids",
 	"Nonflavanoid phenols",
 	"Proanthocyanins",
	"Color intensity",
 	"Hue",
 	"OD280/OD315 of diluted wines",
 	"Proline"
]
SAVING_TITLE1 = "boxplot_wo_normalization.png"
SAVING_TITLE2 = "boxplot_w_normalization.png"
SAVING_TITLE3 = "elements_dist.png"
SAVING_TITLE4 = "corr_matrix.png"
SAVING_TITLE5 = "pca.png"

def apply_pca(df) -> pd.DataFrame:
    features_cols = df.drop("class", axis=1)
    classes = df["class"]

    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(features_cols)

    new_df = pd.DataFrame(data=principal_components, columns=['Principal Component 1', "Principal Component 2"])
    new_df['Class'] = classes.values
    return new_df

def load_data(path: Path | str) -> pd.DataFrame:
    return pd.read_csv(path, names=FEATURES)

def normalize_data(df: pd.DataFrame) -> None:
    scaler = StandardScaler()
    features_cols = df.columns.drop("class")
    df[features_cols] = scaler.fit_transform(df[features_cols])
        
def main():
    # a)
    df = load_data(PATH)
    boxplot(df, "Boxplot das features sem normalização", SAVING_TITLE1)

    # b)
    normalize_data(df)
    boxplot(df, "Boxplot das features com normalização", SAVING_TITLE2)

    # c)
    show_elements_dist(df, "Distribuição de elementos em cada classe.", SAVING_TITLE3)

    # d)
    corr_matrix(df, "Matriz de correlação das features", SAVING_TITLE4)

    # e)
    pca_df = apply_pca(df)
    pca(pca_df, "PCA dataset Wine", SAVING_TITLE5)

if __name__ == "__main__":
    main()