import streamlit as st 
import pandas as pd
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)
st.sidebar.title("Olyampic Analysis")
st.sidebar.image('https://s.yimg.com/fz/api/res/1.2/FUODKXHc0PckFynvDqBBNA--~C/YXBwaWQ9c3JjaGRkO2ZpPW9wdGk7aD0xNjY7dz0xNjY-/https://s.yimg.com/cv/apiv2/default/20230504/olympicsparis.png')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall analysis', 'Country wise analysis', 'Athlete wise analysis')
)
st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header("Meadal Tally")
    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select the Year ",years)
    selected_country= st.sidebar.selectbox("Select the Country",country)
    Medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country =='Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country =='Overall':
        st.title('Medal Tally in '+ str(selected_year) + 'Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Overall Performance')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' performance in '+ str(selected_year) + ' Olympics')
    st.table(Medal_tally)


if user_menu == 'Overall analysis':
    editions = df['Year'].unique().shape[0]-1

    cities = df['City'].unique().shape[0]

    sports = df['Sport'].unique().shape[0]

    events = df['Event'].unique().shape[0]

    athletes = df['Name'].unique().shape[0]

    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)

    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Hosts")
        st.title(cities)

    with col3:
        st.header("Sports")
        st.title(sports)

    coll, col2, col3 = st.columns(3)

    with col1:
        st.header("Events")
        st.title(events)

    with col2:
        st.header('Nations')
        st.title(nations)
    
    with col3:
        st.header('Athletes')
        st.title(athletes)
    plt.figure()
    nation_over_time = helper.data_over_time(df,'region')
    plt.plot(nation_over_time['Edition'], nation_over_time['region'], marker='o')
    st.title('Participating Nation Over the Year')
    st.pyplot(plt)

    plt.figure()
    event_over_time = helper.data_over_time(df,'Event')
    plt.plot(event_over_time['Edition'], event_over_time['Event'], marker='o')
    st.title('Events Over the Year')
    st.pyplot(plt)

    plt.figure()
    athletes_over_time = helper.data_over_time(df,'Name')
    plt.plot(athletes_over_time['Edition'], athletes_over_time['Name'], marker='o')
    st.title('Athletes Over the Year')
    st.pyplot(plt)

    st.title('No of Events over time (Every Sport)')
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax= sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc ='count').fillna(0).astype('int'), annot =True)
    st.pyplot(fig)


    st.title("Most successful Athelete")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country wise analysis':

    st.sidebar.title('Country Wise Analysis')
    country_list =df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.year_wise_medal_tally(df,selected_country)
    plt.plot(country_df['Year'], country_df['Medal'], marker='o')
    st.title(selected_country +' Medal Tally over the years')
    st.pyplot(plt)

    st.title(selected_country + ' Excels in the following Sports')
    pt = helper.country_event_heatmap(df,selected_country)
    fig,ax = plt.subplots(figsize=(15,15))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)
    
    st.title('Top 10 Athlete of Selected Country')
    top10_df = helper.most_successful_country_wise(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete wise analysis':
    athlete_df =df.drop_duplicates(subset =['Name','region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()

    # Plot using sns.kdeplot
    fig, ax = plt.subplots()
    sns.kdeplot(data=x1, label='Overall Age', color='blue',ax=ax)
    sns.kdeplot(data=x2, label='Gold Medalists', color='gold',ax=ax)
    sns.kdeplot(data=x3, label='Silver Medalists', color='silver',ax=ax)
    sns.kdeplot(data=x4, label='Bronze Medalists', color='brown',ax=ax)

    # Set plot labels and titles
    ax.set(title='Age Distribution by Medal Type', xlabel='Age', ylabel='Density')
    plt.legend(title='Category')
    st.title('Distribution of Age')
    st.pyplot(fig)

    x = []
    name = []

    famous_sports =['Basketball',
 'Judo','Football','Tug-Of-War','Athletics','Swimming','Badminton','Sailing','Gymnastics','Art Competitions','Handball','Weightlifting','Wrestling','Water Polo','Hockey',
 'Rowing','Fencing','Volleyball','Equestrianism','Shooting','Boxing','Taekwondo','Cycling','Diving','Canoeing','Table Tennis','Baseball','Rubgy Sevens','Beach Volleyball',
 'Ice Hockey','Tennis','Jeu De Paume','Roque','Basque Pelota','Alpinism','Aeronautics']
   
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    
    fig, ax = plt.subplots(figsize =(10,10))
    for idx, ages in enumerate(x):
        sns.kdeplot(data=ages, label=name[idx], ax=ax)

    # Set plot labels and titles
    ax.set(title='Age Distribution by Sport (Gold Medalists)', xlabel='Age', ylabel='Density')
    ax.legend(title='Sport')
 
    st.title('Age Distribution by Sport')
    st.pyplot(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    st.title("Height Vs Weight")
    selected_sport = st.selectbox('Select a sport',sport_list)

    fig, ax = plt.subplots()

    temp_df = helper.weight_v_height(df,selected_sport)
    sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal',style=temp_df['Sex'] ,ax=ax)
    
    st.pyplot(fig)

    
    fig,ax = plt.subplots()

    final = helper.men_vs_women(df)

    st.title("Men vs Women Participation over the year")

    final_melted = pd.melt(final, id_vars='Year', value_vars=['Male', 'Female'],var_name='Gender',value_name='Count')
    sns.lineplot(data=final_melted, x='Year', y='Count',hue='Gender',ax = ax)
    st.pyplot(fig)


