import pandas as pd

COLS = ["GeneSymbol","ClinicalSignificance","PhenotypeList","ReviewStatus","Assembly","Start"]

def load_data():
    chunks = []
    for chunk in pd.read_csv("variant_summary.txt", sep="\t", low_memory=False,
                             usecols=COLS, chunksize=100000):
        filtered = chunk[(chunk["Assembly"] == "GRCh38") & (chunk["GeneSymbol"].notna())]
        chunks.append(filtered)
    return pd.concat(chunks, ignore_index=True)

def query_gene(df, gene, sig_filter=None):
    result = df[df["GeneSymbol"].str.upper() == gene.upper()]
    if sig_filter:
        result = result[result["ClinicalSignificance"] == sig_filter]
    return result[["GeneSymbol","ClinicalSignificance",
                   "PhenotypeList","ReviewStatus","Start"]]

def gene_summary(df, gene):
    result = df[df["GeneSymbol"].str.upper() == gene.upper()]
    return result["ClinicalSignificance"].value_counts()

if __name__ == "__main__":
    print("Loading data...")
    df = load_data()
    print(f"{len(df):,} variants loaded")
    result = query_gene(df, "BRCA1", sig_filter="Pathogenic")
    print(result.head(10))
