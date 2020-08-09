import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-states.csv'
ny_data = pd.read_csv(url)
ny_data.drop('fips', axis=1, inplace=True)
ny_data.fillna(0, inplace=True) # Filling NaN's with 0's so that we are not making up any infections

cd_data = 'data/'
census_data = pd.read_csv(cd_data+'Population Estimates by State.csv', header=1)
census_data.dropna(inplace=True) # Dropping source row
census_data.columns = ['state', 'population']
census_data['population'] = pd.to_numeric(census_data['population'].str.replace(',', ''))
data = pd.merge(ny_data, census_data, on='state')


# List of states with the most confirmed_cases from highest to lowest.
# print(pd.DataFrame(data['state'].unique()))

def barh_plot(x_axis, color='black',line_data=[0], line_color='black'):
    """
    Plot horizontal bar plot with a line.
    This is to plot several bar plots and the line shows where the next
    plot will end.
    """
    plt.figure(figsize=(15,15))
    data.sort_values(x_axis, axis=0, ascending=False, inplace=True)
    plt.barh(y=data['state'], width=data[x_axis], color=color)
    plt.xticks(range(0,int(max(data[x_axis])),int(max(data[x_axis]/25))), rotation=90)
    plt.axvline(max(line_data), color=line_color)
    plt.ylabel('State')
    plt.xlabel(x_axis.replace('_',' ').title())
    plt.gca().invert_yaxis()
    plt.savefig('figures/'+'state_'+x_axis+'.png')


# __ confirmed cases plot __
barh_plot('population', line_data=data['confirmed_cases'], line_color='goldenrod')
barh_plot('confirmed_cases', color='goldenrod', line_data=data['deaths'], line_color='darkred')
barh_plot('deaths', color='darkred')


def ratio(state, column_x, column_y):
    """
    Calculates that ratio of column_x and column_y filtered by state.

        ratio = column_x / column_y
    """
    state_data = data[data['state'] == state]
    ratio = state_data[column_x]/state_data[column_y]
    return str(round(ratio.unique()[0]*100, 3))+'%'

ratio_data = {'state':data['state'].unique(), 'case_ratio':[], 'death_ratio':[]}
for state in data['state'].unique():
    ratio_data['case_ratio'].append(ratio(state, 'confirmed_cases', 'population'))

for state in data['state'].unique():
    ratio_data['death_ratio'].append(ratio(state, 'deaths', 'confirmed_cases'))

pd.DataFrame(ratio_data).to_csv(cd_data+'ratio_data.csv', index=False)
