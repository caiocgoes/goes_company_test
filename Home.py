import streamlit as st
from PIL import Image

st.set_page_config(page_title = "Home",page_icon="U+1F4C8", layout="wide")#função que iremos usar usar para configuração de nossa imagem 
#image_path = 'c:/Users/caioc/Documents/FACULDADE/CURSO_DATA_SCIENCE_COMUNIDADE_DS/Formação_DS/Python_para_Analise_de_Dados/Ciclo_V/Exercicios/logo.png'
#image = Image.open(image_path)
#st.sidebar.image( image,width=120)

st.sidebar.markdown('# Goes Consultorias')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.write("# Goes Consultorias - PWE Dashboard")

st.markdown("""texto com a descrição do projeto e meus contatos""")