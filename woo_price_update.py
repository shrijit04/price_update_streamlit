import streamlit as st
import pandas as pd
import numpy as np
#import os
#from zipfile import ZipFile
#import io

st.title('Price File Update')

@st.cache_data
def load_data(uploaded_file):
    #st.write(uploaded_file)
    df = pd.read_csv(uploaded_file)
    #st.write('inside fun')
    #st.write(len(df))
    return df

@st.cache_data
def transform_data(df, qt_num, markup):
    drop_list = ['Amazon', 'Walmart', 'Ebay']
    thisFilter = df.filter(drop_list)
    df.drop(columns=thisFilter, inplace=True, axis=1)

    df['MAP Minimum Advertised Pricing'] = df['MAP Minimum Advertised Pricing'].fillna(0)
    df['MAP Minimum Advertised Pricing'] = np.where(df["MAP Minimum Advertised Pricing"] == 9999, 0, df["MAP Minimum Advertised Pricing"])

    df['Price'] = np.where(df["MAP Minimum Advertised Pricing"] == 0 , df['Price'], df['MAP Minimum Advertised Pricing'])

    df = df.sort_values(by=['MAP Minimum Advertised Pricing'], ascending= False)

    df = df.drop(columns='MAP Minimum Advertised Pricing')

    df = df[df['Status'] != 'Discontinued']

    df = df[df['Quantity Available'] - qt_num > 1]

    markuplist = df['Price'] * (1 + (markup * 0.01) ) 

    df.insert(3, 'Price Markup', markuplist)

    return df

@st.cache_data
def create_csv(df, filename: str):
    csv = df.to_csv(index=False).encode('utf-8')
    return csv

#@st.cache_data
#def create_zip(csv_filelist, filename: str):

def generate_download_button(csv_data, filename):
    st.download_button(label=f"Download Modified Split File {filename} ",
                           data=csv_data,
                           file_name=f"{filename}",
                           mime='text/csv')



uploaded_file = st.file_uploader('Upload a file', type = ['csv'])


if uploaded_file is not None:

    df = load_data(uploaded_file)

    #st.write(df.info())

    qt_num = st.number_input('Quantity Check Number', min_value= 1, value=3, step=1)

    markup = st.number_input('price markup', min_value= 0)

    df = transform_data(df, qt_num, markup)

    #st.write(len(df))

    modified_csv = create_csv(df, 'modified_file.csv')


    st.download_button(
        label="Download modified CSV",
        data=modified_csv,
        file_name='modified_file.csv',
        mime='text/csv',
        key='download-csv'
    )

    split = st.checkbox('Want to Split the file')

    if split:
    
        i = st.number_input('file product count', min_value= 1, value= 500, step= 1 )
        k = 0

        #zipObj = ZipFile('sample.zip', 'w')

        #csv_files = list()

        while i*k < len(df):
            data = df[k*i:((k+1)*i)-1]
            #data.to_csv(f'product_{k}.csv', index=False).encode('utf-8')
            csv = create_csv(data, f'product_{k}.csv')
            generate_download_button(csv, f'product_{k}.csv', )
            #zipObj.write(csv)
            #csv_files.append(csv, f'product_{k}.csv')

            k = k + 1
        

        #zipObj.close()

        #for file in csv_files:
         #   os.remove(file)

        #st.download_button(
        #label="Download zip",
        #data=zipObj,
        #file_name='sample.zip',
        #mime='application/zip',
    #)


    

   