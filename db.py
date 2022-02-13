# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 22:52:59 2022

@author: leonidas
"""
import streamlit as st
import pandas as pd
import sqlite3
import os


#path to db
db_path = os.path.join(os.getcwd(), 'db','auth.db')

from authlib.auth import auth, authenticated, requires_auth
from authlib.common import trace_activity


import env
env.verify()


#give permission for creating following tables
authenticated()

##build tables and fill them with data
#connect to db
conn = sqlite3.connect(db_path)

#create table
cur = conn.cursor()
cur.execute("create table if not exists hrguys (id INTEGER PRIMARY KEY,name text, firstname text, company text, email text, quotaleft integer, quotaused integer)")
cur.execute("create table if not exists requestquota (id INTEGER PRIMARY KEY,hrguys_id integer,reqquota integer)")
cur.execute("create table if not exists surveyanswers (id INTEGER PRIMARY KEY,surveycand_id integer,hrguys_id integer, age integer, silent integer, right integer, nerd integer, dbms integer,animal integer)")


cur.execute("insert into hrguys values (NULL,'fett','django','tatoine','df@daimo.de',10,0);")
cur.execute("insert into hrguys values (NULL,'fett','boba','tatoine','bf@daimo.de',10,0);")
cur.execute("insert into hrguys values (NULL,'hi','ho','aerosol','hiho@aerosol.de',0,0);")
cur.execute("insert into requestquota values (NULL,2,5);")



cur.execute("create table if not exists surveycand (id INTEGER PRIMARY KEY,name text, firstname text, email text, team text,hrguysid text, subject text, message text)")
cur.execute("commit")


