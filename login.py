import streamlit as st
import base64
from PIL import Image, ImageDraw
from time import sleep
import dashboard
import os
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Login Page",layout="wide")

st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous">
""", unsafe_allow_html=True)

with open('assets\\css\\style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

var=False
    
if "load_session" not in st.session_state:
    st.session_state.load_session=False

#st.set_page_config(layout="centered")
#st.markdown(container_style, unsafe_allow_html=True)
users_list={
    "admin":"admin",
}
login_container=st.empty()

with login_container:
    #st.markdown("<h3>Welcome back! Please login to continue.</h3>",unsafe_allow_html=True)
    col1, col2, col3=st.columns([1,1,1])

    with col2:
        with st.form("Login"):
            col2_1, col2_2, col2_3=st.columns([1,4,1])
            with col2_2:
                st.image("assets\\images\\LTIlogo.png")
            # st.markdown("<center> <h3> Database login </h3> </center>",unsafe_allow_html=True)
            st.markdown("<center> <h6> Enter snowflake credentials </h6> </center>",unsafe_allow_html=True)
            col2_1, col2_2, col2_3=st.columns([1,4,1])
            with col2_2:
                Username=st.text_input("Username:")
                Password=st.text_input("Password:",type="password")
            col2_11, col2_22, col2_32=st.columns([1,4,1])
            with col2_22:
                "###"
                login=st.form_submit_button("Login")
                "###"
                Username="admin"
                Password="admin"
            if login or st.session_state.load_session:
                if Username in users_list and Password==users_list[Username]:
                    st.session_state.load_session=True
                    st.success("Logged in succesfully!")
                    sleep(0)
                    var=True
                    login_container.empty()
                    "###"
                else:
                    st.error("Invalid username or password")
if var:
    dashboard.main(Username)
    #st.write(var)

