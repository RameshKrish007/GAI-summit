import streamlit as st
from time import sleep
import dashboard
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import pandas as pd
from plotly import graph_objects as go
import plotly.express as px
from GAI_custom_email import *
import json

st.set_page_config(page_title="Login Page",layout="wide")
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous">
""", unsafe_allow_html=True)
var=False
with open('assets\\css\\style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
# st.markdown("###")
if "load_session" not in st.session_state:
    st.session_state.load_session=False
    st.session_state.Username=""
    st.session_state.failed=False
    st.session_state.queried=False
    st.session_state.df_nike=[]
    st.session_state.select_option="multiple"
    st.session_state.generated=False

users_list={
    "admin":"admin",
    "Kasi":"kasi",
    "Anirban":"Anirban",
    "Ansif":"Ansif"
}
login_container=st.empty()

if not st.session_state.load_session:
    with login_container:
        col1, col2, col3=st.columns([1,1,1])

        with col2:
            with st.form("Login"):
                col2_1, col2_2, col2_3=st.columns([1,4,1])
                with col2_2:
                    st.image("assets\\images\\LTIlogo.png")
                    st.markdown("<center> <h6> Enter snowflake credentials </h6> </center>",unsafe_allow_html=True)
                    st.session_state.Username=st.text_input("Username:")
                    Password=st.text_input("Password:",type="password")
                    login=st.form_submit_button("Login")
                    if st.session_state.failed:
                        st.error("Invalid username or password. Try Again")



                if login or st.session_state.load_session:
                    if st.session_state.Username in users_list and Password==users_list[st.session_state.Username]:
                        st.session_state.load_session=True
                        st.success("Logged in succesfully!")
                        sleep(0)
                        login_container.empty()
                    else:
                        st.error("Invalid username or password")
                        st.session_state.failed=True
                        st.experimental_rerun()

if st.session_state.load_session:
    dashboard.main(st.session_state.Username)
