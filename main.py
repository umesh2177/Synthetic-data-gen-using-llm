import pandas as pd
import json
import streamlit as st
# from groq import GroqModel
from groq_agent import python_code_agent
from groq_agent2 import sd_json_agent


def detect_date_format(series):
            try:
            # Sample first non-null date value
                sample = series.dropna().iloc[0]
                # Common date formats to check
                formats = [
                    '%Y-%m-%d', '%d-%m-%Y', '%m-%d-%Y',
                    '%Y/%m/%d', '%d/%m/%Y', '%m/%d/%Y',
                    '%Y.%m.%d', '%d.%m.%Y', '%m.%d.%Y',
                    '%Y-%m-%d %H:%M:%S', '%d-%m-%Y %H:%M:%S',
                    '%Y/%m/%d %H:%M:%S', '%d/%m/%Y %H:%M:%S'
                ]
                # Try each format
                for fmt in formats:
                    try:
                        pd.to_datetime(sample, format=fmt)
                        return fmt
                    except:
                        continue
                return None
            except:
                return None

def get_metadata(df):
    metadata = {
        "columns": list(df.columns),
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "column_details": {
        col: {
        "datatype": ("id" if col.lower().endswith('id') else 
        "categorical" if (df[col].isin([1, -1, '1', '-1']).all()) else
        "date" if (pd.to_datetime(df[col], errors='coerce').notna().any() and 
        not df[col].apply(lambda x: str(x).replace('.','').isdigit()).all()) else
        str(df[col].dtype) if pd.api.types.is_numeric_dtype(df[col]) else
        "boolean" if df[col].dtype == bool else
        "categorical" if df[col].nunique() < 10 else
        "text" if df[col].dtype == object else
        str(df[col].dtype)),
        "is_pii": any(pii in col.lower() for pii in ['name', 'email', 'phone', 'address', 'ssn', 'passport']),
        "date_format": detect_date_format(df[col]) if pd.to_datetime(df[col], errors='coerce').notna().any() else None,
        "unique_values": df[col].nunique() if df[col].nunique() < 10 else None,
        "categories": list(df[col].unique()) if (df[col].nunique() < 10 and not pd.api.types.is_numeric_dtype(df[col]) or df[col].isin([1, -1, '1', '-1']).all()) else None
        }
        for col in df.columns
        }
    }
    return metadata

def generate_synthetic_data(api_key, df,metadata):
      # Generate synthetic data section
        if st.button("Generate Synthetic Data Json file."):
            try:
                synthetic_data= sd_json_agent(question="Generate synthetic data in json format",sample_data=df.sample(n=20,random_state=42).to_json(),api_key_input=api_key,metadata=metadata)
                st.success("Synthetic data generated successfully")
                with open("synthetic_data.json", "w") as f:
                    f.write(synthetic_data.replace("`",""))

                # st.json(synthetic_data.replace("`",""))
                # synthetic_data_df=pd.DataFrame(json.loads(synthetic_data.replace("`","")))
                # synthetic_data_df.to_csv("synthetic_data_json.csv", index=False)
            except Exception as e:
                st.error(f"Failed to generate synthetic data: {str(e)}")

def generate_synthetic_data_code(api_key,df,metadata):
      if st.button("Generate Synthetic Data Python code."):
            try:
                synthetic_code=python_code_agent(question="Generate Python code using open-source libraries to create synthetic data",sample_data=df.sample(n=20,random_state=42),api_key_input=api_key,metadata=metadata)
                st.subheader("Generated Synthetic Data Code")
                st.code(synthetic_code, language="python")

                # Execute the synthetic data code
                st.success("Synthetic data generated successfully")

            except Exception as e:
                st.error(f"Failed to generate synthetic data: {str(e)}")


def read_csv_file(uploaded_file,api_key):
    if uploaded_file is not None:
        try:
            # Read the CSV file
            df = pd.read_csv(uploaded_file)
            metadata = get_metadata(df)
            # Display metadata
            st.subheader("Metadata")
            st.json(metadata)
            generate_synthetic_data(api_key,df,metadata)
            generate_synthetic_data_code(api_key,df,metadata)

        except Exception as e:
            st.error(f"Failed to read CSV file: {str(e)}")

def main():
    st.title("CSV Metadata Viewer and Synthetic Data Generator")
    api_key=st.text_input("Enter your groq api key")
    # File upload section
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    read_csv_file(uploaded_file,api_key)


if __name__ == "__main__":
    main()
