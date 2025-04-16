import streamlit as st
import pandas as pd
import os
from io import BytesIO

# App config
st.set_page_config(page_title="DataSweeper by Shaharyar", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        .stApp {
            background-color: #0f1117;
            color: #f0f2f6;
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3 {
            color: #ffffff;
        }
        .css-1aumxhk {
            background-color: #1c1e26;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
        }
        .stButton>button {
            background-color: #008CBA;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #0072a3;
        }
        .stDownloadButton>button {
            background-color: #28a745;
            color: white;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
        }
        .stDownloadButton>button:hover {
            background-color: #218838;
        }
    </style>
""", unsafe_allow_html=True)

# Title section
st.title("✨ DataSweeper: Sterling Integrator by Muhammad Shaharyar")
st.caption("Transform. Clean. Convert — All in a few clicks.")
st.write("Upload your CSV or Excel files to clean, explore, and convert them with ease.")

# File uploader
uploaded_files = st.file_uploader("📁 Upload your file(s):", type=["csv", "xlsx"], accept_multiple_files=True)

# If files are uploaded
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        # Load file into DataFrame
        try:
            df = pd.read_csv(file) if file_ext == ".csv" else pd.read_excel(file)
        except Exception as e:
            st.error(f"❌ Could not process {file.name}: {e}")
            continue

        with st.expander(f"📊 File: {file.name}", expanded=True):
            st.subheader("👁️ Quick Preview")
            st.dataframe(df.head())

            st.markdown("---")
            st.subheader("🧼 Clean Your Data")

            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Remove duplicates — {file.name}"):
                        df.drop_duplicates(inplace=True)
                        st.success("Duplicates removed.")
                with col2:
                    if st.button(f"Fill missing values — {file.name}"):
                        numeric_cols = df.select_dtypes(include=["number"]).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.success("Missing numeric values filled with column mean.")

            st.markdown("---")
            st.subheader("📌 Select Columns to Keep")
            selected_cols = st.multiselect(f"Choose columns for {file.name}", options=df.columns.tolist(), default=df.columns.tolist())
            df = df[selected_cols]

            st.markdown("---")
            st.subheader("📈 Visualize Data (First Two Numeric Columns)")
            if st.checkbox(f"Enable chart for {file.name}"):
                chart_data = df.select_dtypes(include="number")
                if not chart_data.empty:
                    st.bar_chart(chart_data.iloc[:, :2])
                else:
                    st.info("No numeric data to plot.")

            st.markdown("---")
            st.subheader("🔁 Convert & Download")
            conversion_choice = st.radio(f"Choose format for {file.name}:", ["CSV", "Excel"], key=file.name)
            
            if st.button(f"🚀 Convert {file.name}"):
                buffer = BytesIO()
                file_output = file.name.replace(file_ext, ".csv" if conversion_choice == "CSV" else ".xlsx")
                mime_type = "text/csv" if conversion_choice == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                if conversion_choice == "CSV":
                    df.to_csv(buffer, index=False)
                else:
                    df.to_excel(buffer, index=False)

                buffer.seek(0)
                st.download_button(
                    label=f"📥 Download {file_output}",
                    data=buffer,
                    file_name=file_output,
                    mime=mime_type
                )

st.markdown("---")
st.success("✅ All files processed. You're all set!")
