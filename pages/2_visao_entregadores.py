import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from PIL import Image 
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title = "Entregadores",page_icon="U+1F4E5", layout="wide")

#=====
# Codigo
#======

df = pd.read_csv("dataset/train.csv")

df_delivery_person_age_new = df["Delivery_person_Age"] != "NaN "
df = df.loc[df_delivery_person_age_new,:]
df_multiple_deliveries_new = df["multiple_deliveries"] != "NaN "
df = df.loc[df_multiple_deliveries_new,:]
df["Delivery_person_Age"] = df["Delivery_person_Age"].astype(int)
df["Delivery_person_Ratings"] = df["Delivery_person_Ratings"].astype(float)
df['Order_Date'] = pd.to_datetime( df['Order_Date'], format='%d-%m-%Y' )
df["multiple_deliveries"] = df["multiple_deliveries"].astype(int)

#=====
# Barra lateral 
#======

st.header( 'Marketplace - Visão Entregadores' )

#image_path = 'c:/Users/caioc/Documents/FACULDADE/CURSO_DATA_SCIENCE_COMUNIDADE_DS/Formação_DS/Python_para_Analise_de_Dados/Ciclo_V/Exercicios/logo.png'

#image = Image.open('logo.png')
#st.sidebar.image( image,width=120)

st.header("Dashboard para visão de resultados")
st.sidebar.markdown("# Goes Consultorias")
st.sidebar.markdown("## Selecione uma data limite")

# Ajustando as datas para datetime.date
data_slider = st.sidebar.slider(
    label="Selecione uma data",
    value=datetime.date(2022, 4, 13),
    min_value=datetime.date(2022, 2, 11),
    max_value=datetime.date(2022, 4, 6),
    format="DD-MM-YYYY"
)

# Exibindo a data no formato desejado
st.header(data_slider.strftime('%d-%m-%Y'))

traffic_options = st.sidebar.multiselect('Condições de transito',['Low ','Medium ','High ','Jam '],default=['Low ','Medium ','High ','Jam '])
#linhas_selecionadas = df["Order_Date"] < data_slider
#df = df.loc[linhas_selecionadas,:]
linhas_selecionadas = df["Road_traffic_density"].isin(traffic_options)
df = df.loc[linhas_selecionadas,:]
st.dataframe(df)

#=======
# No streamlit layout 
#=======

tab1,tab2,tab3 = st.tabs(['','_','_'])

with tab1:
    with st.container():
        col1, col2,col3,col4 = st.columns(4, gap='large')
        with col1:
            maior_idade = df["Delivery_person_Age"].max()
            col1.metric ( 'Maior idade ', maior_idade)
        with col2:
            menor_idade = df["Delivery_person_Age"].min()
            col2.metric ( 'Menor idade ', menor_idade)
        with col3:
            melhor_condicao = df["Vehicle_condition"].max()
            col3.metric ( 'Melhor condicao ', melhor_condicao)
        with col4:
            pior_condicao = df["Vehicle_condition"].min()
            col4.metric ( 'Pior condicao ', pior_condicao)
    with st.container():
        st.title( "Avaliacoes" )
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Avaliacoes medias por entregador")
            media_avaliacao_por_entregador = df.loc[:,["Delivery_person_Ratings","Delivery_person_ID"]].groupby("Delivery_person_ID").mean().reset_index()
            st.dataframe( media_avaliacao_por_entregador)
        with col2:
            st.subheader("Avaliacoes medias por transito")
            tabela_pt4_1 = df.loc[:,["Delivery_person_Ratings","Road_traffic_density"]].groupby("Road_traffic_density").mean().reset_index()
            tabela_pt4_1.columns = ["Road_traffic_density","media_avaliacoes"]
            tabela_pt4_2 = df.loc[:,["Delivery_person_Ratings","Road_traffic_density"]].groupby("Road_traffic_density").std().reset_index()
            tabela_pt4_2.columns = ["Road_traffic_density","Desvio_padrao_avaliacoes"]
            media_desvio_padra_avaliacoes_densidate_trafego = pd.merge(tabela_pt4_1,tabela_pt4_2, how = "inner")
            st.dataframe ( media_desvio_padra_avaliacoes_densidate_trafego)
            st.subheader("Avaliacoes medias por clima")
            tabela_p5_1 = df.loc[:,["Delivery_person_Ratings","Weatherconditions"]].groupby("Weatherconditions").mean().reset_index()
            tabela_p5_1.columns = ["Weatherconditions","Media_avaliacoes"]
            tabela_p5_2 = df.loc[:,["Delivery_person_Ratings","Weatherconditions"]].groupby("Weatherconditions").std().reset_index()
            tabela_p5_2.columns = ["Weatherconditions","Desvio_padrao_avaliacoes"]
            media_desvio_padrao_avaliacoes_c_climaticas = pd.merge(tabela_p5_1,tabela_p5_2, how='inner')
            st.dataframe ( media_desvio_padrao_avaliacoes_c_climaticas)

    with st.container():
        st.title( "Velocidade de entrega" )
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top entregadores mais rapidos")
            df['tempo_de_entrega'] = df['Time_taken(min)'].str.replace('(min)', '', regex=False).str.strip()
            df["tempo_de_entrega"] = df["tempo_de_entrega"].astype(float)
            df_pt6 = df.loc[:,["tempo_de_entrega","Delivery_person_ID","City"]].groupby(['City','Delivery_person_ID']).mean().sort_values( ['City','tempo_de_entrega'], ascending = True).reset_index()
            df_pt6_vel_metropolitan = df_pt6.loc[df_pt6['City'] == 'Metropolitian ', :].head(10)
            df_pt6_vel_Urban = df_pt6.loc[df_pt6['City'] == 'Urban ', :].head(10)
            df_pt6_vel_Semi_Urban = df_pt6.loc[df_pt6['City'] == 'Semi-Urban ', :].head(10)
            entregadores_mais_rapidos = pd.concat([df_pt6_vel_metropolitan,df_pt6_vel_Urban,df_pt6_vel_Semi_Urban]).reset_index(drop=True)
            st.dataframe(entregadores_mais_rapidos)
        with col2:
            st.subheader("Top entregadores mais lentos")
            df_pt7 = df.loc[:,["tempo_de_entrega","Delivery_person_ID","City"]].groupby(['City','Delivery_person_ID']).mean().sort_values( ['City','tempo_de_entrega'], ascending = False).reset_index()
            df_pt7_vel_metropolitan = df_pt7.loc[df_pt7['City'] == 'Metropolitian ', :].head(10)
            df_pt7_vel_Urban = df_pt7.loc[df_pt7['City'] == 'Urban ', :].head(10)
            df_pt7_vel_Semi_Urban = df_pt7.loc[df_pt7['City'] == 'Semi-Urban ', :].head(10)
            entregadores_mais_lentos = pd.concat([df_pt7_vel_metropolitan,df_pt7_vel_Urban,df_pt7_vel_Semi_Urban]).reset_index(drop=True)
            st.dataframe(entregadores_mais_lentos)


