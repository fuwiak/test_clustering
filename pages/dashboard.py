import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import streamlit as st
import pandas as pd
from RFM import create_rfm_dataset, rfm_segmentation, segmentation_map

st.sidebar.title("Рассылка")

#load data
input_data = st.sidebar.file_uploader("Загрузите текстовый файл",
                                        type=["xlsx", "xls"])

def send_email(to_address, subject, message, from_address='YOUR_EMAIL@gmail.com', from_password='YOUR_PASSWORD'):
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_address, from_password)
    text = msg.as_string()
    server.sendmail(from_address, to_address, text)
    server.quit()


if input_data is None:
    st.sidebar.warning("No file uploaded.")
else:
    #load as dataframe
    df = pd.read_excel(input_data)
    st.write("Вот что вы загрузили:")
    st.dataframe(df.head(10))

    #rmf

    df = df[df['Quantity'] > 0]

    rfm = create_rfm_dataset(df)
    rfm = rfm_segmentation(rfm)
    rfm = segmentation_map(rfm)

    rfm = rfm.dropna()

    # select type of client

    #remove digits from column
    rfm['Segment'] = rfm['Segment'].str.replace('\d+', '')

    client_type = st.sidebar.selectbox("Выберите тип клиента", rfm['Segment'].unique())

    # filter by client type
    st.write("Вот клиенты, которые подходят под ваш выбор:")
    rfm = rfm[rfm['Segment'] == client_type]
    st.dataframe(rfm.head(10))

    # enter the subject and message
    subject = st.sidebar.text_input('Enter the subject of your email')
    message = st.sidebar.text_area('Enter the body of your email')

    if st.sidebar.button('Send Emails'):
        for customer_id in rfm.index:
            # assuming there is a column in your dataframe that gives you the email of the customer
            email = df[df['CustomerID'] == customer_id]['Email'].values[0]
            send_email(email, subject, message)
