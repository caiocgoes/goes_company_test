import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from PIL import Image 
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title = "Empresa",page_icon="U+1F3EC", layout="wide")

#=====
# Codigo
#======
#c:/Users/caioc/Documents/FACULDADE/CURSO_DATA_SCIENCE_COMUNIDADE_DS/Formação_DS/Python_para_Analise_de_Dados/Ciclo_V/Exercicios/train.csv#
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

#image_path = 'c:/Users/caioc/Documents/FACULDADE/CURSO_DATA_SCIENCE_COMUNIDADE_DS/Formação_DS/Python_para_Analise_de_Dados/Ciclo_V/Exercicios/logo.png'
#image = Image.open('logo.png')
#st.sidebar.image( image,width=120)

st.header("Dashboard para visão de resultados")
st.sidebar.markdown("# Goes Consultorias")
st.sidebar.markdown("## Visao empresa")
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

#=====
# Layout no Streamlit
#======

tab1, tab2, tab3 =st.tabs( ['Visão Gerencial', 'Visão Tatica', 'Visão Geográfica'] )

with tab1:

    #grafico 1
    with st.container():
         st.header("Pedidos por dia")
         #selecao de linhas
         df_ex1 = df.loc[:,["ID","Order_Date"]].groupby("Order_Date").count().reset_index()
         df_ex1.columns = ["Dia","Pedido"]
         #grafico
         fig = px.bar(df_ex1,x = "Dia", y="Pedido")
         st.plotly_chart(fig, user_container_width = True) #usado para que o grafico caiba aqui dentro
     # container para colocar graficos 2 e 3
    with st.container():
        col1,col2 = st.columns(2)
        #Grafico 2
        with col1:
            st.markdown(" Pedidos por tipo de trafego")
            df_Road_traffic_density_new = df["Road_traffic_density"]  != "NaN "
            df= df.loc[df_Road_traffic_density_new,:]
            Product_Qt = len(df["ID"])
            df_product_by_td = df.loc[:,["ID","Road_traffic_density"]].groupby("Road_traffic_density").count().reset_index()
            df_product_by_td["Distibuition"] = df_product_by_td["ID"]/Product_Qt
            fig_g2 = px.pie(df_product_by_td, values = 'Distibuition', names = "Road_traffic_density")
            st.plotly_chart(fig_g2, user_container_width = True)
        #Grafico 3
        with col2:
            st.markdown(" # coluna 2")
            df_city_new = df["City"]  != "NaN "
            df= df.loc[df_city_new,:]
            df_Road_traffic_density_new = df["Road_traffic_density"]  != "NaN "
            df = df.loc[df_Road_traffic_density_new,:]
            df_ex4 = df.loc[:,["ID","City","Road_traffic_density"]].groupby(["City","Road_traffic_density"]).count().reset_index()
            df_ex4["percentual"] = (df_ex4["ID"]/df_ex4["ID"].sum())*100
            df_ex4.columns = ["Cidade","Densidade_de_trafego","Pedidos","percentual"]
            fig_g3 = px.scatter(df_ex4, x="Cidade",y="Densidade_de_trafego", size = "Pedidos", color = "Cidade")
            st.plotly_chart(fig_g3, user_container_width = True)
with tab2:
    with st.container():
         st.markdown ( "# Teste 02" )
         df["semanas"] = df["Order_Date"].dt.strftime( "%U" )
         df_ex2 = df.loc[:,["ID","semanas"]].groupby("semanas").count().reset_index()
         fig_4 = px.line(df_ex2, x ="semanas",y="ID")
         st.plotly_chart(fig_4, user_container_width = True)
    with st.container():
        df["semanas"] = df["Order_Date"].dt.strftime( "%U" )
        df_ex5 = df.loc[:,["ID","semanas"]].groupby("semanas").count().reset_index()
        df_ex5_1 = df.loc[:,["Delivery_person_ID","semanas"]].groupby("semanas").nunique().reset_index()
        df_ex5_1_1 = pd.merge( df_ex5,df_ex5_1,how='inner' )
        df_ex5_1_1["pedidos_por_entregador_por_semana"] = df_ex5_1_1["ID"]/df_ex5_1_1["Delivery_person_ID"]
        fig_6 = px.line(df_ex5_1_1, x="semanas",y="pedidos_por_entregador_por_semana")
        st.plotly_chart(fig_6, user_container_width = True) 
with tab3:
    st.markdown ( "# Teste 03" )
    df_city_new = df["City"] != "NaN "
    df_Road_traffic_density_new = df["Road_traffic_density"] != "NaN "
    df = df.loc[df_city_new,:]
    df = df.loc[df_Road_traffic_density_new,:]
    df_ex6_1 = df.loc[:,["City","Road_traffic_density","Delivery_location_latitude","Delivery_location_longitude"]].groupby(["City","Road_traffic_density"]).median().reset_index()
    mapa = folium.Map(zoom_start=11)
    for i,j in df_ex6_1.iterrows():
        folium.Marker([j["Delivery_location_latitude"],j["Delivery_location_longitude"]],popup=j[["City","Road_traffic_density"]] ).add_to(mapa)
    folium_static(mapa, width=1024, height=600)