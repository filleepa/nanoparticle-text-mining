import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from data_utils import fetch_records, save_raw
from config import RAW_CSV_PATH
from preprocess import add_clean_column
from modeling import fit_topics, get_rolling_df
import time
from wordcloud import WordCloud

label_map = {
    0: "Drug Delivery & Cancer Treatment",
    1: "Magnetic Hyperthermia & Imaging",
    2: "Plasmonic Photothermal Therapy",
    }

def load_and_topic_model():
    """
    Fetch and save data, then read, clean, fit, and produce
    a rolling mean df.
    """
    recs = fetch_records()
    save_raw(recs)
    
    df = add_clean_column(pd.read_csv(RAW_CSV_PATH))
    model, df_topics = fit_topics(df)
    
    
    df_topics["topic"] = df_topics["topic"].map(label_map).fillna("Other")
    rolling_df = get_rolling_df(df_topics)
    
    ## Finding the topic IDs for label mapping
    # topic_info = model.get_topic_info()      # overview: topic IDs and sizes
    # topic_words = {                           # top 10 words per topic
    #     topic_id: [w for w, _ in model.get_topic(topic_id)[:10]]
    #     for topic_id in topic_info.Topic[1:]  # skip the -1 “outliers”
    # }
    
    # df_topics = pd.DataFrame([
    #     {"topic_id": tid, "top_words": ", ".join(words)}
    #     for tid, words in topic_words.items()
    # ])
    # st.write(df_topics)
    
    return model, rolling_df

def plot_topic_wordcloud(model, topic_id):
    words = dict(model.get_topic(topic_id))
    wc = WordCloud(width=300, height=200).generate_from_frequencies(words)
    fig, ax = plt.subplots(figsize=(3,2))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    return fig


def main():
    st.title("Nanoparticle Cancer Research Topic Trender")
    st.markdown("Prototype app: fetch, clean, topic-model & visualize trends.")

    if st.button("Fetch & Preprocess Data"):
        model, rolling_df = load_and_topic_model()
        st.session_state["model"] = model
        st.session_state["rolling_df"] = rolling_df


    if "model" in st.session_state and "rolling_df" in st.session_state:
        model = st.session_state["model"]
        rolling_df = st.session_state["rolling_df"]
        
        # sidebar controls
        all_topics = list(rolling_df.columns)
        
        topics = st.sidebar.multiselect(
            "Topics", 
            all_topics, 
            default=all_topics
            )
        yrs = st.sidebar.slider("Year range", 
                                int(min(rolling_df.index)), 
                                int(max(rolling_df.index)), 
                                (int(min(rolling_df.index)), 
                                int(max(rolling_df.index)))
                                )
        
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
        
        # wordclouds
        st.header("Topic Word-Clouds")
        for tid, label in label_map.items():
            st.subheader(label)
            st.pyplot(plot_topic_wordcloud(model, tid))
            
    else:
        st.info("Click 'Fetch & Preprocess Data' to load and analyse the corpus.")
    
if __name__=="__main__":
    main()