import streamlit as st
import pandas as pd
from training.classify import classify

st.set_page_config(
    page_title="Log Classification System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Custom CSS ----------
st.markdown("""
    <style>
        .main {
            background-color: #0e1117;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        h1 {
            font-weight: 700;
            letter-spacing: -0.5px;
        }

        .stTextArea textarea {
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.title("Log Classification System")
st.caption(
    "Upload CSV log files and automatically classify entries using Regex, BERT, and LLM pipelines."
)

st.divider()

# ---------- Sidebar ----------
with st.sidebar:
    st.header("Upload")

    uploaded_file = st.file_uploader(
        "Choose CSV File",
        type=["csv"]
    )

    st.divider()

    st.markdown("### About")
    st.write(
        """
        Classification Flow:
        1. Regex Matching
        2. BERT Classification
        3. LLM Classification (LegacyCRM)
        """
    )

# ---------- Main Content ----------
if uploaded_file:

    df = pd.read_csv(uploaded_file)

    required_columns = {"source", "log_message"}

    if not required_columns.issubset(df.columns):
        st.error(
            "CSV must contain 'source' and 'log_message' columns."
        )
        st.stop()

    logs = list(zip(df["source"], df["log_message"]))

    with st.spinner("Classifying logs..."):
        results = classify(logs)

    predictions = pd.DataFrame(
        results,
        columns=[
            "Source",
            "Log Message",
            "Category"
        ]
    )

    content = "\n".join(
        predictions["Log Message"].astype(str)
    )

    # ---------- Metrics ----------
    total_logs = len(predictions)

    num_categories = predictions["Category"].nunique()

    top_category = (
        predictions["Category"]
        .value_counts()
        .idxmax()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Logs",
        total_logs
    )

    col2.metric(
        "Unique Categories",
        num_categories
    )

    col3.metric(
        "Top Category",
        top_category
    )

    st.divider()

    # ---------- Tabs ----------
    tab1, tab2, tab3 = st.tabs(
        [
            "Raw Logs",
            "Classification Results",
            "Analytics"
        ]
    )

    # ---------- Raw Logs ----------
    with tab1:
        st.subheader("Uploaded Logs")

        st.text_area(
            "Logs",
            content,
            height=350,
            label_visibility="collapsed"
        )

    # ---------- Results ----------
    with tab2:

        st.subheader("Classification Results")

        categories = sorted(
            predictions["Category"]
            .dropna()
            .unique()
        )

        selected_categories = st.multiselect(
            "Filter Categories",
            categories
        )

        if selected_categories:
            filtered_df = predictions[
                predictions["Category"]
                .isin(selected_categories)
            ]
        else:
            filtered_df = predictions

        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=450
        )

        csv = filtered_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "Download Results",
            data=csv,
            file_name="classified_logs.csv",
            mime="text/csv"
        )

    # ---------- Analytics ----------
    with tab3:

        st.subheader("Category Distribution")

        category_counts = (
            predictions["Category"]
            .value_counts()
        )

        st.bar_chart(category_counts)

        st.dataframe(
            category_counts.rename("Count"),
            use_container_width=True
        )

else:
    st.info(
        "Upload a CSV file containing 'source' and 'log_message' columns to begin."
    )