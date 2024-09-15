import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from PIL import Image 
import folium
from streamlit_folium import folium_static
from haversine import haversine
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title = "Restourante",page_icon="U+1F371", layout="wide")

#=====
# Codigo
#======

df = pd.read_csv("c:/Users/caioc/Documents/FACULDADE/CURSO_DATA_SCIENCE_COMUNIDADE_DS/Formação_DS/Python_para_Analise_de_Dados/Ciclo_V/Exercicios/train.csv")

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
        col1, col2,col3,col4,col5, col6 = st.columns(6, gap='large')
        with col1:
            st.header("Quantidade de entregadores unicos")
            entregadores_unicos = len(df["Delivery_person_ID"].unique())
            col1.metric ( ' Entregadores Unicos ', entregadores_unicos)
        with col2:
            st.header("Distancia media entre os restourantes")
            cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
            df["distancia"] = df.loc[:,cols].apply(lambda x: haversine(x['Restaurant_latitude'], x['Restaurant_longitude'], x['Delivery_location_latitude'], x['Delivery_location_longitude']), axis=1)
            distancia_media = df["distancia"].mean()
            col2.metric ( 'Distancia media entre restaurantes ', distancia_media)
        with col3:
            st.title("Tempo medio de entrega durante os festivais")
            df['tempo_de_entrega'] = df['Time_taken(min)'].str.replace('(min)', '', regex=False).str.strip()
            df_new_festival = df["Festival"] != "NaN "
            df = df.loc[df_new_festival,:]
            cols = ['tempo_de_entrega','Festival']
            tempo_medio_durante_festival = df.loc[:,cols].groupby("Festival").agg({'tempo_de_entrega':['mean','std']})
            tempo_medio_durante_festival.columns = ["Tempo_medio","Desvio_padrao"]
            tempo_medio_durante_festival = tempo_medio_durante_festival.reset_index()
            tempo_medio_durante_festival = np.round(tempo_medio_durante_festival.loc[tempo_medio_durante_festival["Festival"] == "Yes", "Tempo_medio"],2)
            col3.metric("Mean T - festivais", tempo_medio_durante_festival)
        with col4:
            st.title("Desvio padrão de entrega durante os festivais")
            df['tempo_de_entrega'] = df['Time_taken(min)'].str.replace('(min)', '', regex=False).str.strip()
            df_new_festival = df["Festival"] != "NaN "
            df = df.loc[df_new_festival,:]
            cols = ['tempo_de_entrega','Festival']
            desvio_padrao_entrega_durante_festival = df.loc[:,cols].groupby("Festival").agg({'tempo_de_entrega':['mean','std']})
            desvio_padrao_entrega_durante_festival.columns = ["Tempo_medio","Desvio_padrao"]
            desvio_padrao_entrega_durante_festival= desvio_padrao_entrega_durante_festival.reset_index()
            desvio_padrao_entrega_durante_festival = np.round(desvio_padrao_entrega_durante_festival.loc[desvio_padrao_entrega_durante_festival["Festival"] == "Yes", "Desvio_padrao"],2)
            col3.metric("STD - festivais", desvio_padrao_entrega_durante_festival)
            
        with col5:
            st.title("Tempo medio de entrega durante sem os festivais")
            df['tempo_de_entrega'] = df['Time_taken(min)'].str.replace('(min)', '', regex=False).str.strip()
            df_new_festival = df["Festival"] != "NaN "
            df = df.loc[df_new_festival,:]
            cols = ['tempo_de_entrega','Festival']
            tempo_medio_sem_festival = df.loc[:,cols].groupby("Festival").agg({'tempo_de_entrega':['mean','std']})
            tempo_medio_sem_festival.columns = ["Tempo_medio","Desvio_padrao"]
            tempo_medio_sem_festival = tempo_medio_sem_festival.reset_index()
            tempo_medio_sem_festival = np.round(tempo_medio_sem_festival.loc[tempo_medio_sem_festival["Festival"] == "No", "Tempo_medio"],2)
            col4.metric("Mean T s/festivais", tempo_medio_sem_festival)
        with col6:
            st.title("Tempo medio de entrega durante sem os festivais")
            df['tempo_de_entrega'] = df['Time_taken(min)'].str.replace('(min)', '', regex=False).str.strip()
            df_new_festival = df["Festival"] != "NaN "
            df = df.loc[df_new_festival,:]
            cols = ['tempo_de_entrega','Festival']
            desvio_padrao_de_entrega_sem_festival = df.loc[:,cols].groupby("Festival").agg({'tempo_de_entrega':['mean','std']})
            desvio_padrao_de_entrega_sem_festival.columns = ["Tempo_medio","Desvio_padrao"]
            desvio_padrao_de_entrega_sem_festival = desvio_padrao_de_entrega_sem_festival.reset_index()
            desvio_padrao_de_entrega_sem_festival = np.round(desvio_padrao_de_entrega_sem_festival.loc[desvio_padrao_de_entrega_sem_festival["Festival"] == "No", "Tempo_medio"],2)
            col4.metric("STD s/festivais", desvio_padrao_de_entrega_sem_festival)

    with st.container():
            df['tempo_de_entrega'] = df['Time_taken(min)'].str.replace('(min)', '', regex=False).str.strip()
            tabela_vr_pt3_1 = df.loc[:,["tempo_de_entrega","City"]].groupby("City").mean().reset_index()
            tabela_vr_pt3_1.columns = ["Cidade","Tempo_medio"] 
            tabela_vr_pt3_2 = df.loc[:,["tempo_de_entrega","City"]].groupby("City").std().reset_index()
            tabela_vr_pt3_2.columns = ["Cidade","Desvio_padrao"]
            tempo_medio_entrega = pd.merge(tabela_vr_pt3_1,tabela_vr_pt3_2, how = 'inner')
            fig = go.Figure()
            fig.add_trace(go.Bar(name = 'Control', x = tempo_medio_entrega["Cidade"], y = tempo_medio_entrega["Tempo_medio"], error_y = dict(type = 'data', array = tempo_medio_entrega["Desvio_padrao"])))
            fig.update_layout(barmode = 'group')
            st.plotly_chart(fig)


    with st.container():
        st.title( "Distribuição do Tempo" )
        col1, col2, col3 = st.columns(3)
        with col1:    
            st.title("Tempo medio de entrega por cidade")
            cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
            df["distancia"] = df.loc[:,cols].apply(lambda x: haversine(x['Restaurant_latitude'], x['Restaurant_longitude'], x['Delivery_location_latitude'], x['Delivery_location_longitude']), axis=1)
            distancia_media = df.loc[:,["City","distancia"]].groupby("City").mean().reset_index()
            fig = go.Figure(data=[go.Pie(labels=distancia_media["City"], values=distancia_media["distancia"], pull=[0,0.1,0])])
            st.plotly_chart(fig)

        with col2:
            tabela_pt5_vr_1 = df.loc[:,["tempo_de_entrega","City","Road_traffic_density"]].groupby(["City","Road_traffic_density"]).mean().reset_index()
            tabela_pt5_vr_1.columns = ["City","Tipo_de_trafego","Tempo_medio_entrega"]
            tabela_pt5_vr_2 = df.loc[:,["tempo_de_entrega","City","Road_traffic_density"]].groupby(["City","Road_traffic_density"]).std().reset_index()
            tabela_pt5_vr_2.columns = ["City","Tipo_de_trafego","desvio_padrao_tempo_entrega"]
            tempo_medio_desvio_padra_cidade_tipo_trafego = pd.merge(tabela_pt5_vr_1,tabela_pt5_vr_2, how='inner')
            fig = px.sunburst(tempo_medio_desvio_padra_cidade_tipo_trafego, path=["City","Tipo_de_trafego"], values="Tempo_medio_entrega", color="desvio_padrao_tempo_entrega", color_continuous_scale= "RdBu" ,color_continuous_midpoint=np.average(tempo_medio_desvio_padra_cidade_tipo_trafego["desvio_padrao_tempo_entrega"]))
            st.plotly_chart(fig)

    with st.container():
        st.title( "Distribuição da distancia" )
        tabela_pt4_vr_1 = df.loc[:,["tempo_de_entrega","City","Type_of_order"]].groupby(["City","Type_of_order"]).mean().reset_index()
        tabela_pt4_vr_1.columns = ["City","Tipo_de_pedido","tempo_medio_de_entrega"]
        tabela_pt4_vr_2 = df.loc[:,["tempo_de_entrega","City","Type_of_order"]].groupby(["City","Type_of_order"]).std().reset_index()
        tabela_pt4_vr_2.columns = ["City","Tipo_de_pedido","desvio_padrao_tempo_entrega"]
        tempo_medio_desvio_padrao_cidade_tipo_pedido = pd.merge(tabela_pt4_vr_1,tabela_pt4_vr_2, how='inner')
        st.dataframe(tempo_medio_desvio_padrao_cidade_tipo_pedido)

        

