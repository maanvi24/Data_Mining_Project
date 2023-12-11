#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 17:06:22 2023

@author: Maanvi
"""

import streamlit as st
import requests

def main():
    st.title("Summary Generator")

    article = st.text_area("Enter your article here...")
    max_length = st.number_input("Max Length for Summary", min_value=1)
    min_length = st.number_input("Min Length for Summary", min_value=1)
    num_sentences = st.number_input("Number of Sentences for Summary", min_value=1)

    if st.button("Generate Summary"):
        st.write("Generating Summary...")

        # Prepare data for the API request
        data = {
            "summary": article,
            "max_length": int(max_length),
            "min_length": int(min_length),
            "num_sentences": int(num_sentences),
        }

        # Make API request to Flask backend
        response = requests.post("http://127.0.0.1:5000/generate_summary", json=data)

        if response.status_code == 200:
            result = response.json()
            st.success("Summary Generated Successfully!")
            st.subheader("Generated Summary:")
            st.write(result["generated_summary"])
        else:
            st.error("Failed to generate summary. Please check your input.")

if __name__ == "__main__":
    main()
