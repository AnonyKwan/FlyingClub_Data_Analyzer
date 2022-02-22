from cgitb import text
import streamlit as st
import pandas as pd
import numpy as np
import requests
import json

def sidebar():
    st.sidebar.image(paperplane_icon)
    sidebar_layout_title_0 = st.sidebar.columns([1,2,2,1])
    with sidebar_layout_title_0[1]:
        st.title("OPENSEA")
    with sidebar_layout_title_0[2]:
        st.title("STATS") 

    # OPENSEA API FOR FLYINGCLUB STATS
    response = json.loads(requests.get("https://api.opensea.io/api/v1/collection/paperplane-by-flyingclubio/stats").text)

    sidebar_layout_0 = st.sidebar.columns([1,2,2,1])
    with sidebar_layout_0[1]:
        num_items = int(response['stats']['count'])
        st.metric(label="紙飛機數量", value=num_items)     
    with sidebar_layout_0[2]:
        num_holders = int(response['stats']['num_owners'])
        st.metric(label="紙飛持有者", value=num_holders)

    sidebar_layout_1 = st.sidebar.columns([1,2,2,1])
    with sidebar_layout_1[1]:
        floor_price = response['stats']['floor_price']
        st.metric(label="當前地板價", value=floor_price)   
    with sidebar_layout_1[2]:
        thirty_day_volume = response['stats']['thirty_day_volume']
        st.metric(label="30日交易量", value=f"{thirty_day_volume:.1f} Ξ")

if __name__ == "__main__":
    paperplane_icon = 'https://flyingclub.io/assets/paperplane-3245df87512ef7c15e7b91cc0cdeae37109489f2c839fd48cb3674606e5fe0b3.png'
    st.set_page_config(
                        page_title="PaperPlane Analyzer",
                        page_icon=paperplane_icon,
                        layout="wide",
                        initial_sidebar_state="expanded"
                    )
    st.title('PaperPlane Analyzer')
    sidebar()