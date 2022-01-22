import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.pyplot import figure
import plotly.express as px

# Function
def ratio_population(variabel):
    df_variabel = df.groupby('country').agg({variabel:max})
    sum_variabel = df_variabel[variabel].sum()

    df_country = df.groupby('country').agg({'population':max})
    total_population = df_country['population'].sum()
    
    title = 'Ratio of '+variabel

    fig, ax = plt.subplots(figsize=(8,15), dpi=1000)
    ax.pie(
        [total_population,sum_variabel],
        autopct='%.2F%%',
        labels=['total_population',variabel],
        colors = ["#E02401","#F78812"],
        explode=(0,0.1))
    plt.title(title)
    st.pyplot(fig)
    plt.close(fig)
    del(fig)

def treeMapBreakdownbyCountry(variabel):
    df_country = df.groupby('country').agg({'people_vaccinated':max, 'population':max, 'population':max, 'total_vaccinations':max, 'people_fully_vaccinated':max})
    df_country = df_country.reset_index()
    title = "Total "+variabel+" Breakdown by Country"
    treemap = px.treemap(df_country, path=["country"],values=variabel, height = 750,
                     title=title,
                     color_discrete_sequence = px.colors.qualitative.Set3)

    treemap.update_traces(textinfo = "label+text+value")
    st.plotly_chart(treemap)

def run_geomap_death():
    New_deaths_df = df[['date', 'country', 'New_deaths']].sort_values('date')
    New_deaths_df = New_deaths_df[New_deaths_df.New_deaths > 0]
    New_deaths_df['log2(New_deaths)'] = np.log2(New_deaths_df['New_deaths'])
    New_deaths_df['date'] = New_deaths_df['date'].dt.strftime('%m/%d/%Y')

    fig = px.choropleth(New_deaths_df, locations="country", locationmode='country names',
                        color="log2(New_deaths)", hover_name="country", hover_data=['New_deaths'],
                        projection="natural earth", animation_frame="date",
                        title='<b>Coronavirus Global New_deaths Over Time</b>',
                        color_continuous_scale="reds",
                    )

    fig.update_layout(coloraxis={"colorbar": {"title":"<b>New_deaths</b><br>",
                                            "titleside":"top",
                                            "tickmode":"array"}
                                }
                    )

    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 10
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 2

    st.plotly_chart(fig)  


def run_geomap_vaccinations():
    total_vaccinations_df = df[['date', 'country', 'total_vaccinations']].sort_values('date')
    total_vaccinations_df = total_vaccinations_df[total_vaccinations_df.total_vaccinations > 0]
    total_vaccinations_df['log2(total_vaccinations)'] = np.log2(total_vaccinations_df['total_vaccinations'])
    total_vaccinations_df['date'] = total_vaccinations_df['date'].dt.strftime('%m/%d/%Y')

    fig = px.choropleth(total_vaccinations_df, locations="country", locationmode='country names',
                        color="log2(total_vaccinations)", hover_name="country", hover_data=['total_vaccinations'],
                        projection="natural earth", animation_frame="date",
                        title='<b>Coronavirus Global total_vaccinations Over Time</b>',
                        color_continuous_scale="greens",
                    )

    fig.update_layout(coloraxis={"colorbar": {"title":"<b>total_vaccinations</b><br>",
                                            "titleside":"top",
                                            "tickmode":"array"}
                                }
                    )

    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 10
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 2

    st.plotly_chart(fig)

st.set_page_config(page_title = 'Streamlit Dashboard', 
layout='wide',
page_icon='💹')

st.title('COVID vaccination vs. mortality Analysis')

df = pd.read_csv("D:/PCR\Semester 7/dsls_bootcamp/Pertemuan 3/Tugas/covid-vaccination-vs-death_ratio.csv")
df['date'] = pd.to_datetime(df['date'], format = '%Y-%m-%d', errors='ignore')
df.drop(columns=["Unnamed: 0"], axis=1, inplace=True)

first_kpi, second_kpi = st.columns(2) 

with first_kpi:
    st.markdown("**Data Set**")
    st.write(df)

with second_kpi:
    st.markdown("**Number of Country**")
    number2 = len(df['country'].unique()) 
    st.markdown(f"<h1 style='text-align: center; color: red; font_size: 100px'>{number2}</h1>", unsafe_allow_html=True)


st.markdown("## Ratio of Population")

first_chart, second_chart, third_chart = st.columns(3)


with first_chart:
    ratio_population('people_fully_vaccinated')

with second_chart:
    ratio_population('people_vaccinated')

with third_chart:
    ratio_population('total_vaccinations')

st.markdown("## TreeMap")

first_treemap, second_treemap= st.columns(2)
third_treemap, fourth_treemap= st.columns(2)

with first_treemap:
    treeMapBreakdownbyCountry("people_vaccinated")
with second_treemap:
    treeMapBreakdownbyCountry("people_fully_vaccinated")
with third_treemap:
    treeMapBreakdownbyCountry("population")
with fourth_treemap:
    treeMapBreakdownbyCountry("total_vaccinations")


st.markdown("## Geo Map by Date per Country")

first_geomap, second_geomap= st.columns(2)
with first_geomap:
    run_geomap_death()
with second_geomap:
    run_geomap_vaccinations()


# Memisahkan setiap negara menjadi 1 csv
filter_country = df['country'].unique()
filter_country = list(filter_country)

for i in filter_country:
    data_percountry = df.where(df['country'] == i)
    data_percountry.dropna(inplace=True)
    data_percountry.to_csv(i+".csv")

def linechart(x, y1, title):
    fig, ax1 = plt.subplots(1,1,figsize=(16,9), dpi= 80)
    ax1.plot(x,y1,color='tab:red')

    ax1.set_xlabel('date',fontsize=20)
    ax1.tick_params(axis='x',rotation=0,labelsize=12)
    ax1.set_ylabel(title,color='tab:red',fontsize=20)
    ax1.tick_params(axis='y',rotation=0,labelcolor='tab:red')
    ax1.grid(alpha=0.4)
    st.pyplot(fig)

def call_country_and_draw_line_chart(country_name):
    csv_name = country_name+".csv"
    df_country = pd.read_csv(csv_name)
    df_country.drop(columns=["Unnamed: 0"], axis=1, inplace=True)
    df_country['date'] = pd.to_datetime(df_country['date'], format = '%Y-%m-%d', errors='ignore')
    column_name = ["total_vaccinations","people_vaccinated","people_fully_vaccinated","population","New_deaths"]
    df_country[column_name] = df_country[column_name].astype(int)
    
    x = df_country['date']
    y1 = df_country['total_vaccinations']
    y2 = df_country['New_deaths']
    y3 = df_country['people_vaccinated']
    y4 = df_country['people_fully_vaccinated']
    
    st.header("--"+country_name+"--")
    linechart(x, y1, 'total_vaccinations')
    linechart(x, y2, 'New_deaths')
    linechart(x, y3, 'people_vaccinated')
    linechart(x, y4, 'people_fully_vaccinated')

st.markdown("## Visualization per Country")
country_name = list(df['country'].unique())
option = st.selectbox('Country Name', country_name)
call_country_and_draw_line_chart(option)