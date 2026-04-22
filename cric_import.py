import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu # navbar (multipages) ?

st.set_page_config(layout="wide")


st.title("cric info app")

#loading data


df=pd.read_csv("cric_info.csv")
#______ navbar________

select = option_menu(
    menu_title = None,
    options = ["Home","Player Analysis","Country Insights","Comparison","Data Explorer"],
    icons=["house","person","globe","bar-chart","table"],
    orientation = "horizontal",
 )

 #=-------- home ---------
if select == "Home":
   st.title("Cricket Analysis Dashboard")
   col1,col2,col3 = st.columns(3)
   col1.metric("Total Players", df["Player"].nunique())

   col2.metric("Total Runs", df["Runs"].sum())
   col3.metric("Countries", df["Country"].nunique())

   st.dataframe(df.head())

   #------ Player Analysis-------
elif select == "Player Analysis":
    st.title("Player Analysis")
    player = st.selectbox("select player" , df["Player"])
    pdata = df[df["Player"]== player].reset_index()
    values=pdata[["100","50","4s","6s"]].iloc[0]

    fig=px.bar(
        x=values,
        y=values.index
    )
    fig.update_xaxes(range=[0,values.max()+20])


    col4,col5,col6,col7=st.columns(4)    

    total_runs=pdata["Runs"].sum()
    total_matches=pdata ["Matches"]
    hundreds= pdata ["100"].sum()
    sixes= pdata ["6s"].sum()
    #four= pdata ["4s"].sum()
    #duration = pdata ["Duration"].sum()
    #inn = pdata ["innings"]
    #High_s = pdata ["High_score"]
    col4.metric(label = "Total Runs",value=total_runs)
    col5.metric(label = "Total Matches",value=total_matches)
    col6.metric(label = "Total 100's",value=hundreds)  
    col7.metric(label = "Total 6's",value=sixes) 
    #col8.metric(label = "Total 4's",value=four)
    #col9.metric(label = "Total Duration ",value=duration)
    #col10.metric(label = "Total inning", value=inn)
    #col11.metric(label = "Total High_score",value =High_s )

    col8,col9,col10,col11=st.columns(4)
  
    four= pdata ["4s"].sum()
    High_s = pdata ["High_score"]
    inn = pdata ["innings"]
    duration = pdata ["Duration"].sum()

    col8.metric(label = "Total 4's",value=four)
    col11.metric(label = "Total High_score",value =High_s )
    col10.metric(label = "Total inning", value=inn)
    col9.metric(label = "Total Duration ",value=duration)
    st.plotly_chart(fig,use_container_width=True)#chart ki width set karega

    #---------- country ----------

elif select == "Country Insights":
    st.title("Country Insights")
    country_runs = df.groupby("Country")["Runs"].sum().reset_index()
    fig= px.pie(country_runs,names="Country", values="Runs")

    st.plotly_chart(fig,use_container_width=True)

#------ Comparison-------


elif select == "Comparison":  
   st.title(" Players Comparison")
   players = st.multiselect(
    "Comparison Players",
    df["Player"],
    default=df["Player"].head(5)
    )
   compare=df[df["Player"].isin(players)]

   fig = px.scatter(
    compare,
    x="Strike_rate",
    y= "Ave",
    size="Runs",
    color="Country"
   )   
   st.plotly_chart(fig,use_container_width=True)

   #------ Data Explorer-------

elif select == "Data Explorer" : 
    st.title("Data Explorer")
    st.dataframe(df)