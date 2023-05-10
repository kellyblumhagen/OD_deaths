import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load data
df = pd.read_csv("data/ODs.csv")
data = pd.read_csv("data/Pop_Dens_2021.csv")

# Page Layout
st.set_page_config(layout="wide")
st.title('America\'s Drug Epidemic')

tab1,tab2,tab3 = st.tabs([' Overview ', ' Drug Classifications ', ' Resources ',])


### OVERVIEW ###
with tab1:
    st.subheader("DEATH-RELATED OVERDOSES")
    option = st.selectbox('Search by:', ('State', 'Region'))

    if option == 'State':
        state = st.selectbox('Select State:', df['State'].unique())
        filtered_df = df[df['State'] == state]

        # Create line graph
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_df['Year'], y=filtered_df['All_Drug_Overdose_Death_Rate'], name='ALL overdose deaths'))
        fig.add_trace(go.Scatter(x=filtered_df['Year'], y=filtered_df['Opioid_Overdose_Death_Rate'], name='OPIOD overdose deaths'))
        fig.update_traces(mode="markers+lines", hovertemplate=None)
        fig.update_layout(
                        xaxis_title='Year',
                        yaxis_title='Total Deaths',
                        hovermode="x")
        st.plotly_chart(fig, use_container_width = True)


    else:
        region_list = df["Region"].unique()
        region = st.selectbox("Select:",region_list)
        col1,col2 = st.columns(2)
        fig = px.line(df[df['Region'] == region], 
            x = "Year", y = "Opioid_Overdose_Death_Rate",
            title = "Opioid Overdose Deaths",color = "State")
        fig.update_layout(title="OPIOD overdose deaths",
                            xaxis_title='Year',
                            yaxis_title='Total Deaths',
                            legend_title='State', 
                            yaxis_range=[0,100])
        col1.plotly_chart(fig)

        fig = px.line(df[df["Region"] == region], x = "Year", y = "All_Drug_Overdose_Death_Rate",
                        title = "All Drug Overdose Deaths",color = "State")
        fig.update_layout(title="ALL DRUG overdose deaths",
                            xaxis_title='Year',
                            yaxis_title='Total Deaths',
                            legend_title='State',
                            yaxis_range=[0,100])
        col2.plotly_chart(fig)




### TAB 2 ###
with tab2:
    st.subheader("OD-Deaths Based On Drug Classification")

    # Drug categories
    drug_categories = ["Opioids", "Cocaine", "Psychostimulants_with_Abuse_Potential"]
    selected_drug = st.selectbox("Select a drug classification:", drug_categories)
    filtered_data = data[data["drug_category"] == selected_drug]

    # Sort data by score to select the top 5 states
    top_states = filtered_data.sort_values(by="score", ascending=False).head(5)

    # Create bar chart
    fig = px.bar(top_states, x="state", y="score", title=f"States with Highest Total OD-Deaths for {selected_drug}")
    fig.update_layout(xaxis_title="State", yaxis_title="OD Death Score")
    st.plotly_chart(fig)

    st.markdown('*Results have been adjusted according to each states\'s population density.')


### Resources ###
with tab3:
    st.subheader("Resources")
   
    st.markdown('Data: ')
    st.write("[CDC](https://data.cdc.gov/NCHS/VSRR-Provisional-Drug-Overdose-Death-Counts/xkb8-kh2a)")

    st.markdown('Get Help:  ')
    st.markdown("[NCDHHS: Mental Health and Substance Abuse](https://www.ncdhhs.gov/assistance/mental-health-and-substance-abuse)")

