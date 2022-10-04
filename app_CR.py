from ast import Pass
import pandas as pd
import warnings
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import dateutil.relativedelta
# from matplotlib.pyplot import axis
import numpy as np
warnings.filterwarnings("ignore")
from tqdm import tqdm
import streamlit as st
from funciones_CR import *
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import base64
import io
locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))

st.set_page_config(page_title="Auto Totalizador", page_icon="lds.png")

def main():
    choice = ['Cortes y Reconexiones','Proximamente']
    choice_value = st.sidebar.selectbox("Seleccionar el proceso", choice)

    if choice_value == 'Cortes y Reconexiones':
        st.title(choice[0])
        # fecha = st.date_input("Ingrese mes a analizar")
        # fecha = fecha.strftime('%Y-%m-01')

        uploaded_file_cxn = st.file_uploader("Elige la base de Cortes")
        uploaded_file_rcxn = st.file_uploader("Elige la base de Reconexiones")

        if uploaded_file_cxn and uploaded_file_rcxn:
            st.button("Procesar Cortes y Reconexiones")
            input_cxn = pd.read_excel(uploaded_file_cxn, header=1)
            input_rcxn = pd.read_excel(uploaded_file_rcxn, header=1)
            df_indicador, df_fin, df3 = cxn_rcxn().procesamiento_inicial(input_cxn,input_rcxn)

            st.subheader('Excel - CXN y RCXN')
            st.write('Esta aplicación te muestra un excel de análisis de Cortes y Reconexiones')

            # selection = tabla_interactiva(df=df_fin)

            towrite = io.BytesIO() #to bytes
            downloaded_file = df_fin.to_excel(towrite, encoding='latin-1', index=False, header=True) # write to BytesIO buffer
            towrite.seek(0)  # reset pointer
            b64 = base64.b64encode(towrite.read()).decode()
            towrite.close()

            # st.download_button(label='📥 Descarga Cortes y Reconexiones',
            #                                 data=df_fin ,
            #                                 file_name= 'df_test.xlsx')

            st.markdown(excel_download(df_indicador, df_fin, df3,'Cortes y Reconexiones'), unsafe_allow_html=True)

            #No sirven igual / Arroja en binario¿
            st.download_button(label='📥 Descarga Cortes y Reconexiones - NO USAR',
                                            data=b64 ,
                                            file_name= 'Cortes y Reconexiones.xls',mime='application/vnd.ms-excel.')
    
    else:
        pass


def tabla_interactiva(df: pd.DataFrame):
                options = GridOptionsBuilder.from_dataframe(
                    df, enableRowGroup=True, enableValue=True, enablePivot=True
                )

                options.configure_side_bar()

                options.configure_selection("single")
                selection = AgGrid(
                    df,
                    enable_enterprise_modules=True,
                    gridOptions=options.build(),
                    theme='streamlit',
                    update_mode=GridUpdateMode.MODEL_CHANGED,
                    allow_unsafe_jscode=True,
                )
               

                return selection
def excel_download(df,df1,df2,dfname):
    towrite = io.BytesIO() #to bytes
    with pd.ExcelWriter(towrite,engine='xlsxwriter') as writer:
    # writer = pd.ExcelWriter(towrite, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Reporte de Efectividad Diaria',encoding='latin-1', index=True, header=True)
        df1.to_excel(writer, sheet_name='BD x Operador x Día',encoding='latin-1', index=False, header=True)
        df2.to_excel(writer, sheet_name='Tiempo_Operador',encoding='latin-1', index=True, header=True)
    # downloaded_file = df3.to_excel(writer, encoding='latin-1', index=False, header=True) # write to BytesIO buffer
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode() #decodes again
    towrite.close()    
    fn = dfname + '.xlsx' 
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download= ' + fn + '>' + fn + ' / 📥 Descarga Archivo Excel</a>'
    return linko




if __name__ == '__main__':
    main()