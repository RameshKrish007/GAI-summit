import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import plotly.express as px
import plotly
import st_aggrid
from plotly import graph_objects as go
from streamlit_plotly_events import plotly_events
import dash
import matplotlib.pyplot as plt
from dash import dcc, html

def main(username="User"):
    df=pd.read_csv("history.csv")
    history=pd.DataFrame(
        {"Month":["January","February","March","April","May","June"],"Sent":[300,250,313,259,210,218,],"Actual_Purchased":[60,75,55,79,40,51]})
    col1, col2,col3=st.columns([0.8,0.1,0.1])
    with col1:
        st.markdown("<h1 class='text-light'>Dashboard</h1>",unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h6 class='text-light'>Hi &nbsp;&nbsp<strong class='text-capitalize'>{username}</strong></h6>",unsafe_allow_html=True)
    with col3:
        logout=st.button("logout")

    if not logout:
        listTabs = [" Analysis "," Create Data "," Generate Email "]
        whitespace = 32
        analysis, JoinDB, message = st.tabs([s.center(whitespace,"\u2001") for s in listTabs])

        with analysis:
            st.markdown("<h3 class='text-light'>Analysis</h3>",unsafe_allow_html=True)
            # st.markdown("---")
            a1_col1,a1_col2, a1_col3,a1_col4,a1_col5,a1_col6=st.columns([0.01,0.3,0.01,0.3,0.01,0.3])
            a1_col2.metric("**Emails sent from 1st January 2023 to till date:**",history["Sent"].sum())
            a1_col4.metric("**Emails sent yesterday:**",250)
            a1_col6.metric("**Conversion Ratio**", "", "4%")
            
            #with a_col2:
            #    st.selectbox("Select date",[1,2])
            #df=pd.DataFrame(columns=["first name","last name","email id","date","message"])
            st.markdown("###")
            history_bar=go.Figure(
                data=[
                    go.Bar(
                        name="Sent",
                        x=history["Month"],
                        y=history["Sent"],
                        offsetgroup=0
                    ),
                    go.Bar(
                        name="Actual Purchased",
                        x=history["Month"],
                        y=history["Actual_Purchased"],
                        offsetgroup=1
                    )
                ],
                layout=go.Layout(
                    title="Email Trend Conversion Statistics",
                    yaxis_title="No of Customers"
                )
            )
            st.plotly_chart(history_bar,use_container_width=True)
            st.markdown("###")
            # gb1 = GridOptionsBuilder.from_dataframe(df[["first_name","last_name","email_Id"]])
            # gb1.configure_selection(selection_mode="single", use_checkbox=True)
            # gridoptions1=gb1.build()
            # data1=AgGrid(df[["first_name","last_name","email_Id"]],
            #             fit_columns_on_grid_load=True,
            #             update_mode=GridUpdateMode.SELECTION_CHANGED,
            #             gridOptions = gridoptions1,enable_enterprise_modules=True,
            #             allow_unsafe_jscode=True,
            #             height=300
            # )
            # st.markdown("---")
            a3_col1,a3_col2=st.columns(2)
            with a3_col1:
                st.markdown("<h3 class='text-light'>Recent Email Message</h3>",unsafe_allow_html=True)
                text1="""Hi John...!
                Greetings from Product......
                Grab your deal and Unlock benefits
                and Get our New collections with Special offer prize.
                ClickHere...
                
                Thanks
                """
                st.text_area(label="Message",value=text1, disabled=True,label_visibility="collapsed",height=200)
            
            with a3_col2:
                st.markdown("<h3 class='text-light'>Prompt </h3>",unsafe_allow_html=True)
                text2="""A short label explaining to the user what this input is for. The label can optionally \
                        contain Markdown and supports the following elements: Bold, Italics, \
                        Strikethroughs, Inline Code, Emojis, and Links. Note that the data to be downloaded is \
                        stored in-memory while the user is connected, so it's a good idea to keep file sizes \
                        under a couple hundred megabytes to conserve memory.
                        """
                st.text_area(label="prompt",value=text2,disabled=True,label_visibility="collapsed",height=200)   
            st.markdown("---")
            a4_col1, a4_col2=st.columns(2)
            with a4_col2:
                gb1 = GridOptionsBuilder.from_dataframe(df[["first_name","last_name","email_Id"]])
                gb1.configure_selection(selection_mode="single", use_checkbox=True)
                gridoptions1=gb1.build()
                data1=AgGrid(df[["first_name","last_name","email_Id"]],
                            fit_columns_on_grid_load=True,
                            update_mode=GridUpdateMode.SELECTION_CHANGED,
                            gridOptions = gridoptions1,enable_enterprise_modules=True,
                            allow_unsafe_jscode=True,
                            height=450
                )
            with a4_col1:
                segment_pie=px.pie(df,names="Brand_segment",
                                        title="Demographic Profile of customers ",
                                        template="plotly_white"
                ) 
                st.plotly_chart(segment_pie,use_container_width=True)
            st.markdown("---")




        with JoinDB:
            st.markdown("<h3 class='text-light'>Create Data</h3>",unsafe_allow_html=True)




        with message:
            st.markdown("<h3 class='text-light'>Generate Email</h3>",unsafe_allow_html=True)
            ge1_col1, ge1_col2, ge1_col3=st.columns(3)
            with ge1_col1:
                filter1=st.selectbox("Select filter 1:",[0,1,2])
            with ge1_col2:
                filter2=st.selectbox("Select filter 2:",[0,1,2])
            with ge1_col3:
                filter1=st.selectbox("Select filter 3:",[0,1,2])
            st.markdown("---")
            ge2_col1, ge2_col2=st.columns(2)
            df2=pd.read_csv("history.csv")
            #st.write(df2.info())
            #df2=df2.set_index("email id")
            

            with ge2_col1:
                st.write("Select email recipients:")
                gb2 = GridOptionsBuilder.from_dataframe(df2[["email_Id"]])
                gb2.configure_selection(selection_mode="multiple", use_checkbox=True)
                gb2.configure_column("email_Id", headerCheckboxSelection = True)
                gridoptions2=gb2.build()
                data2=AgGrid(df2[["email_Id"]],
                            fit_columns_on_grid_load=True,
                            update_mode=GridUpdateMode.SELECTION_CHANGED,
                            gridOptions = gridoptions2,enable_enterprise_modules=True,
                            allow_unsafe_jscode=True,
                            height=300
                )          
            with ge2_col2:
                # edit_message=st.checkbox("Edit message")
                # st.text_area(label=" Message ",value=" Area to display the message ",height=300,label_visibility="collapsed",disabled=not(edit_message))
                st.markdown("<button type='button' class='btn btn-sm btn-primary' disabled>Edit Message</button>",unsafe_allow_html=True)
                email_text="""Hi Tony...!
                Greetings from Product......
                Grab your deal and Unlock benefits
                and Get our New collections with Special offer prize.
                ClickHere...
                
                Thanks
                """
                st.text_area(label="Message",value=email_text,height=292,label_visibility="collapsed",disabled=True)


    else:
        logout=False
        pass

##################################################################################################################################
#st.write(f"plotly=={plotly.__version__}")
#st.write(f"pandas=={pd.__version__}")
#st.write(f"streamlit=={st.__version__}")
#st.write(st_aggrid.__version__)
##################################################################################################################################