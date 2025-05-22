import matplotlib.pyplot as plt
import pandas as pd
from bertopic import BERTopic

def fit_topics(df):
    """
    Fit BERTopic on df["clean"]
    Returns (model, df_with_topics).
    """
    docs = df["clean"].fillna("").astype(str).tolist()
    
    model = BERTopic(
        language="english", 
        calculate_probabilities=False, 
        verbose=False)
    
    topics, _ = model.fit_transform(docs)
    
    if len(topics) != len(df):
        raise ValueError(
            f"Topic assignments ({len(topics)}) ≠ document count ({len(df)})"
        )
    
    df_out = df.copy()
    df_out["topic"] = pd.Series(topics, index=df.index)

    return model, df_out

def get_rolling_df(df_topics, window=3, min_periods=1):
    """From df_topics, which has 'year' and 'topic' columns, return
    a pivoted DataFrame of topic counts by year with a rolling mean applied.
    """
    topic_year = (
        df_topics
        .groupby(["year", "topic"])
        .size()
        .reset_index(name="n")
    )
    # pivot to wide format
    pivot = (
        topic_year
        .pivot(index="year", columns="topic", values="n")
        .fillna(0)
        .sort_index()
    )
    # rolling mean
    rolling_df = pivot.rolling(window=window, min_periods=min_periods).mean()
    return rolling_df

def plot_trends(rolling_df):
    """ 
    Plot topic frequency by year (3-year rolling mean). 
    Returns the figure object."""
    
    fig, ax = plt.subplots(figsize=(10,5))
    rolling_df.plot(ax=ax, legend=False)

    ax.set_title("Nanoparticle-TNBC Topic Trends (3-year rolling average)")
    ax.set_xlabel("Publication Year")
    ax.set_ylabel("Avg. Papers / Year")
    ax.legend(title="Topic", bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.tight_layout()
    return fig
    