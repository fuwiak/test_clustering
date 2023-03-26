import streamlit as st
import pandas as pd
# from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
# kneed
from kneed import KneeLocator
from sklearn.preprocessing import StandardScaler
from KmeansCustom import optimal_number_cluster_kmeans
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import sys
import plotly.express as px
from RFM import create_rfm_dataset,rfm_segmentation, segmentation_map

st.title("Кластеризация методом K-means")  # заголовок

def load_data():
    text_file = st.sidebar.file_uploader("Загрузите текстовый файл",
                                         type=["xlsx", "xls"])
    global df, rfm
    df = None
    if text_file is None:
        st.sidebar.warning("No file uploaded.")
    else:
        try:
            num_rows = st.sidebar.number_input(
                "Количество строк для загрузки", min_value=1, max_value=4372, value=4372)


            df = pd.read_excel(text_file, nrows=num_rows)
            df = df[df['Quantity'] > 0]

            rfm = create_rfm_dataset(df)
            rfm = rfm_segmentation(rfm)
            rfm = segmentation_map(rfm)

            rfm = rfm.dropna()


        except ValueError as e:
            st.write(e)
            # st.sidebar.error(
            #     "Неверный файл. Пожалуйста, загрузите текстовый файл.")


def main():
    load_data()
    # rfm = None
    #get local variable rfm from load_data()
    rfm = globals().get('rfm')


    if df is not None:


        st.dataframe(rfm.head(10))
    else:
        # handle the case where no file was uploaded or an invalid file was uploaded
        st.error("No file uploaded or invalid file uploaded")
        sys.exit(1)

    #multiselect columns
    columns = st.multiselect('Выберите колонки для кластеризации', rfm.columns, default=['Frequency', 'Monetary'])
    if len(columns) == 0:
        st.error("Выберите колонки для кластеризации")
        sys.exit(1)












    #max number of clusters
    max_number_cluster = st.number_input('Введите максимальное количество кластеров', min_value=2, max_value=10, value=10)

    #kmeans
    k,distortions = optimal_number_cluster_kmeans(rfm, columns, max_number_cluster)


    st.write(f"Оптимальное количество кластеров: {k}")

    #kmeans
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(rfm[columns])
    rfm['cluster'] = kmeans.labels_
    st.dataframe(rfm['cluster'].value_counts())

    #silhouette score

    st.write(f"Silhouette score: {silhouette_score(rfm[columns], kmeans.labels_)}")

    #plot
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # plot
    plt.plot(range(1, max_number_cluster), distortions, marker='o')
    # plt.title(title)
    plt.vlines(k, plt.ylim()[0], plt.ylim()[1], linestyles='dashed')
    plt.xlabel('Number of clusters')
    plt.ylabel('Distortion')
    plt.show()

    st.pyplot()

    # merge with original dataset

    rfm = rfm.merge(df, on=['CustomerID'], how='left')


    fig = px.scatter(rfm, x=columns[0], y=columns[1],
                     color="cluster", title='Кластеризация методом K-means',
                      hover_data=list(rfm.columns))

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))



    st.plotly_chart(fig)

    #st.write(df['cluster'].value_counts())


    #filter by cluster
    cluster = st.number_input('Введите номер кластера', min_value=0, max_value=k, value=0)



    st.dataframe(rfm[rfm['cluster'] == cluster])

    #save dataframe
    type_file = st.selectbox('Выберите тип файла', ['csv', 'xlsx', 'xls'])
    if st.button('Сохранить датасет'):
        if type_file == "csv":
            rfm.to_csv(f"rfm.csv", index=False)
        elif type_file in ("xlsx", "xls"):
            rfm.to_excel(f"rfm.xlsx", index=False)
        else:
            raise ValueError("Неверный тип файла.")

        st.write("Датасет успешно сохранен.")








if __name__ == "__main__":
    # load_data()
    main()
    # st.write(f"количесто строк в датасете: {df.shape[0]}")






