import streamlit as st
from st_screenwidth_detector import screenwidth_detector

st.write("screen width:", screenwidth_detector())
