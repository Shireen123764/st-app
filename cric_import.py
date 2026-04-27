import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu #navbar
st.set_page_config(layout="wide") #
st.title("Cric info app")
#loading Data
df=pd.read_csv("cric_info.csv")

#---------NAVBAR------------#

select = option_menu(
    menu_title=None,
    options=["Home","Player Analysis","Country Insights","Comparison",
             "Data Explorer"],
    icons=["house","person","globe","bar-chart","table"],
    orientation="horizontal"

)

##-----------------Home--------------

if select == "Home":

    st.title("Cricket Analysis Dashboard")
    col1,col2,col3 = st.columns(3)
    col1.metric("Total Players", df["Player"].nunique())
    col2.metric("Total Runs", df["Runs"].sum())
    col3.metric("Countries", df["Country"].nunique())

    st.dataframe(df.head())


#-----------Player Analysis----------------

elif select == "Player Analysis":

    st.title("Player Analysis")
    player = st.selectbox("Select Player", df["Player"])
    pdata = df[df["Player"]==player]
    df2=pdata[["Runs","Matches","innings","6s","4s","100","50","Ave","High_score"]]
    df2=df2.T.reset_index()
    st.dataframe(df2)
    fig=px.bar(df2,x="index",y=df2.columns[1],color="index")
   

    col4,col5,col6,col7=st.columns(4)
#-------key metrics------
    total_runs=pdata["Runs"].sum()
    total_matches=pdata["Matches"]
    hundreds=pdata["100"].sum()
    sixes=pdata["6s"].sum()
    col4.metric(label="Total Runs",value=total_runs)
    col5.metric(label="Total Matches",value=total_matches)
    col6.metric(label="Total 100's",value=hundreds)
    col7.metric(label="Total 6's",value=sixes)

    st.plotly_chart(fig,use_container_width=True)



#-----------Country Analysis------------


elif select == "Country Insights":
    st.title("Country Insights")

    country_runs = df.groupby("Country")["Runs"].sum().reset_index()
    fig= px.pie(country_runs,names="Country",values="Runs")
    st.plotly_chart(fig,use_container_width=True)

   

    country_select=st.selectbox("Select Country", df["Country"].unique())
    cdata=df[df["Country"]==country_select]
    fig_runs=px.pie(
        cdata,
        names="Player",
        values="Runs"
    )

    st.plotly_chart(fig_runs,use_container_width=True)




#-------------Comparison----------------



elif select== "Comparison":

    st.title("Player Comparison")

    players=st.multiselect(
        "Compare Players",
        df["Player"],
        default=df["Player"].head(5)
    )

    compare=df[df["Player"].isin(players)]

    fig=px.scatter(
        compare,
        x="Strike_rate",
        y="Ave",
        size="Runs",
        color="Country"

    )
    st.plotly_chart(fig,use_container_width=True)


elif select == "Data Explorer":

    st.title("Data Explorer")

    st.dataframe(df)