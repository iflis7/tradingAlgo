import datetime as dt

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import xgboost as xgb

color_pal = sns.color_palette
plt.style.use('fivethirtyeight')
df = pd.read_csv('dataset/PJME_hourly.csv')

df.set_index(keys='Datetime', inplace=True)
df.index = pd.to_datetime(df.index)

# df.plot(style='.', figsize=(15, 5), color=color_pal(),
#         title='PJM East energy use in MW')


# Train / Test split
train = df.loc[df.index < '01-01-2015']
test = df.loc[df.index >= '01-01-2015']

fig, ax = plt.subplots(figsize=(15, 5))
train.plot(ax=ax, label='Training Set')
test.plot(ax=ax,  label='Testing Set')
ax.axvline(x='01-01-2015', color='black', linestyle='--')
ax.legend({"Training Set", "Testing Set"})


df.loc[(df.index > '01-01-2010') & (df.index < '01-08-2010')] \
    .plot(figsize=(15, 5), title='Week Of Data')
# plt.show()


# Feature Engineering
def create_features(df):
    """
    Create time series features based on time series index.
    """
    df = df.copy()  # Don't overwrite original data
    df['hour'] = df.index.hour
    df['dayofweek'] = df.index.dayofweek
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear
    df['dayofmonth'] = df.index.day
    df['weekofyear'] = df.index.isocalendar().week
    return df


df = create_features(df)

# Visualize our Feature / Target Relationships
#  Hourly Energy Use
fig, ax = plt.subplots(figsize=(10, 8))
sns.boxplot(data=df, x='hour', y='PJME_MW')
ax.set_title('MW by Hour')

#  Monthly Energy Use
fig, ax = plt.subplots(figsize=(10, 8))
sns.boxplot(data=df, x='month', y='PJME_MW', palette='Blues')
ax.set_title('MW by Month')
plt.show()


