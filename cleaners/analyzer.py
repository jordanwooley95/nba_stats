import pandas as pd

data = pd.read_csv("team_averages.csv")

# normalize the data 0-1 while keeping team as a column
data = data.drop(columns=["Team"])
data = (data - data.min()) / (data.max() - data.min())
data["Team"] = data.index

# move the team column to the front
cols = data.columns.tolist()
cols = cols[-1:] + cols[:-1]
data = data[cols]


# save the data to a csv file
output = data.to_csv("team_avgs_normalized.csv", index=False)
