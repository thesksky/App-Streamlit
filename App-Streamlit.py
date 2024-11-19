#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")


# Streamlit simplifies the process of deploying Python scripts as web applications. By incorporating a few Streamlit commands into  Python script, we can create interactive web apps without the need for extensive front-end development knowledge. Once the script is ready, we can easily deploy it to platforms like Streamlit Community Cloud or Heroku, making our data-driven applications accessible to a wider audience. Creating a simple web app for the CatAPI scraping project.

# In[2]:


# App-Streamlit.py

# Title of the app
st.title("Cats API Scraper, limited use, only accessing facts")

# Section for API interaction
st.header("Get Random Cat Facts")
num_facts = st.slider("Number of facts to fetch", min_value=1, max_value=20, value=5, key="facts_slider_1")

# Fetch data from the CatsAPI
if st.button("Fetch Cat Facts"):
    url = f"https://catfact.ninja/facts?limit={num_facts}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        facts = data['data']

        # Display the facts in a DataFrame
        df = pd.DataFrame(facts)
        st.write("Fetched Cat Facts:")
        st.dataframe(df)

        # Optional: Save to CSV
        if st.button("Save to CSV"):
            df.to_csv("cat_facts.csv", index=False)
            st.success("Saved cat facts to cat_facts.csv!")
    else:
        st.error("Failed to fetch cat facts. Please try again later.")


# In[3]:


# Get API key from environment variable if run locally
# api_key = os.getenv("CAT_API_KEY")  # Replace "CAT_API_KEY" with the key name in your .env or deployment settings

# Get API key from Streamlit Cloud secrets if deployd on Streamlit
api_key = st.secrets["CAT_API_KEY"]

if not api_key:
    st.error("API Key not found.")

# Endpoint for cat images
url = "https://api.thecatapi.com/v1/images/search"

# Request headers with API key
headers = {
    "x-api-key": api_key
}

# Title of the app
st.title("Cats API Scraper with using my api_key")

# Section for API interaction
st.header("Get Random Cat Images")
num_images = st.slider("Number of images to fetch", min_value=1, max_value=20, value=5, key="image_slider")

# Fetch data from the CatsAPI
if st.button("Fetch Cat Images"):
    # Correctly use `num_images` from the slider
    response = requests.get(url, headers=headers, params={"limit": num_images})
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract image URLs
        image_urls = [item['url'] for item in data]
        
        # Display images
        st.write("Fetched Cat Images:")
        for img_url in image_urls:
            st.image(img_url, caption=img_url, use_container_width=True)

        # Optional: Save to CSV
        if st.button("Save to CSV"):
            df = pd.DataFrame(image_urls, columns=["Image URL"])
            df.to_csv("cat_images.csv", index=False)
            st.success("Saved cat images to cat_images.csv!")
    else:
        st.error("Failed to fetch cat images. Please try again later.")

