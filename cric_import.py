import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu  #navbar

st.set_page_config(layout="wide")

st.title("Cric Info App")

#loading data

df=pd.read_csv("cric_info.csv")

#-------------NAVBAR------------#

select = option_menu(
    menu_title=None,
    options=["Home","Player Analysis","Country Insights","Comparison","Data Explorer"],
    icons=["house","person","globe","bar-chart","table"],
    orientation="horizontal",
)


##-----------Home-------------

if select == "Home":

    st.title("Cricket Analysis Dashboard")

    col1,col2,col3 = st.columns(3)

    col1.metric("Total Players",df["Player"].nunique())

    col2.metric("Total Runs",df["Runs"].sum())

    col3.metric("Countries",df["Country"].nunique())

    st.dataframe(df.head())

    #---------Player Analysis-------------

elif select == "Player Analysis":
    
    st.title("Player Analysis")

    player = st.selectbox("Select Player",df["Player"])

    pdata = df[df["Player"]==player]
    df2=pdata[["Runs","Matches","innings","6s","4s","100","50","Ave","High_score"]]
    df2=df2.T.reset_index()# transpose
    st.dataframe(df2)
    fig=px.bar(df2,x="index", y=df2.columns[1],color="index")

    #values=pdata[["100","50","4s","6s"]].iloc[0]

    #fig=px.bar(
    #    x=values,
    #    y=values.index
   # )


    #fig.update_xaxes(range=[0,values.max()+20])


    #stats=["100","50","4s","6s"]

    #chart_data = (
        #pdata[stats]
        #.iloc[0]
        #.reset_index()
   # )

   # chart_data.columns = ["Stat","Value"]

   # fig=px.bar(
        #chart_data,
       # x="Stat",
       # y="Value"
    #)


    col4,col5,col6,col7=st.columns(4)
    
    total_runs=pdata["Runs"].sum()
    total_matches=pdata["Matches"]
    hundreds=pdata["100"].sum()
    sixes=pdata["6s"].sum()
    col4.metric(label="Total Runs",value=total_runs)
    col5.metric(label="Total Matches",value=total_matches)
    col6.metric(label="Total 100's",value=hundreds)
    col7.metric(label="6's",value=sixes)
    
 
    col8,col9,col10,col11=st.columns(4)

    high_score=pdata["High_score"]
    ball_faced=pdata["Ball_faced"]
    strike_rate=pdata["Strike_rate"].sum()
    Inns=pdata["Inns"]
    col8.metric(label="High_score",value=high_score)
    col9.metric(label="Ball_faced",value=ball_faced)
    col10.metric(label="Strike_rate",value=strike_rate)
    col11.metric(label="Total Inns",value=Inns)
    st.plotly_chart(fig,use_container_width=True)



#---------------Country--------------

elif select == "Country Insights":

    st.title("Country Insights")

    country_runs = df.groupby("Country")["Runs"].sum().reset_index()

    fig= px.pie(country_runs,names="Country",values="Runs") 

    st.plotly_chart(fig,use_container_width=True)

    country_select=st.selectbox("select Country",df["Country"].unique())
    cdata=df[df["Country"]==country_select]
    fig_runs=px.pie(
        cdata,
        names="Player",
        values="Runs"
    )
    st.plotly_chart(fig,use_container_width=True)
#-------------Comparison--------------------------

elif select == "Comparison":

    st.title("Player Comparison")

    players = st.multiselect(
        "Player Comparison",
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


#------------------Data Explorer-------------

elif select == "Data Explorer":
    
    st.title("Data Explorer")

    st.dataframe(df)