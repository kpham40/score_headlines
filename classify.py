#!/usr/bin/env python
# coding: utf-8

# ML Engineering
# Assignment 3
# Paul Pham

# host = "localhost"
# port1 = "8015"
# port2 = "9015"

# In[5]:


# streamlit_app.py
import streamlit as st
import requests

API_URL = "http://localhost:8015/classify"

st.set_page_config(page_title="Headline Classifier", page_icon="📰")

st.title("Headline Classifier")
st.write("Enter your headlines below, you can edit or delete them, and get instant classification results!")

# Initialize session state for headlines
if "headlines" not in st.session_state:
    st.session_state.headlines = [""]

# Function to delete a headline
def delete_headline(index):
    st.session_state.headlines.pop(index)

# Function to add a headline
def add_headline():
    st.session_state.headlines.append("")

# Display editable text boxes
for i, text in enumerate(st.session_state.headlines):
    cols = st.columns([4, 1])
    st.session_state.headlines[i] = cols[0].text_input(f"Headline {i+1}", text)
    if cols[1].button("X", key=f"del_{i}"):
        delete_headline(i)
        st.experimental_rerun()

# Add headline button
if st.button("Add Headline"):
    add_headline()

# Submit button
if st.button("Classify Headlines"):
    headlines = [h.strip() for h in st.session_state.headlines if h.strip()]
    if headlines:
        try:
            resp = requests.post(API_URL, json={"headlines": headlines})
            if resp.status_code == 200:
                results = resp.json()["results"]
                st.subheader("Classification Results")
                st.table(results)
            else:
                st.error(f"API error: {resp.status_code}")
        except Exception as e:
            st.error(f"Could not connect to API: {e}")
    else:
        st.warning("Please enter at least one headline.")

