# -*- coding: utf-8 -*-
"""

@author: Leonidas, Sehmi


This module starts the Website.
"""
#import modules
import streamlit as st
import pandas as pd
import sqlite3
import os


#simple site configs
st.set_page_config(page_title="Authentication", layout="wide")

from authlib.auth import auth, authenticated, requires_auth
from authlib.common import trace_activity


import env
env.verify()

#path to db
db_path = os.path.join(os.getcwd(), 'db','auth.db')

#connect to db
conn = sqlite3.connect(db_path)

#create table
cur = conn.cursor()
#test print all tables
# cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
# rows = cur.fetchall()
# for row in rows:
#     st.write(row)
#user variable
user = auth(sidebar=True, show_msgs=True)

#user = "hrdadmin"

st.title('HRD Inc.')

#hrdadmin interface
if authenticated() and user == "hrdadmin":

    st.success(f'`{user}` is authenticated')

    st.write("Table: hrguys")
    st.write(pd.read_sql_query("SELECT * FROM hrguys", conn))
    
    st.write("Table: requestquota")
    st.write(pd.read_sql_query("SELECT * FROM requestquota", conn))
    
    grant_id = st.selectbox('Please select the id you want to grant from the requestquota table and press the "grant" key',list(range(0,999)), key="1")
    
    grant = st.button('grant', key="2")
    
    #process for granting new quota
    if grant:
        
        #get data from requestquota table
        cur.execute(f"SELECT * FROM requestquota where id={grant_id};")
        rows = cur.fetchall()
        #extract data
        hrguys_id = rows[0][1]
        reqquota = rows[0][2]
        
        #get data from hrguys table to sum reqquota with old_quota
        cur.execute(f"SELECT quotaleft FROM hrguys where id={hrguys_id};")
        rows = cur.fetchall()
        
        #calc new_quota or quotaleft
        old_quota = rows[0][0]
        new_quota = old_quota + reqquota
        
        #update hrguys table with the new quota amount for quotaleft column
        cur.execute(f"update hrguys set quotaleft = {new_quota} where id = {hrguys_id};")
        cur.execute("commit")
        #show update
        st.write("Updated table: hrguys")
        st.write(pd.read_sql_query("SELECT * FROM hrguys", conn))
        
#hrguys interface
elif authenticated() and user.isdigit():
    
    st.success(f'`{user}` is authenticated')
    
    st.write("Please fill out to invite a survey candidate")
    name = st.text_input('name')
    firstname = st.text_input('firstname')
    email = st.text_input('email')
    team = st.text_input('team')
    
    
    invite = st.button('invite', key="3")
    
    #show table
    st.write("Table: surveycand")
    st.write(pd.read_sql_query("SELECT * FROM surveycand", conn))
    
    ##check for remaining quota
    #get data from hrguys table
    cur.execute(f"SELECT quotaleft FROM hrguys where id={user};")
    rows = cur.fetchall()
    
    #calc new_quota or quotaleft
    cur_quota = rows[0][0]
    
    #disable invite button if quota is not enough
    if cur_quota == 0:
        st.write("not enough quota! please request more!")
        invite.enabled = False


    
    #process for inviting new survey candidates
    if invite:

        
        hrguysid = user
        subject = "survey invitation"
        message = f"Hello {name}, please fill out your survey by klicking on this link: http://localhost:8503. Your credentials are surveyu1:1 Regards HR{user}"


        cur.execute(f"insert into surveycand values (NULL,'{name}','{firstname}','{email}','{team}','{hrguysid}','{subject}','{message}');")
        # cur.execute('DELETE FROM surveycand;')
        cur.execute("commit")
        
        #show update
        st.write("Updated table: surveycand")
        st.write(pd.read_sql_query("SELECT * FROM surveycand", conn))
        
        #UPDATE Orders SET Quantity = Quantity + 1 WHERE ...
        cur.execute(f"update hrguys set quotaleft = quotaleft - 1 where id = {hrguysid};")
        cur.execute(f"update hrguys set quotaused = quotaused + 1 where id = {hrguysid};")
        cur.execute("commit")
        #show update
        st.write("Updated table: hrguys")
        st.write(pd.read_sql_query("SELECT * FROM hrguys", conn))


    #request more quota
    amountq = st.selectbox('Please select the amount of quota you want to request',list(range(0,999)), key="4")
    
    request = st.button('request', key="5")
    
    if request:

        cur.execute(f"insert into requestquota values (NULL,{user},{amountq});")
        cur.execute("commit")
        st.write("Updated table: requestquota")
        st.write(pd.read_sql_query("SELECT * FROM requestquota", conn))

    
    
        
    #change hrguys data
    st.write("If you wish to change your customer data fill in the form (all fields are mandatory)")
    
    nameh = st.text_input('new name')
    firstnameh = st.text_input('new firstname')
    emailh = st.text_input('new email')
    companyh = st.text_input('new companyname')
    
    change = st.button('change', key="6")
    
    #show update
    st.write("Table: hrguys")
    st.write(pd.read_sql_query("SELECT * FROM hrguys", conn))

    
    if change:

    
        #update hrguys table with the new data
        cur.execute(f"update hrguys set name = '{nameh}',firstname = '{firstnameh}', company = '{companyh}', email = '{emailh}' where id = {user};")
        cur.execute("commit")
        
        #show update
        st.write("Updated table: hrguys")
        st.write(pd.read_sql_query("SELECT * FROM hrguys", conn))


    
    #show table
    st.write("Your invited people")
    st.write(pd.read_sql_query(f"SELECT * FROM surveycand where hrguysid = {user} order by team", conn))
    
    st.write("Number of team members per team")
    st.write(pd.read_sql_query(f"SELECT team, count(team) as members FROM surveycand where hrguysid = {user} group by team", conn))

    #show surveanswers
    st.write("Table: surveyanswers")
    st.write(pd.read_sql_query(f"SELECT * FROM surveyanswers", conn).astype(str))

    #status of invitation
    st.write("Table: status of invitation and survey")
    st.write(pd.read_sql_query(f"SELECT name,firstname,email,team,hrguysid,surveycand_id,hrguys_id,age,silent,right,nerd,dbms,animal FROM surveycand left join surveyanswers on surveycand.id = surveyanswers.surveycand_id", conn).astype(str))
    
    ##statistics of teams
    st.write("statistics of teams (0 is lowest and 10 is highest)")
    st.write(pd.read_sql_query(f"select team,AVG(NULLIF(age,'')) as avg_age,AVG(NULLIF(silent,'')) as avg_silent,AVG(NULLIF(right,'')) as avg_right,AVG(NULLIF(nerd,'')) as avg_nerd,AVG(NULLIF(dbms,'')) as avg_dbms,AVG(NULLIF(animal,'')) as avg_animal  from surveyanswers,surveycand where surveycand.id = surveyanswers.surveycand_id group by team", conn).astype(str))
    st.write("Recommendation if a person will work well in a team: The persons age, silent-, nerd-,dbms- and animal-score should not be too far away from the average in a team. But the right-score should not be high too if the average right-score in a team is already high!")
    


elif authenticated() and user == "surveyu1":
    
    st.write("Please fill out your survey.")
    
    #name of the surveycandidate
    names = st.text_input('name (mandatory)')
    firstnames = st.text_input('firstname (mandatory)')
        
    # st.write("user found!")
    # st.write("your ID is",surveycand_id)
    # st.write("your hrgys_id is",hrgys_id)
    
    #survey questions
    ages = st.text_input('type in your age (no text allowed only numbers)')
    silent = st.text_input('type in a number from 0-10. 0 stands for i can work well in a loud environment and 10 stands for i need a quiet place to concentrate.')
    right = st.text_input('type in a number from 0-10. 0 stands for you would never confront someone who is in the wrong and 10 stands for you would always confront someone who is in the wrong.')
    nerd = st.text_input('type in a number from 0-10. 0 stands for im not interested in technology and 10 stands for iam a nerd.')
    dbms = st.text_input('type in a number from 0-10. 0 stands for im not interested in DBMS and 10 stands for iam fascinated of DBMS.')
    anim = st.text_input('type in a number from 0-10. 0 stands for i hate animals and 10 stands for i love animals.')
    

    send = st.button('send', key="8")
        
    if send:
        
        #find ids for surveycandidate since these are mandatory for the surveyanswers table
        cur.execute(f"SELECT * FROM surveycand where name = '{names}' and firstname = '{firstnames}';")
        rows = cur.fetchall()
        #extract data
        surveycandids = rows[0][0]
        hrgys_id = rows[0][5]


        
        #insert into surveyanswers table
        cur.execute(f"insert into surveyanswers values (NULL,'{surveycandids}','{hrgys_id}','{ages}','{silent}','{right}','{nerd}','{dbms}','{anim}');")
        cur.execute("commit")
        
        #show update
        st.write("succesfully added following row to table")
        st.write(pd.read_sql_query(f"SELECT * FROM surveyanswers where surveycand_id = {surveycandids}", conn))
    
    
    
else:
    st.warning(f'permission denied')

