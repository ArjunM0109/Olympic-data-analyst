import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


athletes = pd.read_csv(r'C:\Users\acer\Desktop\Python\Data Science\Projects\2. EDA2\App\data\athlete_events.csv')
region = pd.read_csv(r'C:\Users\acer\Desktop\Python\Data Science\Projects\2. EDA2\App\data\noc_regions.csv')

def dataprocessor():
    global athletes,region
    df = pd.merge(athletes,region,on='NOC')
    df.drop_duplicates(inplace=True)
    df['Medal'].fillna('No-Medal',inplace=True)
    Summer = df[df['Season']=='Summer']
    Winter = df[df['Season']=='Winter']
    return Summer,Winter


def duplicates_row_removers(df1,df2):
    df1 = df1.drop_duplicates(subset = ['Team','NOC','Games','City','Sport','Event'])
    df2 = df2.drop_duplicates(subset = ['Team','NOC','Games','City','Sport','Event'])
    return df1,df2


def medal_tally_calculator(df):
    medal_counts = df.groupby(['NOC','Medal']).size().reset_index(name='count')
    medal_pivot = medal_counts.pivot(index='NOC',columns='Medal',values='count')
    medal_pivot.fillna(0,inplace=True)
    medal_pivot = medal_pivot.astype(int)

    if 'No-Medal' in medal_pivot.columns:
        medal_pivot.drop(columns='No-Medal',inplace=True)

    medal_pivot['total-medal'] = medal_pivot[['Gold', 'Silver', 'Bronze']].sum(axis=1)
    medal_pivot.sort_values(by=['Gold','Silver','Bronze'],ascending=False,inplace=True)
    return medal_pivot

def country_wise_search(noc, pivot_table):
    # Check if the NOC exists in the index of the pivot table
    if noc in pivot_table.index:
        details = {
            'Gold': pivot_table.loc[noc, 'Gold'],
            'Silver': pivot_table.loc[noc, 'Silver'],
            'Bronze': pivot_table.loc[noc, 'Bronze'],
            'Total-Medals': pivot_table.loc[noc, 'total-medal']
        }
        return details
    else:
        # Return None or an empty dictionary if the NOC does not exist
        print('No NOC exists!')
        return None
    


def plot_medals(year, country, df):

    medal_count = df.groupby(['Year','region','Medal']).size().unstack(fill_value=0)
    medal_count['Total Medals'] = medal_count[['Gold','Silver','Bronze']].sum(axis=1)
    medal_count = medal_count.reset_index()

    filtered_df = medal_count[(medal_count['Year'] == year) & (medal_count['region'] == country)]
    if filtered_df.empty:
        print(f"No data available for {country} in {year}.")
        return
        
    gold = filtered_df['Gold'].values[0]
    silver = filtered_df['Silver'].values[0]
    bronze = filtered_df['Bronze'].values[0]
    total_medals = filtered_df['Total Medals'].values[0]
    
    medals = [gold, silver, bronze,total_medals]
    labels = ['Gold', 'Silver', 'Bronze','Total_Medal']
    colors = ['#FFD700', '#C0C0C0', '#CD7F32','g']  # gold, silver, bronze colors
    # Plotting the medals
    plt.figure(figsize=(8, 6))
    plt.bar(labels, medals, color=colors)
    plt.title(f"{country} Medals in {year}")
    plt.xlabel("Type of Medal")
    plt.ylabel("Number of Medals")
    plt.ylim(0, max(medals) + 5)  # Add some space above the highest bar
    st.pyplot(plt)


def plot_year_progress(country, df): 

    medal_count = df.groupby(['Year','region','Medal']).size().unstack(fill_value=0)
    medal_count['Total Medals'] = medal_count[['Gold','Silver','Bronze']].sum(axis=1)
    medal_count = medal_count.reset_index()

    # Filter the DataFrame for the specified country
    filtered_df = medal_count[medal_count['region'] == country]
    
    # Plot each medal type over the years
    plt.figure(figsize=(10, 6))  # Create a new figure with a specified size
    plt.plot(filtered_df['Year'], filtered_df['Gold'], color='gold', label='Gold')
    plt.plot(filtered_df['Year'], filtered_df['Silver'], color='silver', label='Silver')
    plt.plot(filtered_df['Year'], filtered_df['Bronze'], color='brown', label='Bronze')
    plt.plot(filtered_df['Year'], filtered_df['Total Medals'], color='green', label='Total Medals')
    
    # Add legend, title, and labels
    plt.legend()
    plt.title(f"Medal Progress for {country} Over the Years")  # Use plt.title instead of plt.set_title
    plt.xlabel("Year")  # Use plt.xlabel instead of plt.set_xlabel
    plt.ylabel("Number of Medals")  # Use plt.ylabel instead of plt.set_ylabel
    
    # Display the plot
    st.pyplot(plt)
