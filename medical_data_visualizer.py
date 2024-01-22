import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
BMI = (df["weight"])/((df["height"]/100)**2)
df.insert(13, "BMI", BMI)
listofzeros = [0] * 70000
df.insert(14, "overweight", listofzeros)
df["overweight"].where(df["BMI"] < 25, other=1, inplace=True)
del df["BMI"]

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df["cholesterol"].where(df["cholesterol"] != 1, other=0, inplace=True)
df["cholesterol"].where(df["cholesterol"] == 0, other=1, inplace=True)
df["gluc"].where(df["gluc"] != 1, other=0, inplace=True)
df["gluc"].where(df["gluc"] == 0, other=1, inplace=True)


# Draw Heat Map
def draw_heat_map():
          # Clean the data
          dfh = df.drop(df[df["ap_lo"] > df["ap_hi"]].index)
          dfh = dfh.drop(dfh[dfh['height'] < dfh['height'].quantile(0.025)].index)
          dfh = dfh.drop(dfh[dfh['height'] > dfh['height'].quantile(0.975)].index)
          dfh = dfh.drop(dfh[dfh['weight'] < dfh['weight'].quantile(0.025)].index)
          df_heat = dfh.drop(dfh[dfh['weight'] > dfh['weight'].quantile(0.975)].index)
          
          # Calculate the correlation matrix
          corr = df_heat.corr()
          # Generate a mask for the upper triangle
          mask = np.triu(np.ones_like(corr))
          
          
          # Draw the heatmap with 'sns.heatmap()'
          dataplot = sns.heatmap(corr.round(decimals=1), cmap="YlGnBu", annot=True, mask=mask, cbar=False)
          
          # Set up the matplotlib figure
          fig = dataplot.get_figure()
          
          # Do not modify the next two lines
          fig.savefig('heatmap.png')
          return fig
          
  
# Draw Categorical Plot
def draw_cat_plot():
   # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
  df_cat = df.melt(id_vars="cardio", value_vars=["cholesterol", "gluc", "smoke", "alco", "active", "overweight"])


  # Draw the catplot with 'sns.catplot()'
  g = sns.catplot(x="variable", hue="value", col="cardio", data=df_cat, kind="count")


  # Get the figure for the output
  fig = g


  # Do not modify the next two lines
  fig.savefig('catplot.png')
  return fig
