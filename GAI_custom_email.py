import os
import requests
import json
import openai
import pandas as pd
import config
import random
import snowflake.connector
import csv
import re

print(config.AZURE_KEY)
#openai.api_key = "20e517d9eb8c403b8ebb05056601315e"
openai.api_key = config.AZURE_KEY
openai.api_base =  "https://foundry-demo.openai.azure.com/" # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = 'azure'
openai.api_version = '2022-12-01' # this may change in the future

deployment_name='fountry' #This will correspond to the custom name you chose for your deployment when you deployed a model. 

def read_snowflake_table_to_dataframe(table,County):
    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user='ANSIF',
        password='Gaicustomemail@234',
        #account='app.snowflake.com/east-us-2.azure/iz19763/',
        account='iz19763.east-us-2.azure',
        warehouse='COMPUTE_WH',
        database='GAI_DB',
        schema='PUBLIC'
    )

    # Retrieve table data
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table} where COUNTY='{County}'")
        rows = cursor.fetchall()
        column_names = [col[0] for col in cursor.description]

    # Convert data to DataFrame
    df = pd.DataFrame(rows, columns=column_names)
    return df


def extract_email_body(text):
    start = text.find("Dear")
    end = text.find("Just Do It!!! ")
    return text[start:end]
def add_salutations(email_body,user):
    email_body=email_body.replace("Dear User",f"Dear {user}")
    email_body=email_body.replace("<|im_end|"," ")
    return email_body


def create_ad(campaign,user,discount,recommendation_1,recommendation_2,client="Nike",tone="professional",platform="personalised targeted email"):
    context=f'''Your task is to write a {platform} on behalf of {client}, as a creative ad for the campaign: {campaign}.
    Personalised to a user, Include Discount {discount}, and recommendations from {recommendation_1} and {recommendation_2} if present.  '''
    prompt=f"""Use the following pieces of context to generate an email. If you don't know any detail, just say those details will be provided later, don't try to make up the details.

    {context}
    
    Email Format:
    <|im_start|>
    Dear User,
    <Body of the email>
    Scincerely,
    Nike
    Just Do it!!!
    <|im_end|>"""
    
    prompt_instructions=f"""
    The email should include the following:
- Do not make up names, keep salutation as Dear User,
- create only the body of the email
- Do not plagiarize content. All content must be original.
- The email should be written with the assumption that the recipient is interested in attending the event.
- Although the email is targeted to a specific individual, the tone of the email should be inclusive and not exclusive. 
- The email should not exceed 300 words.
- Ensure that the tone of the email is {tone} and engaging.
IMPORTANT :
- do not hallucinate, generate email based on the information shared.
- the response must only contain text and no code or tags
- Do not try to explain the products, campaign or recommendations.


"""
    #print(prompt)
    response = openai.Completion.create(
      engine=deployment_name,
      model="text-davinci-003",
      #model="gpt-3.5-turbo",
      prompt=str(prompt)+str(prompt_instructions),
      temperature=0.1,
      max_tokens=300,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    email_body=extract_email_body(response['choices'][0]['text'])
    email_body=add_salutations(email_body,user)
    return email_body
    #return response
    
#email=create_ad(campaign="Product trial",user="John Miller",discount=30,recommendation_1="Nike AIR Max",recommendation_2="Nike AIR Neo",client="Nike",tone="professional",platform="personalised targeted email")

# df["CUSTOM_EMAIL"]=""
# for index, row in df.iterrows():
    # campaign=row['CAMPAIGN']
    # discount=row['DISCOUNT']
    # recommendation_1=row['RECOMMENDATION_1']
    # recommendation_2=row['RECOMMENDATION_2']
    # user=f"""SALUTATION : <{row['SALUTATION']}>, first name : <{row['FIRST_NAME']}> ,last name : <{row['LAST_NAME']}>"""
    # response=create_ad(campaign,user,discount,recommendation_1,recommendation_2)
    # print(response)
    # df.at[index,"CUSTOM_EMAIL"]=response
