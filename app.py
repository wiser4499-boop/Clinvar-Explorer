import streamlit as st
import pandas as pd
from explorer import load_data, query_gene, gene_summary

@st.cache_data
def get_data():
    return load_data()

df = get_data()

st.title("ClinVar variant explorer")
gene = st.text_input("Gene symbol", placeholder="e.g. BRCA1")
sig = st.selectbox("Clinical significance",
      ["All","Pathogenic","Likely pathogenic",
       "Uncertain significance","Benign"])

if gene:
    result = query_gene(df, gene, None if sig=="All" else sig)
    st.write(f"{len(result)} variants found")
    st.bar_chart(gene_summary(df, gene))
    st.dataframe(result)
