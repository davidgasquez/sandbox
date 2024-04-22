import duckdb
import pandas as pd

import streamlit as st

st.markdown("# Welcome to the DuckDB Streamlit Demo")

c = duckdb.connect("md:fdp")

st.write("Here's our first attempt at using data to create a table:")
st.write(
    pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})
)

a = st.radio("Select one:", ["filecoin_storage_providers", "filecoin_clients"])

st.write(c.sql(f"select * from main.{a}").df())
