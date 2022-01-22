import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.pyplot import figure
import plotly.express as px

df = pd.read_csv("D:/PCR\Semester 7/dsls_bootcamp/Pertemuan 3/Tugas/covid-vaccination-vs-death_ratio.csv")
df['date'] = pd.to_datetime(df['date'], format = '%Y-%m-%d', errors='ignore')

st.markdown("## Visualization per Country")
country_name = list(df['country'].unique())
option = st.selectbox('Country Name', country_name)
