import numpy as np
def Medal_tally(df):
    #Counting only one medal 
    Medal_tally = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    
    Medal_tally = Medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    
    Medal_tally['total'] = Medal_tally['Gold'] + Medal_tally['Silver'] + Medal_tally['Bronze']
    
    Medal_tally['Gold'] = Medal_tally['Gold'].astype('int')
    Medal_tally['Silver'] = Medal_tally['Silver'].astype('int')
    Medal_tally['Bronze'] = Medal_tally['Bronze'].astype('int')
    Medal_tally['total'] = Medal_tally['total'].astype('int')

    return Medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')

    return years,country

def fetch_medal_tally(df,years,country):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 0
    if years == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if years =='Overall' and country != 'Overall':
        flag =1
        temp_df = medal_df[medal_df['region'] == country]
    if years !='Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == 2016]
    if years !='Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == years) & (medal_df['region']== country)]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending=True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x
def data_over_time(df,col):
    nation_over_time = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')

    nation_over_time.rename(columns={'Year':'Edition','count': col},inplace= True)
    return nation_over_time

# Most Medal Athelete
def most_successful(df,sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    x =  temp_df['Name'].value_counts().reset_index().head(15).merge(df, on='Name', how='left')[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns={'count':'Medals'},inplace =True)
    return x

def year_wise_medal_tally(df,country):
    temp_df = df.dropna(subset =['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace =True)

    new_df = temp_df[temp_df['region']==country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset =['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace =True)

    new_df = temp_df[temp_df['region']==country]

    pt = new_df.pivot_table(index= 'Sport',columns ='Year', values ='Medal',aggfunc='count').fillna(0)
    return pt

def most_successful_country_wise(df,country):
    temp_df = df.dropna(subset=['Medal'])
    
    temp_df = temp_df[temp_df['region'] == country]
    x =  temp_df['Name'].value_counts().reset_index().head(15).merge(df, on='Name', how='left')[['Name','count','Sport']].drop_duplicates('Name')
    x.rename(columns={'count':'Medals'},inplace =True)
    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset =['Name','region'])
    athletemp_df = athlete_df[athlete_df['Sport'] == 'Athletics']
    if sport != 'Overall':

        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df
    
def men_vs_women(df):
    
    athlete_df = df.drop_duplicates(subset =['Name','region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women,on = 'Year',how ='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y':'Female'},inplace=True) 
    final.fillna(0,inplace=True)
    
    return final