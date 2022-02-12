#from matplotlib.pyplot import title
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go


st.set_page_config(page_title= "Airplane Crashes Data Visualization")

#############################################################################################################################
                # THE BELOW CODE IS TO HIDE THE MADE WITH STREAMLIT AND THE HAMBURGER MENU.
#############################################################################################################################
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
#############################################################################################################################
st.sidebar.image("Picture1.png", use_column_width=True)
st.sidebar.caption("Powered by MSBA42")

section=st.sidebar.selectbox("Go to:", ["Story", "Analysis", "Raw Data"])


#############################################################################################################################

#############################################################################################################################

# to compress the code
# padding = 0
# st.markdown(f""" <style>
#     .reportview-container .main .block-container{{
#         padding-top: {padding}rem;
#         padding-right: {padding}rem;
#         padding-left: {padding}rem;
#         padding-bottom: {padding}rem;
#     }} </style> """, unsafe_allow_html=True)


#############################################################################################################################



if section == "Story":
    # choosing a title for our web app
    st.title('Aeroflot Flight 593')
# starting with introducing the story of Aeroflot Flight 593
    st.header("Story Summary")
    st.write(" On March 23rd of the year 1994, the Aeroflot Flight 593 was heading from Moscow to Hong Kong, \
    after sometime from its take off the plane crashed into the Kuznetsk Alatau mountain range in Kemerovo Oblast killing all 75 people aboard.")
#adding a link to the youtube documentary.
    st.write("For the full story, check out this [link](https://youtu.be/LHyymJu6c4U)")
# Introducing the captain.
    st.image("Pilot.jpg","The pilot: Kudrinsky")

# Objective
    st.header("Objective of this analysis")
    st.write("In this analysis, we aim to study airplane crashes, and discover the best and worst airlines when it comes to safety.")

#############################################################################################################################

#############################################################################################################################

#############################################################################################################################

elif section == "Analysis":
    df=pd.read_csv("cleaned_airplane_crashes_with_countries.csv")
    #time series plot for the total number of fatalities over the years.
    fatalities_per_year=df.pivot_table(index="Year",values='Fatalities', aggfunc=np.sum)
    fatalities_per_year.reset_index(inplace=True)

    #time series plot for the number of ground deaths over year
    ground_per_year=df.pivot_table(index="Year",values='Ground', aggfunc=np.sum)
    ground_per_year.reset_index(inplace=True)
        
    st.title("Visualizations")
    st.header("Let's discover the pattern")
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=fatalities_per_year['Year'], y=fatalities_per_year['Fatalities'],
                    mode='lines',
                    name='Aboard Deaths'))
    fig.add_trace(go.Scatter(x=ground_per_year['Year'], y=ground_per_year['Ground'],
                     mode='lines',
                     name='Ground Deaths'))
    fig.add_annotation(x=2001, y=5641,
            text="What happened here ?!",
            showarrow=True,
            arrowhead=1)
    fig.update_layout(title={
        'text': "Fatalities and Ground Deaths over time",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        font=dict(
        family="Arial",
        size=14,
        color="Black"
    ) )
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="Deaths")
    st.plotly_chart(fig, use_container_width=True)

    st.write("It is evident that the world witnessed an increase in airplane crashes after WorldWar II, but after\
        the year 1972, the number has been decreasing despite the increase in Air Traffic.")

    ###################################################################################################################
    st.markdown("<br>", unsafe_allow_html=True)
    """
    ---
    """



    ###################################################################################################################
    st.header("Let's visualize the Fatalities per country ")
    df_by_iso= df.pivot_table(index=['iso','Country'],values=['Fatalities'], aggfunc=np.sum)
    df_by_iso.reset_index(inplace=True)
    fig_map = px.choropleth(df_by_iso, locations="iso",
                    color="Fatalities", # lifeExp is a column of gapminder
                    hover_name="Country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma)
    fig_map.update_layout(title={
        'text': "A choropleth map showing the difference in Fatalities between countries",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        font=dict(
        family="Arial",
        size=13,
        color="Black"
    ) )
    st.plotly_chart(fig_map,use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    """
    ---
    """

    ###################################################################################################################
    ###################################################################################################################
    top_operators=dict(df['Operator'].value_counts()[:10])
    list_top_operators= list(top_operators.keys())
    #subsetting the dataframe to get the data for these operators only.
    top_operators_data = df[df['Operator'].isin(list_top_operators)]
    top_operators_summary_2 = top_operators_data.pivot_table(index=['Operator'],values=['Fatalities','Ground'],aggfunc=np.sum)
    top_operators_summary_2.reset_index(inplace=True)
    st.header("Which Operator is the worst ?")
    fig_summary_2 = px.pie(top_operators_summary_2, values='Fatalities', names='Operator')
    fig_summary_2.update_traces(textposition='inside', textinfo='percent+label')
    fig_summary_2.update_layout(title={
        'text': "Pie chart showing the Fatalities by the top 10 operators",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        font=dict(
        family="Arial",
        size=13,
        color="Black"
    ) )
    st.plotly_chart(fig_summary_2,use_container_width=True)
    st.write("The pie chart above shows that when it comes to civilian airlines Aeroflot is the Worst in terms of safety\
        as it has almost 40%  of the fatalities operated by the top airliners.")
    st.markdown("<br>", unsafe_allow_html=True)
    """
    ---
    """
    #########################################################################################################################
    st.header("Let's dig deeper!")
    selected_operator=st.selectbox("Select an Operator",list_top_operators)
    top_operators_summary_2_updated = top_operators_data.pivot_table(index=['Operator','Year'],values=['Fatalities','Ground'],aggfunc=np.sum)
    top_operators_summary_2_updated.reset_index(inplace=True)
    selected_operator_summary=top_operators_summary_2_updated[top_operators_summary_2_updated['Operator']==selected_operator]
    fig_operator=go.Figure()
    fig_operator.add_trace(go.Scatter(x=selected_operator_summary['Year'], y=selected_operator_summary['Fatalities'],
                    mode='lines',
                    name='Aboard Deaths'))
    fig_operator.add_trace(go.Scatter(x=selected_operator_summary['Year'], y=selected_operator_summary['Ground'],
                    mode='lines',
                    name='Aboard Deaths'))
    title_1="Fatalities & Ground Deaths over time for planes operated by {}".format(selected_operator)
    fig_operator.update_layout(title={
        'text':title_1,
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        font=dict(
        family="Arial",
        size=14,
        color="Black"
    ) )
    fig_operator.update_layout(yaxis_range=[0,1000])
    fig_operator.update_xaxes(title_text="Year")
    fig_operator.update_yaxes(title_text="Deaths")
    st.plotly_chart(fig_operator, use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    """
    ---
    """
    #########################################################################################################################
    #########################################################################################################################
    
    st.header("Let's visualize the difference between the top operators")
    years= list(range(1926,2010,1))
    updated_summary= pd.DataFrame()
    Year_updated=[]
    Operator_updated=[]
    for operator in list_top_operators:
        Year_updated.append(years)
        Operator_updated.append([operator]*84)

    Year_updated_2 = [item for sublist in Year_updated for item in sublist]
    Operator_updated_2 = [item for sublist in Operator_updated for item in sublist]
    updated_summary['Year']= Year_updated_2  
    updated_summary['Operator']=Operator_updated_2
    top_operators_summary_2_updated_years_added = top_operators_data.pivot_table(index=['Year','Operator'],values=['Fatalities','Ground'],aggfunc=np.sum)
    top_operators_summary_2_updated_years_added.reset_index(inplace=True)
    new_df = pd.merge(updated_summary, top_operators_summary_2_updated_years_added,  how='left', left_on=['Year','Operator'], right_on = ['Year','Operator'])
    new_df.fillna(0,inplace=True)


    top_operators_summary_new = new_df.pivot_table(index=['Operator','Year'],values='Fatalities',aggfunc=np.sum)
    top_operators_summary_new.reset_index(inplace=True)
    fig_animated = px.bar(top_operators_summary_new, x="Operator", y="Fatalities", color="Operator",
        animation_frame="Year", range_y=[0,1000])
    fig_animated.update_layout(title={
        'text':"Animated barplot showing the changes in fatalities per operator over time",
        'y':0.97,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        font=dict(
        family="Arial",
        size=14,
        color="Black"
    ) )
    fig_animated.update_xaxes(title_text="")
    st.plotly_chart(fig_animated,use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    """
    ---
    """
#############################################################################################################################

    st.header("Fatalities Per Country")
    Number_Of_Fatalities=st.slider("Minimum Number Of Fatalities",0,6485)
    filtered_df_by_iso= df_by_iso[df_by_iso['Fatalities']>Number_Of_Fatalities]
    fig_scatter_geo = px.scatter_geo(filtered_df_by_iso, locations="iso",
                     size="Fatalities", # size of markers, "pop" is one of the columns of gapminder
                     )
    fig_scatter_geo.update_layout(title={
        'text': "A map showing the Fatalities within the Countries",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        font=dict(
        family="Arial",
        size=13,
        color="Black"
    ) )
    st.plotly_chart(fig_scatter_geo,use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    """
    ---
    """


    
#############################################################################################################################

#############################################################################################################################

#############################################################################################################################



elif section == "Raw Data":
    st.title("Airplane Crashes Dataset")
    st.write("Airplane Crashes and Fatalities Since 1908 (Full history of airplane crashes throughout the world, from 1908-present)")
    data_path = "cleaned_airplane_crashes_with_countries.csv"
    @st.cache
    def load_data(path):
        data = pd.read_csv(path)
        return data
    data = load_data(data_path)
    st.dataframe(data)







footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Powered by <a style='display: block; text-align: center;' href="https://www.aub.edu.lb/osb/MSBA/Pages/default.aspx"  target="_blank">MSBA42</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
