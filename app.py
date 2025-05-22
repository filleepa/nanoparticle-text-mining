import streamlit as st
import pandas as pd
import plotly.express as px
from data_utils import fetch_records, save_raw
from config import RAW_CSV_PATH
from preprocess import add_clean_column
from modeling import fit_topics, get_rolling_df
import time


def main():
    st.title("Nanoparticle TNBC Topic Trender")
    st.markdown("Prototype app: fetch, clean, topic-model & visualize trends.")

    if st.button("Fetch & Preprocess Data"):
        with st.spinner("Downloading records…"):
            recs = fetch_records()
            save_raw(recs)
        df = add_clean_column(pd.read_csv(RAW_CSV_PATH))
        st.success(f"Fetched {len(df)} records and cleaned text.")
        model, df_topics = fit_topics(df)
        rolling_df = get_rolling_df(df_topics)

        # sidebar controls
        topics = st.sidebar.multiselect("Topics", rolling_df.columns, default=rolling_df.columns[:5])
        yrs = st.sidebar.slider("Year range", 
                                int(min(rolling_df.index)), 
                                int(max(rolling_df.index)), 
                                (int(min(rolling_df.index)), 
                                int(max(rolling_df.index))))
        df_view = rolling_df.loc[yrs[0]:yrs[1], topics]
        
        # plotly interactive line chart
        fig = px.line(
            df_view.reset_index().melt("year", var_name="topic", value_name="count"),
            x="year", y="count", color="topic",
            labels={"count":"Avg. Papers/Year","year":"Publication Year"},
            title="Topic Trends Over Time"
        )
        fig.update_layout(legend_title_text="Topic")
        st.plotly_chart(fig, use_container_width=True)
    
if __name__=="__main__":
    main()