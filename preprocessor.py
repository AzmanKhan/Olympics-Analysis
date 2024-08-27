import pandas as pd


def preprocess(df,region_df):
    #filter for summer Olyampics
    df = df[df['Season'] == 'Summer']
    #merge the two dataframes
    df = pd.merge(df, region_df, on='NOC',how ='left')
    #dropping duplicate 
    df.drop_duplicates(inplace=True)
    # One Hot Encoding Medal
    df = pd.concat([df, pd.get_dummies(df['Medal'])],axis =1)
    return df
