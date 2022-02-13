##this module is for initializing the userdatabase and choose the very first users
import streamlit as st
#simple site configs
st.set_page_config(page_title="Authentication", layout="wide")
import env
import authlib.auth as auth

#simple site configs
#import streamlit_debug
# streamlit_debug.set(flag=False, wait_for_client=True, host='localhost', port=8765)
env.verify()

#title of website
st.title('Database Admins')

#set storage provider
try:
    auth.override_env_storage_provider('SQLITE')
    auth.admin()
except Exception as ex:
    st.write('## Trapped exception')
    st.error(str(ex))

