import pandas as pd
import numpy as np

box_scores = pd.read_csv("output.csv")

# drop the date column
box_scores = box_scores.drop(columns=["Date"])

# drop the matchup column
box_scores = box_scores.drop(columns=["Matchup"])

# drop the wl column
box_scores = box_scores.drop(columns=["WL"])

# drop the fg% column
box_scores = box_scores.drop(columns=["FG%"])

# drop the 3p% column
box_scores = box_scores.drop(columns=["3P%"])

# drop the team column
# box_scores = box_scores.drop(columns=["Team"])

# combine the position columns that have the same letters for example C-F and F-C can be combined to C-F
# and F-G and G-F can be combined to F-G
box_scores["Position"] = box_scores["Position"].str.replace("F-C", "C-F")
box_scores["Position"] = box_scores["Position"].str.replace("G-F", "F-G")


# check for duplicates and print if any are dropped and show the dropped rows also
print("Dropping duplicates")
print(box_scores[box_scores.duplicated()])
box_scores = box_scores.drop_duplicates()


box_scores["TD"] = np.where(
    ((box_scores["Pts"] >= 10) & (box_scores["Reb"] >= 10) & (box_scores["Ast"] >= 10))
    | (
        (box_scores["Pts"] >= 10)
        & (box_scores["Reb"] >= 10)
        & (box_scores["Stl"] >= 10)
    )
    | (
        (box_scores["Pts"] >= 10)
        & (box_scores["Reb"] >= 10)
        & (box_scores["Blk"] >= 10)
    )
    | (
        (box_scores["Pts"] >= 10)
        & (box_scores["Ast"] >= 10)
        & (box_scores["Stl"] >= 10)
    )
    | (
        (box_scores["Pts"] >= 10)
        & (box_scores["Ast"] >= 10)
        & (box_scores["Blk"] >= 10)
    )
    | (
        (box_scores["Pts"] >= 10)
        & (box_scores["Stl"] >= 10)
        & (box_scores["Blk"] >= 10)
    )
    | (
        (box_scores["Reb"] >= 10)
        & (box_scores["Ast"] >= 10)
        & (box_scores["Stl"] >= 10)
    )
    | (
        (box_scores["Reb"] >= 10)
        & (box_scores["Ast"] >= 10)
        & (box_scores["Blk"] >= 10)
    )
    | (
        (box_scores["Reb"] >= 10)
        & (box_scores["Stl"] >= 10)
        & (box_scores["Blk"] >= 10)
    )
    | (
        (box_scores["Ast"] >= 10)
        & (box_scores["Stl"] >= 10)
        & (box_scores["Blk"] >= 10)
    ),
    1,
    0,
)

box_scores["DD"] = np.where(
    ((box_scores["Pts"] >= 10) & (box_scores["Reb"] >= 10))
    | ((box_scores["Pts"] >= 10) & (box_scores["Ast"] >= 10))
    | ((box_scores["Pts"] >= 10) & (box_scores["Stl"] >= 10))
    | ((box_scores["Pts"] >= 10) & (box_scores["Blk"] >= 10))
    | ((box_scores["Reb"] >= 10) & (box_scores["Ast"] >= 10))
    | ((box_scores["Reb"] >= 10) & (box_scores["Stl"] >= 10))
    | ((box_scores["Reb"] >= 10) & (box_scores["Blk"] >= 10))
    | ((box_scores["Ast"] >= 10) & (box_scores["Stl"] >= 10))
    | ((box_scores["Ast"] >= 10) & (box_scores["Blk"] >= 10))
    | ((box_scores["Stl"] >= 10) & (box_scores["Blk"] >= 10)),
    1,
    0,
)

# each pt = 1, reb = 1.2, ast = 1.5, stl = 2, blk = 2, tov = -0.5, double double = 1.5, triple double = 3
box_scores["Fpts"] = (
    box_scores["Pts"]
    + box_scores["Reb"] * 1.2
    + box_scores["Ast"] * 1.5
    + box_scores["Stl"] * 2
    + box_scores["Blk"] * 2
    - box_scores["Tov"] * 0.5
    + box_scores["DD"] * 1.5
    + box_scores["TD"] * 3
)

# drop player column
box_scores = box_scores.drop(columns=["Player"])

# drop the position column
box_scores = box_scores.drop(columns=["Position"])

# group by team and calculate averages
team_averages = box_scores.groupby("Team").mean().round(2).reset_index()


# order the teams by fpts
team_averages = team_averages.sort_values(by="Fpts", ascending=False)

# output the team averages
team_averages.to_csv("team_averages.csv", index=False)
