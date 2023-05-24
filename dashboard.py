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
from GAI_custom_email import *
import json

def main(username="User"):
    
    df=pd.read_csv("history.csv")
    history=pd.DataFrame(
        {"Month":["January","February","March","April","May","June"],"Sent":[300,250,313,259,210,218,],"Actual_Purchased":[60,75,55,79,40,51]})
    col1, col2,col3=st.columns([0.75,0.1,0.15])
    with col1:
        st.markdown("<h1 class='text-light'>Dashboard</h1>",unsafe_allow_html=True)
    with col2:
        st.markdown("---")
        st.markdown(f"<h6 class='text-light pt-2'>Hi &nbsp;&nbsp<strong class='text-capitalize'>{username}</strong></h6>",unsafe_allow_html=True)
    with col3:
        st.markdown("---")
        logout=st.button("logout")

    if not logout:
        listTabs = [" Analysis "," Create Data "," Generate Email "]
        whitespace = 31
        analysis, JoinDB, message = st.tabs([s.center(whitespace,"\u2001") for s in listTabs])

        with analysis:
            st.markdown("<h3 class='text-light'>Analysis</h3>",unsafe_allow_html=True)
            # st.markdown("---")
            a1_col1,a1_col2, a1_col3,a1_col4,a1_col5,a1_col6=st.columns([0.01,0.3,0.01,0.3,0.01,0.3])
            a1_col2.metric("**Emails sent from 1st January 2023 to till date:**",history["Sent"].sum())
            a1_col4.metric("**Emails sent yesterday:**",250)
            a1_col6.metric("**Conversion Ratio**", "", "4%")
            st.markdown("---")

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
                    title="Conversion Statistics",
                    yaxis_title="No of Customers"
                )
            )
            st.plotly_chart(history_bar,use_container_width=True)
            st.markdown("---")
            a2_col1,a2_col2,a2_col3=st.columns(3)
            with a2_col1:
                treemap_plot=px.treemap(df,
                    path=[px.Constant("Total"),"customer_segment"],
                    title="RFM Treemap"
                )
                #st.plotly_chart(treemap_plot,use_container_width=True)
                selected_point=plotly_events(treemap_plot)
                #st.write(selected_point)
            categories=df["customer_segment"].unique()
            categories.sort()

            with a2_col2:
                #st.write(len(selected_point))
                if len(selected_point)==0:
                    selection=0
                else:
                    selection=selected_point[0]['pointNumber']
                #st.write(selected_point)
                #st.write(selection)
                df_selected=df[df["customer_segment"]==categories[selection]]
                gb1=GridOptionsBuilder.from_dataframe(df_selected[["first_name","last_name","email_Id","customer_segment"]])
                gb1.configure_selection(selection_mode="single", use_checkbox=True)
                gridoptions1=gb1.build()
                data1=AgGrid(df_selected[["first_name","last_name","email_Id","customer_segment"]],
                        fit_columns_on_grid_load=True,
                        update_mode=GridUpdateMode.SELECTION_CHANGED,
                        gridOptions = gridoptions1,enable_enterprise_modules=True,
                        allow_unsafe_jscode=True,
                        height=450
                )

            with a2_col3:
                text1="""A short label explaining to the user what this input is for. The label can optionally \
                        contain Markdown and supports the following elements: Bold, Italics, \
                        Strikethroughs, Inline Code, Emojis, and Links. Note that the data to be downloaded is \
                        stored in-memory while the user is connected, so it's a good idea to keep file sizes \
                        under a couple hundred megabytes to conserve memory.
                        """
                st.text_area(label="Message",value=text1, disabled=True,label_visibility="collapsed",height=450)
            st.markdown("---")

            a4_col1, a4_col2=st.columns(2)
            with a4_col1:
                df_no=df.groupby(["class"])["email_Id"].nunique().reset_index()
                class_plot=px.bar(df_no,x="class",
                                    y="email_Id",
                                    title="Customers across different classes",
                                    template="plotly_white"
                                )  
                st.plotly_chart(class_plot,use_container_width=True)
            with a4_col2:
                segment_pie=px.pie(df,names="Brand_segment",
                                        title="Brand segment",
                                        template="plotly_white"
                ) 
                st.plotly_chart(segment_pie,use_container_width=True)

        with JoinDB:
            st.markdown("<h3 class='text-light'>Join Tables</h3>",unsafe_allow_html=True)
            cd1_col1,cd1_col2 = st.columns(2)
            with cd1_col1:
                cd1_col1_1,cd1_col1_2 = st.columns(2)
                with cd1_col1_1:
                    age=st.selectbox("**Age:**",[25])
                with cd1_col1_2:
                    category=st.selectbox("**Sports Category:**",["Daily walker"])
                # st.markdown("###")
                county=st.selectbox("**County:**",['Ottawa County','Carbon County','Eddy County','Norfolk County','Gloucester County','San Joaquin County','Washington County'])
                Query=st.button("**Request**")
            with cd1_col2:
                
                st.write("**Customer data:**")
                if Query:
                    with st.spinner("Loading..."):
                        st.session_state.df_nike=read_snowflake_table_to_dataframe(table="NIKE_CUSTOMER_TABLE",County=county)
                        st.session_state.df_newscorp=read_snowflake_table_to_dataframe(table="Newscorp_cus_table",County=county)
                        st.session_state.df_newscorp=st.session_state.df_newscorp[["EMAIL_ADDRESS","CONTENT_PREFERENCE","PROGRAM"]]
                        st.session_state.queried=True
                        st.session_state.generated=False

                elif not st.session_state.queried:
                    cd1_col2.markdown("""<div class='alert alert-primary'>
                                        No Data Generated
                                        </div>""", unsafe_allow_html=True)
                if st.session_state.queried:
                    st.session_state.df_common=pd.merge(st.session_state.df_nike,st.session_state.df_newscorp,on='EMAIL_ADDRESS',how='inner')
                    cd1_col2.dataframe(st.session_state.df_common,height=250, use_container_width=True)

        with message:
            st.markdown("<h3 class='text-light'>Generate Email</h3>",unsafe_allow_html=True)
            st.markdown("---")
            ge1_col1, ge1_col2, ge1_col3=st.columns(3)
            with ge1_col1:
                brand_segment=st.selectbox("**Brand Segment:**",["Daily Walker","Classic Shoe Enthusiast","College Basketball","Classic Shoe Enthusiast","High Mileage Runner","Shoes for Fashion"])
            with ge1_col2:
                campaign=st.selectbox("**Campaign:**",["Play New","Basketball Verse","Equality"])
            with ge1_col3:
                discount=st.selectbox("**Discount:**",["10%","20%","30%","40%"])
            
            ge2_col1, ge2_col2=st.columns(2)
            with ge2_col1:
                rec1=st.selectbox("**Recommendation 1:**",["Vintage","Air Jordan","Air Max"])
            with ge2_col2:
                rec2=st.selectbox("**Recommendation 2:**",["Vintage","Air Jordan","Air Max"])

            st.markdown("---")
            #################################################################################################
            #######                     Selection of Email Recepients                                 ####### 
            #################################################################################################
            if not st.session_state.generated:
                message_container=st.empty()
                with message_container:
                    ge3_col1, ge3_col2=st.columns(2)
                    with ge3_col1:
                        if len(st.session_state.df_nike)==0:
                            st.markdown("""<div class='alert alert-warning'>
                                        Please Query the data before proceeding ...
                                        </div>""", unsafe_allow_html=True)
                            # st.info("Please Query the data before proceeding ... ")
                            generate_email=False
                        
                        else:
                            st.write("Select email recipients:")
                            gb2 = GridOptionsBuilder.from_dataframe(st.session_state.df_common[["EMAIL_ADDRESS","FIRST_NAME","LAST_NAME","SALUTATION"]])
                            gb2.configure_selection(selection_mode="multiple", use_checkbox=True)
                            gb2.configure_column("EMAIL_ADDRESS", headerCheckboxSelection = True)
                            gridoptions2=gb2.build()
                            data2=AgGrid(st.session_state.df_common[["EMAIL_ADDRESS","FIRST_NAME","LAST_NAME","SALUTATION"]],
                                        fit_columns_on_grid_load=True,
                                        update_mode=GridUpdateMode.SELECTION_CHANGED,
                                        gridOptions = gridoptions2,enable_enterprise_modules=True,
                                        allow_unsafe_jscode=True,
                                        height=280
                            )
                            generate_email=st.button("Generate Email")
                                
                    with ge3_col2:
                        if generate_email:
                            st.session_state.generated=True
                            with st.spinner("Generating Messages ..."):
                                select_emails=data2["selected_rows"]
                                st.session_state.df_gen=pd.DataFrame(columns=["EMAIL_ADDRESS","FIRST_NAME","LAST_NAME","SALUTATION","MESSAGE"])
                                c=0
                                for i in select_emails:
                    
                                    user=f"""SALUTATION : <{i['SALUTATION']}>, first name : <{i['FIRST_NAME']}> ,last name : <{i['LAST_NAME']}>"""
                                    message=create_ad(campaign=campaign,discount=discount,user=user,recommendation_1=rec1,recommendation_2=rec2)
                                    #message="Hello world "+str(c)
                                    st.session_state.df_gen.loc[len(st.session_state.df_gen.index)]=[i['EMAIL_ADDRESS'],i['FIRST_NAME'],i['LAST_NAME'],i['SALUTATION'],message]
                                    c=c+1
                            message_container.empty()
                            
                        else:
                            st.markdown("""<div class='alert alert-danger'>
                                        No Messages have been generated
                                        </div>""", unsafe_allow_html=True)
                            # st.info("No Messages have been generated")

            
            #################################################################################################
            #######                    Viewing Messages                                               ####### 
            #################################################################################################
            if st.session_state.generated:
                
                ge3_col1, ge3_col2=st.columns(2)
                with ge3_col1:
                    st.write("Select email recipients:")
                    gb3 = GridOptionsBuilder.from_dataframe(st.session_state.df_gen[["EMAIL_ADDRESS","FIRST_NAME","LAST_NAME","SALUTATION"]])
                    gb3.configure_selection(selection_mode="single", use_checkbox=True)
                    gb3.configure_column("EMAIL_ADDRESS", headerCheckboxSelection = False)
                    gridoptions3=gb3.build()
                    data3=AgGrid(st.session_state.df_gen[["EMAIL_ADDRESS","FIRST_NAME","LAST_NAME","SALUTATION"]],
                                    fit_columns_on_grid_load=True,
                                    update_mode=GridUpdateMode.SELECTION_CHANGED,
                                    gridOptions = gridoptions3,enable_enterprise_modules=True,
                                    allow_unsafe_jscode=True,
                                    height=280
                            )
                with ge3_col2:
                    selected_gen=data3["selected_rows"]
                    if selected_gen:

                        edit_message=st.checkbox("Edit message")

                        gen_message=st.session_state.df_gen[st.session_state.df_gen["EMAIL_ADDRESS"]==selected_gen[0]["EMAIL_ADDRESS"]]["MESSAGE"].values[0]
                        st.text_area(label="Message",value=gen_message,height=280,label_visibility="collapsed",disabled=not(edit_message))
                        #st.write(selected_gen[0]["_selectedRowNodeInfo"]["nodeRowIndex"])
                        #st.write(selected_gen)
                    else:
                        st.markdown("""<div class='alert alert-danger'>
                                        Select any Email
                                        </div>""", unsafe_allow_html=True)
                    send_email=st.button("Send Email")

    else:
        logout=False
        st.session_state.load_session=False
        st.session_state.failed=False
        st.experimental_rerun()
        pass

##################################################################################################################################

# user=f"""SALUTATION : <{row['SALUTATION']}>, first name : <{row['FIRST_NAME']}> ,last name : <{row['LAST_NAME']}>"""

#st.write(f"plotly=={plotly.__version__}")
#st.write(f"pandas=={pd.__version__}")
#st.write(f"streamlit=={st.__version__}")
#st.write(st_aggrid.__version__)
##################################################################################################################################