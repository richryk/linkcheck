import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

def check_backlinks(df):
    results = []
    for index, row in df.iterrows():
        page_url = row[0]
        backlink_url = row[1]
        try:
            response = requests.get(page_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a', href=backlink_url)
                if links:
                    for link in links:
                        no_follow = 'rel' in link.attrs and 'nofollow' in link.attrs['rel']
                        anchor_text = link.get_text(strip=True)
                        results.append([page_url, backlink_url, 'Yes', no_follow, anchor_text])
                else:
                    results.append([page_url, backlink_url, 'No', 'N/A', 'N/A'])
            else:
                results.append([page_url, backlink_url, 'Error', 'N/A', 'N/A'])
        except Exception as e:
            results.append([page_url, backlink_url, 'Failed', 'N/A', 'N/A'])

    return pd.DataFrame(results, columns=['Page URL', 'Backlink URL', 'Link Found', 'No-Follow', 'Anchor Text'])

def main():
    st.title("Backlink Checker App")

    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.write(df)

        if st.button('Check Backlinks'):
            results_df = check_backlinks(df)
            st.write(results_df)

if __name__ == "__main__":
    main()
