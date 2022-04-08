# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 12:30:29 2022

@author: 123
"""


import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import base64
from streamlit_option_menu import option_menu
from  PIL import Image


st.set_page_config(layout = 'wide')




#Importar bases de de datos de incidencia delicitva
idelic_1 = pd.read_csv('Bases/idelic_1.csv')
envipe19_1= pd.read_csv('Bases/envipe19_1.csv')
envipe20_1= pd.read_csv('Bases/envipe20_1.csv')


with st.sidebar:

    st.info('''Elaborado por:
            Emmanuel Bolivar, Maria Clara Salazar, y Verónica García''')
    
    bandera = Image.open('Imagenes/bandera.png')

    st.image(bandera, width=300)
        
    
    menu = option_menu('Secciones', ["↗️ Evolución de la criminalidad", "🥷🏻 Delincuentes", "👨‍👩‍👧‍👦 Víctimas", '☑️Conclusiones'],
    icons=['cat', 'cat', "cat", 'cat'], 
    menu_icon="cast", default_index=0, orientation="vertical",
    styles={
                "container": {"padding": "0!important", "background-color": "#F2D7D5"},
                "icon": {"color": "orange", "font-size": "25px"}, 
                "nav-link": {"font-size": "23px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "brown"},
            }
        )

if menu == "↗️ Evolución de la criminalidad":

    
    #Detalles del dashborad

    st.markdown(""" <style> .font {
     font-size:25px ; font-family: 'Cooper Black'; color: #943126;} 
     </style= 'text-align: center > """, unsafe_allow_html=True)

    st.markdown("<h1 style ='text-align: center; color:#196F3D;'>Incidencia delictiva en México: Factores relevantes 👤💰🔫 </h1>", unsafe_allow_html =True)

    st.markdown("<h2 style ='text-align: center; color:#943126;'>Contextualización </h2>", unsafe_allow_html =True)

    st.markdown("La delincuencia es una problemática bastante común en el mundo, tanto así que se ha llegado a normalizar en latinoamérica. En este caso específicamente, en el año 2020 se identificó que seis de las 10 ciudades más peligrosas del mundo se encuentran en México, de acuerdo con el Consejo Ciudadano para la Seguridad Pública y la Justicia Penal (CCSPJP)."
                " Es por ello, que se hace muy necesario encontrar la manera óptima de disminuir los niveles de delincuencia y percepción de seguridad en este país, que es precisamente para lo que sirve el análisis de esta situación, encontrando los principales factores que influyen en la ocurrencia de la inseguridad por la que atraviesa actualmente México", unsafe_allow_html =True)

    c1, c2, c3 = st.columns(3)
    delito = Image.open('Imagenes/delito.jpg')
    c2.image(delito, width=400)
    
    st.markdown("<h2 style ='text-align: center; color:#943126;'>Análisis de la incidencia delictiva </h2>", unsafe_allow_html=True)    
    
    c1, c2, c3 = st.columns(3)
    entidad = Image.open('Imagenes/entidades.gif')

    c2.image(entidad, width=400)
    
    c1, c2 = st.columns([2,1])
    
   
    with c1:
        st.markdown("<h3 style='text-align: center; color: #943126;'>Pareto de casos en entidades de México </h3>", unsafe_allow_html=True)

        
        #filtrar la base de datos
        idelic_2=idelic_1.groupby(['año', 'mes', 'entidad'])[['value']].sum().reset_index()
    
        
        #Cambiar el tipo de dato
        
        idelic_2['entidad']= idelic_2['entidad'].astype('category')
        idelic_2['año']= idelic_2['año'].astype('str')
        idelic_2['mes']= idelic_2['mes'].astype('str')
        
        #Unir fechas
        idelic_2['fecha'] = pd.to_datetime(idelic_2['año'] + '-' + idelic_2['mes'], format='%Y-%m').dt.strftime('%Y-%m')
        #Convertir columna fecha de obj a datetime
        idelic_2['fecha']=pd.to_datetime(idelic_2['fecha'])
        
        #Crear un dataframe con todas las fechas
        df= pd.DataFrame(pd.date_range(start=idelic_2['fecha'].min(), end=idelic_2['fecha'].max())).rename(columns ={0:'fecha'})
        df.head()
        
        #Unir las bases de datos
        idelic_a= pd.merge(df, idelic_2, on ='fecha', how ='left')
        
        #filtrar la base de datos
        idelic_3a=idelic_a.groupby(['entidad'])[['value']].sum().sort_values('value', ascending=False)
        idelic_3a['ratio'] = idelic_3a.apply(lambda x: x.cumsum()/idelic_3a['value'].sum())
        
        #pareto para saber cuales son las entidades con más casos

        # definir figura
        fig = go.Figure([go.Bar(x=idelic_3a.index, y=idelic_3a['value'], yaxis='y1', name='sessions id'),
                         go.Scatter(x=idelic_3a.index, y=idelic_3a['ratio'], yaxis='y2', name='casos de criminalidad', hovertemplate='%{y:.1%}', marker={'color': '#845422'})])
        
        # agregar detalles
        fig.update_layout(template='plotly_white', showlegend=False, hovermode='x', bargap=.3,
                          title={'text': '<b>Pareto casos de criminalidad por entidad federativa<b>', 'x': .5}, 
                          yaxis={'title': 'Casos'},
                          yaxis2={'rangemode': "tozero", 'overlaying': 'y', 'position': 1, 'side': 'right', 'title': 'ratio', 'tickvals': np.arange(0, 1.1, .2), 'tickmode': 'array', 'ticktext': [str(i) + '%' for i in range(0, 101, 20)]},
                          width=600, 
                          height=450)

        st.plotly_chart(fig)
    with c2:
        st.metric(label="Entidad", value="MEX", delta="524.599")
        st.metric(label="Entidad", value="GTO", delta="134.883")
        st.metric(label="Entidad", value="B.C", delta="123.693")
        
    st.markdown("<h3 style='text-align: center; color: #943126;'>Evolución anual de la incidencia delictiva en diferentes entidades de México </h3>", unsafe_allow_html=True)
        
        
    c1, c2 = st.columns([1,1])

    with c1:
        

        #Filtrar
        #filtrar la base de datos
        idelic_3=idelic_a.groupby(['fecha','entidad'])[['value']].sum().reset_index().sort_values(['fecha','value'], ascending=[True, False])
        # idelic_3.sort_values('value',ascending= False)
        
        for i in ['México$','Guanajuato','Baja California$','Jalisco']:
          df1=idelic_3[idelic_3['entidad'].str.contains(i)].reset_index()
          df=pd.concat([df,df1])  
                
        #Crear columna año
        df['año']=df['fecha'].dt.year
        
        #agrupar casos por año y por entidad
        df=df.groupby(['año','entidad'])[['value']].sum().reset_index().sort_values(['año','value'], ascending=[True, False])
        df=df.replace(0,np.nan)
        df=df.dropna()
        
        #Gráfico por año
        fig = px.line(df, x= 'año', y ='value', color= 'entidad',
                      color_discrete_sequence=px.colors.qualitative.Dark2, width=600, height =470)
      
        # agregar detalles
        fig.update_layout(
            template = 'simple_white',
            title_x = 0.2,
            legend_title = 'Entidad',
            xaxis_title = '<b>Años<b>',
            yaxis_title = '<b>Cantidad de casos<b>',
            width=560, 
            height=350
        )
    
        st.plotly_chart(fig)
        

        
    with c2:
        # crear gráfica
        fig = px.bar(df, x = 'año', y='value', color = 'entidad',
                     color_discrete_sequence=px.colors.qualitative.Dark2)
        
        # agregar detalles a la gráfica
        fig.update_layout(
            xaxis_title = 'Años',
            yaxis_title = 'Cantidad de casos',
            template = 'simple_white',
            title_x = 0.5,
            width=560, 
            height=350)
        st.plotly_chart(fig)
        
        
    st.info('En la mayoría de casos la incidencia delictiva se mantuvo constante en las entidades federativas entre los años de 2015 a 2018. Después, a partir del  2019 hasta 2021 hubo un aumentó en la ocurrencia de crímenes.El panorama para la gran mayoría de entidades federales es devastador, especialmente para el Estado de México, Guanajuato, Ciudad de México, Jalisco, y Baja California.')
     
        
    st.markdown("<h3 style ='text-align: center; color:#943126;'>Jornada más frecuente </h3>", unsafe_allow_html=True)     
    
    c1,c2= st.columns([1,3])
    
    #Agrupar por año y jornada 2019
    envi19= envipe19_1.groupby(['año','jornada'])[['tipo_delito']].count().sort_values('tipo_delito',ascending=False).reset_index()
    
    #Agrupar por año y jornada 2020
    envi20= envipe20_1.groupby(['año','jornada'])[['tipo_delito']].count().sort_values('tipo_delito',ascending=False).reset_index() 

    #Concatenar los datos agrupados
    envipeT= pd.concat([envi19,envi20]).rename(columns={'tipo_delito':'cantidad'}) 
    
    #Convertir la variable en string
    envipeT["año"] = envipeT["año"].astype('str')
    
    #Graficar
    fig = px.scatter(envipeT, x = 'jornada', y='cantidad', color='año', hover_name='año', labels= 'año', title= '<b>Tipo de jornada<b>',
                     size ='cantidad', width=1000, height= 670,size_max = 40, )
    with c1:
        st.text_area('Interpretación', '''
            Según el resultado obtenido, se puede evidenciar que en México en las horas de la tarde, es decir, entre las 12:01h a 18:00h, se presentan más delitos, seguido de la jornada de la noche. Además, la ocurrencia de delitos entre el 2019 y 2020 realmente no tuvo mucha variación, especialmente en las jornadas de la tarde y la mañana. Pero, en general, sucedieron más crímenes en el año 2020.
            ''', height=350)       
    with c2:
        # agregar detalles a la gráfica
        fig.update_layout(
            xaxis_title = '<b>Tipo de jornada <b>',
            yaxis_title = '<b>Cantidad de delitos<b>',
            template = 'simple_white',
            title_x = 0.5,
            width=600, 
            height=450)
        
        st.plotly_chart(fig)
    

        
elif menu == "🥷🏻 Delincuentes":
    
    st.markdown("<h2 style ='text-align: center; color:#943126;'>Caracterización de los delincuentes </h2>", unsafe_allow_html=True)     
    
    c1, c2, c3 = st.columns(3)
    delincuente = Image.open('Imagenes/delincuente.jpg')

    c2.image(delincuente, width=300)
    
    #LLenar los vacíos
    envi19_3 =envipe19_1[['tipo_delito','edad_victima','edad_delincuente']].fillna('no sabe/no responde')
    envi20_3 =envipe20_1[['tipo_delito','edad_victima','edad_delincuente']].fillna('no sabe/no responde')
    
    #Reemplazar valores del año 2019
    envi19_3['edad_delincuente'] = envi19_3['edad_delincuente'].replace({'nan': 'no sabe/no responde'})
    envi19_3['edad_delincuente'] = envi19_3['edad_delincuente'].replace({'No sabe/no responde': 'no sabe/no responde'})
    envi19_3['edad_delincuente'] = envi19_3['edad_delincuente'].replace({'De varias edades': 'no sabe/no responde'})
    envi19_3['edad_delincuente'] = envi19_3['edad_delincuente'].replace({'De 26 a 35 años': '26-35'})
    envi19_3['edad_delincuente'] = envi19_3['edad_delincuente'].replace({'De 36 a 45 años': '36-45'})
    envi19_3['edad_delincuente'] = envi19_3['edad_delincuente'].replace({'De 18 a 25 años': '18-25'})
    envi19_3['edad_delincuente'] = envi19_3['edad_delincuente'].replace({'De 46 a 60 años': '46-60'})
    envi19_3['edad_delincuente'] = envi19_3['edad_delincuente'].replace({'De 12 a 17 años': '12-17'})
    envi19_3['edad_delincuente'] = envi19_3['edad_delincuente'].replace({'Menores de 12 años': '0-12'})
    envi19_3['edad_delincuente'] = envi19_3['edad_delincuente'].replace({'Más de 60 años': '61-97'})
    
    #Reemplazar valores del año 2020
    envi20_3['edad_delincuente'] = envi20_3['edad_delincuente'].replace({'nan': 'no sabe/no responde'})
    envi20_3['edad_delincuente'] = envi20_3['edad_delincuente'].replace({'No sabe/no responde': 'no sabe/no responde'})
    envi20_3['edad_delincuente'] = envi20_3['edad_delincuente'].replace({'De varias edades': 'no sabe/no responde'})
    envi20_3['edad_delincuente'] = envi20_3['edad_delincuente'].replace({'De 26 a 35 años': '26-35'})
    envi20_3['edad_delincuente'] = envi20_3['edad_delincuente'].replace({'De 36 a 45 años': '36-45'})
    envi20_3['edad_delincuente'] = envi20_3['edad_delincuente'].replace({'De 18 a 25 años': '18-25'})
    envi20_3['edad_delincuente'] = envi20_3['edad_delincuente'].replace({'De 46 a 60 años': '46-60'})
    envi20_3['edad_delincuente'] = envi20_3['edad_delincuente'].replace({'De 12 a 17 años': '12-17'})
    envi20_3['edad_delincuente'] = envi20_3['edad_delincuente'].replace({'Menores de 12 años': '0-12'})
    envi20_3['edad_delincuente'] = envi20_3['edad_delincuente'].replace({'Más de 60 años': '61-97'})
    

    #Agrupar por edad del delincuente
    envi19_5= envi19_3.groupby(['edad_delincuente'])[['tipo_delito']].count().reset_index().rename(columns={'tipo_delito':'cantidad'})
    envi20_5= envi20_3.groupby(['edad_delincuente'])[['tipo_delito']].count().reset_index().rename(columns={'tipo_delito':'cantidad'})
    
    #Concatenar edad de los delincuentes
    envipeE_1 = pd.concat([envi19_5,envi20_5], axis = 0)
    
    # Agrupar por rango de edad
    enviE_1= envipeE_1.groupby(['edad_delincuente'])[['cantidad']].sum().reset_index().rename(columns={'edad_delincuente':'rango_edad_delincuente'})
    enviE_1.sort_values('cantidad',ascending=False)
    
     
    st.markdown("<h3 style ='text-align: center; color:#196F3D;'>Edad de los delincuentes </h3>", unsafe_allow_html=True)     
    
    c1,c2 = st.columns([2,1])
    
    with c1:
            
        #Graficar
        fig= px.bar(enviE_1, x='rango_edad_delincuente', y='cantidad', title = 'Rango edad de los delincuentes')
        
        # agregar detalles
        fig.update_layout(
            template = 'simple_white',
            title_x = 0.5,
            xaxis_title = '<b>Años<b>',
            yaxis_title = '<b>Cantidad<b>',
            width=600, 
            height=450
        )
    
        st.plotly_chart(fig)
        
    with c2:
            
        st.text_area('Interpretación', '''
        Cabe aclarar que en la mayoría de casos no se supo con certeza qué edad tenían los delincuentes; sin embargo, en los que sí se pudieron catalogar se observa que el rango de edad mayormente identificado fue de 26 a 35 años, seguido por 36 a 45 años, y en una mínima cantidad los delincuentes eran menores de 12 años
        ''', height=350)
        

    st.markdown("<h3 style ='text-align: center; color:#196F3D;'>Género de los delincuentes </h3>", unsafe_allow_html=True)     
            
    c1, c2 = st.columns(([2,1]))
    
    # Cuál fue el género más común en los delincuentes y cambia de acuerdo al tipo de delito? 
    generoA=idelic_1[['año','entidad','tipo de delito','sexo','clave_ent']]
    generoA=generoA.astype(str)
    
    inc19= generoA[generoA['año'].str.contains('19$')]#Buscar los datos del 2019
    inc20=generoA[generoA['año'].str.contains('20$')]#Buscar los datos del 2020
    incgen=pd.concat([inc19,inc20])#Concatenar las bases del 2019 y 2020
    
    #Agrupar por sexo
    incgen1=incgen.groupby(['sexo'])[['año']].count()
    incgen1= incgen1.rename(columns = {'año':'total_casos'})
    
    #Se crea una función para varias columnas
    
    def funcion5(fila):
      if fila['delincuente_hombre'] == 'Hombre':
        valor = 'Hombre'
      elif fila['delincuente_mujer'] == 'Mujer':
        valor = 'Mujer'
      else:
        valor='No identificado'
      return valor
    
    #Crear columna de genero victimario en bases de envipe 2019 y 2020
    envipe19_1['genero_victimario']=envipe19_1.apply(funcion5,axis=1)
    envipe20_1['genero_victimario']=envipe20_1.apply(funcion5,axis=1)
    
    #Agrupar
    envipe19gen=envipe19_1.groupby(['genero_victimario'])[['edad_delincuente']].count()
    envipe19gen= envipe19gen.rename(columns = {'edad_delincuente':'total_casos'})
    envipe20gen=envipe20_1.groupby(['genero_victimario'])[['edad_delincuente']].count()
    envipe20gen= envipe20gen.rename(columns = {'edad_delincuente':'total_casos'})
    
    #juntar bases
    generom=pd.concat([incgen1,envipe19gen,envipe20gen],axis=1)
    generom['Total']=generom.sum(axis=1)
    generom=generom[['Total']]
    generom=generom.reset_index().rename(columns={'index':'genero'})
    
    #Grafica del genero más común en los delicuentes en los años 2019-2020
    fig = px.pie(generom,values = 'Total',names ='genero',
                 title= '<b>Género más común en delincuentes<b>',
                 color_discrete_sequence=px.colors.qualitative.Vivid)
    
    # agregar detalles
    fig.update_layout(
        template = 'simple_white',
        title_x = 0.47,
        legend_title = 'Género:',
        width=600, 
        height=450
        
    )
    
    c1.write(fig)
    
    c2.info('Como se muestra anteriormente, es mucho más común que los delincuentes sean hombres, con un 66.2%')
    
    #Agrupar por genero y delito
    
    c1, c2 = st.columns(([1,3]))
    
    diccincg={'Extorsión':'extorsion','Otros delitos contra la sociedad':'otros delitos','Lesiones':'daño fisico',
              'Secuestro':'secuestro'}
    
    incgen2=incgen.groupby(['tipo de delito','sexo'])[['año']].count().reset_index()
    incgen2= incgen2.rename(columns = {'año':'total_casos'})
    incgen2['tipo de delito']=incgen2['tipo de delito'].replace(diccincg)
    
    envipe19gen2=envipe19_1.groupby(['tipo_delito','genero_victimario'])[['edad_delincuente']].count().reset_index().sort_values('tipo_delito')
    envipe19gen2= envipe19gen2.rename(columns = {'edad_delincuente':'total_casos'})
    
    envipe20gen2=envipe20_1.groupby(['tipo_delito','genero_victimario'])[['edad_victima']].count().reset_index().sort_values('tipo_delito')
    envipe20gen2= envipe20gen2.rename(columns = {'edad_victima':'total_casos'})
    envipe20gen2= envipe20gen2.rename(columns = {'genero_victimario':'genero_victimario2'})
    envipe20gen2= envipe20gen2.rename(columns = {'tipo_delito':'tipo_delito2'})
    
    env=pd.concat([envipe19gen2,envipe20gen2],axis=1)
    env=env.dropna()
    env=env[['genero_victimario','total_casos','tipo_delito']]
    env=env.set_index(['genero_victimario','tipo_delito'])
    env['Total']=env.sum(axis=1)
    env=env[['Total']].reset_index().sort_values(['Total'], ascending=[False])
    
    # crear gráfica
    fig = px.bar(env, x = 'tipo_delito', y='Total', color = 'genero_victimario', 
                 title= '<b>Género del criminal por delito<b>',
                 color_discrete_sequence=px.colors.qualitative.Dark2)
    
    # agregar detalles a la gráfica
    fig.update_layout(
        xaxis_title = 'Tipo de delito',
        yaxis_title = 'Cantidad delitos',
        template = 'simple_white',
        title_x = 0.5)
    
    
    with c1:
        st.info('El sexo del victimario sigue siendo más marcado por la presencia del género masculino, excepto los crímenes de robo de accesorios de vehículos y robo total de vehículos, ya que estas artimañas, tal parece que son más comunmente cometidas por mujeres')
    with c2: 
        st.plotly_chart(fig)
    
    ##armas
    st.markdown("<h3 style ='text-align: center; color:#196F3D;'>Tipo de arma más usada </h3>", unsafe_allow_html=True)     
      
    idelic_5= idelic_1[idelic_1.modalidad.str.contains('arma|elemento')]#Buscar tipo de arma
    
    #Agrupar por modalidad y año 
    idelic_6 = idelic_5.groupby(['modalidad', 'año'])[['tipo de delito']].count().reset_index().rename(columns={'modalidad':'tipo_de_arma', 'tipo de delito':'cantidad'})  

    #Tabla resumida
    pv_tbl_1=pd.pivot_table(idelic_6, values='cantidad', index='tipo_de_arma', columns= 'año', aggfunc='sum').reset_index()
    pv_tbl_1.columns.name= None
    
    c1,c2= st.columns([2,1])
    
    with c1:
        st.table(pv_tbl_1)
        

        #Graficas
        fig = px.area(idelic_6, x = 'año', y ='cantidad', color = 'tipo_de_arma',
                     title= '<b>Tipo de arma usada en los delitos que ocurren en México por año<b>',
                     color_discrete_sequence=px.colors.qualitative.Alphabet)
        
        fig.update_layout(
            xaxis_title = 'Año',
            yaxis_title = 'Cantidad de delitos',
            template = 'simple_white',
            title_x = 0.5,
            legend_title = 'Tipo de arma:',
            width=600, 
            height=450)
        
        st.plotly_chart(fig)
        
    with c2:
        st.success('En México lo más común es que los delincuentes usen en mayor medida armas de fuego en lugar de armas blancas para cometer un delito, sin embargo, las víctimas afirmaron que su victimario usaba cualquier otro elemento que no pudieron identificarlo')
        
    ##efectos
    st.markdown("<h3 style ='text-align: center; color:#196F3D;'>Efecto bajo el cual se percibió al delincuente</h3>", unsafe_allow_html=True)     
    
    c1,c2= st.columns([1,2])
    #Año 2019
    ef19 = envipe19_1[generoA['año'].str.contains('19$')].reset_index()#Buscar el año 2019
    ef19=ef19[['tipo_delito','entidad','alguna_droga','alcohol']]#Tomar las columnas de interes para resumir tabla
    
    #Crear funcion para crear columna de efecto
    def funcion8(fila):
      if fila['alguna_droga'] == 'Si' and fila['alcohol'] == 'Si':
        valor = 'drogado y alcoholizado'
      elif fila['alguna_droga'] == 'Si':
        valor = 'drogado' 
      elif fila['alcohol'] == 'Si':
        valor = 'alcoholizado'
     
      else:
        valor=np.NAN
      return valor
 
    ef19['Efectos']=ef19.apply(funcion8,axis=1) #Aplicar la función
    ef19=ef19.dropna(subset=['Efectos']) #Borrar los vacíos de la columna efectos
    
    #Agrupar por efectos
    ef19=ef19.groupby(['Efectos'])[['alcohol']].count().reset_index()
    ef19= ef19.rename(columns = {'alcohol':'total_casos'})
    ef19['año']='2019'#Crear columna de año
    ef19['efecto']=ef19.apply(lambda x: str(x['Efectos']),axis=1)
    ef19=ef19[['efecto','total_casos','año']]
    
    #Año 2020
    ef20=envipe20_1[generoA['año'].str.contains('20$')].reset_index() #Buscar año 2020
    ef20=ef20[['tipo_delito','entidad','alguna_droga','alcohol']]#Tomar columnas de interés
    ef20['Efectos']=ef20.apply(funcion8,axis=1)#Aplicar función
    ef20=ef20.dropna(subset=['Efectos'])#Borrar los nulos de la columna efectos
    ef20=ef20.groupby(['Efectos'])[['alcohol']].count().reset_index()
    ef20= ef20.rename(columns = {'alcohol':'total_casos'})
    ef20['año']='2020'
    ef20['efecto']=ef20.apply(lambda x: str(x['Efectos']),axis=1)
    ef20=ef20[['efecto','total_casos','año']]
    
    #Concatenar 
    tot=pd.concat([ef19,ef20]).sort_values('total_casos', ascending = False)
    
    #Grafica
    fig = px.histogram(tot, x="efecto", y="total_casos",
                 color='año', barmode='group', color_discrete_sequence=px.colors.qualitative.Pastel, title='<b>Efectos bajo los cuales se percibieron a los delincuentes entre 2019-2020<b>')
    
    # agregar detalles a la gráfica
    fig.update_layout(
        xaxis_title = '<b>Efectos<b>',
        yaxis_title = '<b>Número de Casos<b>',
        template = 'simple_white',
        title_x = 0.5,
        width=600, 
        height=450)
    
    with c1:
        st.warning('Los delincuentes se percibieron  en gran medida, bajo los efectos de las drogas en ambos años. Además, se puede ver una drástica caída en todos los casos de un año a otro lo cual puede atribuirse a la pandemia, donde las personas estuvieron en sus casas gran parte del año 2020')    
    with c2:
        st.plotly_chart(fig)

elif menu== "👨‍👩‍👧‍👦 Víctimas":
    st.markdown("<h2 style ='text-align: center; color:#943126;'>Caracterización de las víctimas </h2>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    victima = Image.open('Imagenes/victima.jpg')

    c2.image(victima, width=300)
    
    #LLenar los vacíos
    envi19_3 =envipe19_1[['tipo_delito','edad_victima','edad_delincuente']].fillna('no sabe/no responde')
    envi20_3 =envipe20_1[['tipo_delito','edad_victima','edad_delincuente']].fillna('no sabe/no responde')
        
    #Reemplazar valores del año 2019
    envi19_3['edad_delincuente'] = envi19_3['edad_delincuente'].replace({'nan': 'no sabe/no responde'})
    envi19_3['edad_delincuente'] = envi19_3['edad_delincuente'].replace({'No sabe/no responde': 'no sabe/no responde'})
    envi19_3['edad_delincuente'] = envi19_3['edad_delincuente'].replace({'De varias edades': 'no sabe/no responde'})
    envi19_3['edad_delincuente'] = envi19_3['edad_delincuente'].replace({'De 26 a 35 años': '26-35'})
    envi19_3['edad_delincuente'] = envi19_3['edad_delincuente'].replace({'De 36 a 45 años': '36-45'})
    envi19_3['edad_delincuente'] = envi19_3['edad_delincuente'].replace({'De 18 a 25 años': '18-25'})
    envi19_3['edad_delincuente'] = envi19_3['edad_delincuente'].replace({'De 46 a 60 años': '46-60'})
    envi19_3['edad_delincuente'] = envi19_3['edad_delincuente'].replace({'De 12 a 17 años': '12-17'})
    envi19_3['edad_delincuente'] = envi19_3['edad_delincuente'].replace({'Menores de 12 años': '0-12'})
    envi19_3['edad_delincuente'] = envi19_3['edad_delincuente'].replace({'Más de 60 años': '61-97'})
    
    #Reemplazar valores del año 2020
    envi20_3['edad_delincuente'] = envi20_3['edad_delincuente'].replace({'nan': 'no sabe/no responde'})
    envi20_3['edad_delincuente'] = envi20_3['edad_delincuente'].replace({'No sabe/no responde': 'no sabe/no responde'})
    envi20_3['edad_delincuente'] = envi20_3['edad_delincuente'].replace({'De varias edades': 'no sabe/no responde'})
    envi20_3['edad_delincuente'] = envi20_3['edad_delincuente'].replace({'De 26 a 35 años': '26-35'})
    envi20_3['edad_delincuente'] = envi20_3['edad_delincuente'].replace({'De 36 a 45 años': '36-45'})
    envi20_3['edad_delincuente'] = envi20_3['edad_delincuente'].replace({'De 18 a 25 años': '18-25'})
    envi20_3['edad_delincuente'] = envi20_3['edad_delincuente'].replace({'De 46 a 60 años': '46-60'})
    envi20_3['edad_delincuente'] = envi20_3['edad_delincuente'].replace({'De 12 a 17 años': '12-17'})
    envi20_3['edad_delincuente'] = envi20_3['edad_delincuente'].replace({'Menores de 12 años': '0-12'})
    envi20_3['edad_delincuente'] = envi20_3['edad_delincuente'].replace({'Más de 60 años': '61-97'})
    
    #Agrupar por edad de la víctima
    envi19_4= envi19_3.groupby(['edad_victima'])[['tipo_delito']].count().reset_index().rename(columns={'tipo_delito':'cantidad'})
    envi20_4= envi20_3.groupby(['edad_victima'])[['tipo_delito']].count().reset_index().rename(columns={'tipo_delito':'cantidad'})

    #Agrupar por edad del delincuente
    envi19_5= envi19_3.groupby(['edad_delincuente'])[['tipo_delito']].count().reset_index().rename(columns={'tipo_delito':'cantidad'})
    envi20_5= envi20_3.groupby(['edad_delincuente'])[['tipo_delito']].count().reset_index().rename(columns={'tipo_delito':'cantidad'})
    
    #Concatenar Víctima
    envipeE = pd.concat([envi19_4,envi20_4], axis = 0).sort_values('cantidad',ascending=False)
    
    
    #Dividir la edad en categorias
    envipeE['rango_edad_victima']= pd.cut(envipeE['edad_victima'], bins=(18,25,35,45,60,97), ordered=False, labels= ['18-25','26-35','36-45','46-60','61-97'])
    
    # Agrupar por rango de edad
    enviE= envipeE.groupby(['rango_edad_victima'])[['cantidad']].sum().reset_index()
    enviE.sort_values('cantidad',ascending=False)
    
    envipeE_1 = pd.concat([envi19_5,envi20_5], axis = 0)
    # Agrupar por rango de edad
    enviE_1= envipeE_1.groupby(['edad_delincuente'])[['cantidad']].sum().reset_index().rename(columns={'edad_delincuente':'rango_edad_delincuente'})
    enviE_1.sort_values('cantidad',ascending=False)
    
    
    
    st.markdown("<h3 style ='text-align: center; color:#196F3D;'>Edad de las víctimas </h3>", unsafe_allow_html=True)     
    
    c1,c3 = st.columns([2,1])
    
    with c1:
            
    #Graficas
        fig= px.bar(enviE, x='rango_edad_victima', y='cantidad', title = '<b>Rango edad de las victimas<b>')
    #fig.add_trace(go.Bar(x=enviE_1['rango_edad_delincuente'], y=enviE_1['cantidad'],marker=dict(color=[1,2,3,4, 5, 6,7,8,9, 10], coloraxis="coloraxis")), row=1, col=1)
        #fig.add_trace(go.Bar(x=enviE['rango_edad_victima'], y=enviE['cantidad'], marker=dict(color=[1,2,3,4, 5, 6,7,8,9, 10], coloraxis="coloraxis")), row=1, col=2)

    #fig.update_xaxes(title_text="<b>Rango de edad de delincuentes<b>", row=1, col=1)
        fig.update_xaxes(title_text="<b>Rango de edad de víctimas<b>", row=1, col=2)

        fig.update_layout(
             
               coloraxis=dict(colorscale='Bluered_r'), showlegend=False,
               yaxis_title = '<b>Cantidades<b>',
               template = 'simple_white',
               title_x=0.5,
               width=600, 
               height=450)
    
        st.plotly_chart(fig)
    
    with c3:
            
        st.text_area('Interpretación', '''
        Se observa que el rango de edad mayormente identificado fue de 26 a 35 años, seguido por 36 a 45 años, y en una mínima cantidad los delincuentes eran menores de 12 años. Por otro lado, las víctimas suelen ser más vulnerables en el rango de edad de 26 a 35 años, y en menor cantidad, aunque no insignificante de 61 a 97 años.

        ''', height=350)
    
    st.markdown("<h3 style ='text-align: center; color:#196F3D;'>Género de las víctimas </h3>", unsafe_allow_html=True)     
        
    c1, c2 = st.columns(([2,1]))
    envi19_1= envipe19_1[['año','tipo_delito', 'entidad', 'sexo_victima']]#Tomar columnas de interes para acotar base de datos 2019
    

    envi20_1= envipe20_1[['año','tipo_delito', 'entidad', 'sexo_victima']]#Tomar columnas de interes para acotar base de datos 2020
    envipeV = pd.concat([envi19_1, envi20_1], axis = 0)#Concatenar bases acotadas
    
    #Agrupar por entidad y víctima
    envipeV_1= envipeV.groupby(['sexo_victima'])[['tipo_delito']].count().reset_index().rename(columns={'tipo_delito':'cantidad'})
    #envipeV.sort_values('cantidad',ascending=True)
    
    #Tabla resumida
    pv_tbl_1=pd.pivot_table(envipeV_1, values='cantidad', index=['entidad'], columns= 'sexo_victima', aggfunc='sum').reset_index().fillna(0)
    pv_tbl_1.columns.name= None
    pv_tbl_1=pd.pivot_table(envipeV_1, values='cantidad', index=['entidad'], columns= 'sexo_victima', aggfunc='sum').reset_index().fillna(0)
    pv_tbl_1.columns.name= None

    
    #Graficar
    fig = px.bar(envipeV_1, x = 'cantidad', y='sexo_victima', color='sexo_victima', orientation= 'h', hover_name='sexo_victima', labels= 'sexo_victima',
             title= '<b>Género de la víctimas por entidad federativa<b>',
             width=500, height= 370, color_discrete_sequence=px.colors.qualitative.Antique )

    # agregar detalles a la gráfica
    fig.update_layout(
        xaxis_title = '<b>Cantidad de víctimas <b>',
        yaxis_title = '<b>Entidades<b>',
        template = 'simple_white',
        title_x = 0.5)
    
    #st.plotly_chart(fig)
    with c2:
        st.info('Las personas que son más afectadas por la delincuencia en México son las mujeres con 38.855 casos registrados, no muy lejos se encuentran los hombres con 36.876 casos registrados.')
    with c1: 
        st.plotly_chart(fig)
        
    st.markdown("<h3 style ='text-align: center; color:#196F3D;'>Pareto por estrato sociodemográfico de las víctimas de todos los delitos cometidos </h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(([2,1]))
    
    estrato19=envipe19_1.groupby(['estrato'])[['sexo_victima']].count().reset_index()#Agrupar en año 2019
    estrato19= estrato19.rename(columns = {'sexo_victima':'total_casos19'})
    estrato19= estrato19.rename(columns = {'estrato':'estrato_victima19'})
    
    estrato20=envipe20_1.groupby(['estrato'])[['sexo_victima']].count().reset_index()#Agrupar en año 2020
    estrato20= estrato20.rename(columns = {'sexo_victima':'total_casos20'})
    estrato20= estrato20.rename(columns = {'estrato':'estrato_victima20'})
    
    #Concatenar los estratos de los años 2019 y 2020 
    pareto=pd.concat([estrato19,estrato20],axis=1).reset_index()
    #extrer columnas de interes
    pareto=pareto[['estrato_victima19','total_casos19','total_casos20']]
    pareto=pareto.set_index('estrato_victima19')
    pareto['total_casos']=pareto.sum(axis=1)
    #pareto=pareto.set_index('estrato_victima19')
    
    
    st.table(pareto)
   
    
   # crear base
    df0 = pareto.groupby(['estrato_victima19'])[['total_casos']].sum().sort_values('total_casos', ascending = False).rename(columns={'total_casos':'counts'})
    df0['ratio'] = df0.apply(lambda x: x.cumsum()/df0['counts'].sum())

    #definir figura
    fig = go.Figure([go.Bar(x=df0.index, y=df0['counts'], yaxis='y1', name='sessions id'),
                 go.Scatter(x=df0.index, y=df0['ratio'], yaxis='y2', name='accidentes de transito', hovertemplate='%{y:.1%}', marker={'color': '#000000'})])

    #agregar detalles
    fig.update_layout(template='plotly_white', showlegend=False, hovermode='x', bargap=.3,
                  title={'text': '<b>Pareto delitos por estrato<b>', 'x': .5}, 
                  yaxis={'title': 'accidentes'},
                  yaxis2={'rangemode': "tozero", 'overlaying': 'y', 'position': 1, 'side': 'right', 'title': 'ratio', 'tickvals': np.arange(0, 1.1, .2), 'tickmode': 'array', 'ticktext': [str(i) + '%' for i in range(0, 101, 20)]})

    st.plotly_chart(fig)
    
    st.text_area('Interpretación', '''Gracias al diagrama de pareto, se puede evidenciar que en México entre el 2019 y el 2020, lo más común es que las víctimas pertenecieran al estrato sociodemográfico medio bajo con un porcentaje de 50%, seguido por las víctimas pertenecientes al estrato medio alto con un 30%. Esto podría ser común debido a que estas zonas de estos estratos tendrían menos vigilancia y seguridad policial.

        ''', height=120)



        
elif menu=='☑️Conclusiones':
    st.balloons()
    st.title('Conclusiones')
    

    
    c1, c2= st.columns([1,1])
    c1.info('Según el análisis, se pudo evidenciar que en México los delitos ocurren con mayor frecuencia en las horas de la tarde, por lo que será necesario reforzar la seguridad en está jornada, para asegurar una mayor protección a la población vulnerable. Adicionalmente, la mitad de las víctimas pertenecen al estrato sociodemográfico medio bajo, es decir, es necesario hacer control en las zonas correspondientes a este estrato en específico, para garantizar un menor nivel de inseguridad en el país.')
    c2.success('En primera instancia se pensaba que los delitos son más frecuentes porque en México son más permisivos con respecto a la portación de armas; sin embargo, al analizar los datos, se evidencio que es muy común que los delincuentes usen cualquier otro tipo de elemento diferente a las armas, ya sea de fuego o blanca, para cometer un delito')
    c1.warning('Los delincuentes, en gran medida son identificados como hombres en un 66.2% de los casos, sobre 26.7% en los que son catalogados con sexo femenino. Contrario a lo que sucede con las víctimas, ya que estas suelen ser mujeres.')
    c2.error('Entre los años 2015 y 2021, la ocurrencia de delitos en los estados de Chihuahua, Michoacán de Ocampo, Querétaro y Zacatecas han ido aumentando, los demás estados federales están en sube y baja, pero a partir del año 2019 en la mayoría ha aumentado los casos de delitos. Las autoridades encargadas deben actuar con inmediatez, para disminuir los casos de estos lamentables sucesos, además de que algunos de ellos son lugares muy turísticos. ')
    c1.success('El crimen no discrimina edad, porque las víctimas suelen verse afectadas, sin variar mucho la edad que tengan. Además, es lamentable que se hayan presentado casos donde los delincuentes fueron menores de 12 años, ya que se consideran niños, y aunque no fue una cifra muy escandalosa, debería ser de 0, porque esto significa que desde muy temprana edad se empieza a cometer crímenes en México.')
    c2.warning('La entidad federativa Estado de México, presenta mayor ocurrencia de delitos, seguido por Guanajuato, Baja California, Jalisco, y Ciudad de México. Las entidades con menos indices de criminalidad son Nayarit, Tlaxcala, y Campeche.')
    st.error('El Estado de México y Guanajuato son dos de las entidades federativas mas turísticas del país, por eso será de vital importancia, aumentar el control de la seguridad en estos lugares.')
    
    c1, c2 = st.columns(2)
    guanajuato = Image.open('Imagenes/guanajuato.jpg')
    mexico = Image.open('Imagenes/mexico.jpg')
    c1.image(mexico, width=430)
    c2.image(guanajuato, width=400)
    
