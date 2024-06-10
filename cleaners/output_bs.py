import csv
from mysql.connector import connect, Error
from datetime import date, time, datetime
import pandas as pd
from settings import DB_NAME, DB_HOST, DB_USER, DB_PASSWORD


def execute_query(query):
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows


def write_to_csv(rows, sum_or_individual, file_path):
    df = pd.DataFrame(rows)
    df.to_csv(file_path, index=False)
    with open("output.csv", "w", newline="") as file:
        writer = csv.writer(file)
        if sum_or_individual.lower() == "s":
            writer.writerow(
                [
                    "Player",
                    "Team",
                    "Min",
                    "Pts",
                    "Reb",
                    "Ast",
                    "Stl",
                    "Blk",
                    "Tov",
                ]
            )
        elif sum_or_individual.lower() == "i":
            writer.writerow(
                [
                    "Date",
                    "Player",
                    "Position",
                    "Team",
                    "Matchup",
                    "WL",
                    "Min",
                    "Pts",
                    "Reb",
                    "Ast",
                    "Stl",
                    "Blk",
                    "Tov",
                    "FGM",
                    "FGA",
                    "FG%",
                    "3PM",
                    "3PA",
                    "3P%",
                ]
            )
        for row in rows:
            if sum_or_individual.lower() == "s":
                writer.writerow(
                    [
                        row["player_name"],
                        row["team_abbreviation"],
                        row["min"],
                        row["pts"],
                        row["reb"],
                        row["ast"],
                        row["stl"],
                        row["blk"],
                        row["tov"],
                    ]
                )
            elif sum_or_individual.lower() == "i":
                writer.writerow(
                    [
                        row["game_date"],
                        row["player_name"],
                        row["position"],
                        row["team_abbreviation"],
                        row["matchup"],
                        row["wl"],
                        row["min"],
                        row["pts"],
                        row["reb"],
                        row["ast"],
                        row["stl"],
                        row["blk"],
                        row["tov"],
                        row["fg3m"],
                        row["fg3a"],
                        row["fg_pct"],
                        row["fg3m"],
                        row["fg3a"],
                        row["fg3_pct"],
                    ]
                )


try:
    with connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    ) as connection:
        print(f"Connection to DB successful {connection}")
        print("Dates must be in the format 'YYYY-MM-DD'")
        start_date = input("Enter start date: ")
        end_date = input("Enter end date: ")
        player_names = input("Enter player name(s) separated by commas: ").split(",")
        player_names = "' or player_name ='".join(player_names)
        player_names = f"{player_names}"
        sum_or_individual = input("Sum or individual? (s/i): ")

        if sum_or_individual.lower() == "s" and len(player_names) > 0:
            query = f"""
                SELECT player_name, team_abbreviation, sum(min) as min,
                    sum(pts) as pts, sum(reb) as reb, sum(ast) as ast,
                    sum(stl) as stl, sum(blk) as blk,
                    sum(tov) as tov
                FROM boxscores
                WHERE game_date >= '{start_date}' AND game_date <= '{end_date}'
                    AND (player_name = '{player_names}')
                GROUP BY player_name, team_abbreviation
                ORDER BY player_name
            """
        elif sum_or_individual.lower() == "i" and len(player_names) > 0:
            matchup = input("Enter a matchup or leave blank for all (i.e:CLE vs. ORL):")
            if matchup == "":
                query = f"""
                    SELECT game_date,player_name,team_abbreviation,matchup, 
                    wl, min, pts, reb, ast, stl, blk, tov, fgm, fga, fg_pct, fg3m, fg3a, fg3_pct
                    FROM boxscores
                    WHERE game_date >= '{start_date}' AND game_date <= '{end_date}'
                        AND (player_name = '{player_names}')
                    ORDER BY matchup desc
                """
            else:
                query = f"""
                    SELECT game_date, player_id, player_name, team_id, team_abbreviation, 
                    game_id, matchup, wl, min, pts, reb, ast, stl, blk, tov, fgm, fga, fg_pct, fg3m, fg3a, fg3_pct
                    FROM boxscores
                    WHERE game_date >= '{start_date}' AND game_date <= '{end_date}'
                    AND (player_name = '{player_names}' AND matchup = '{matchup}')
                    ORDER BY matchup desc
            """
        elif sum_or_individual.lower() == "s" and len(player_names) == 0:
            query = f"""
                SELECT player_name, team_abbreviation, sum(min) as min,
                    sum(pts) as pts, sum(reb) as reb, sum(ast) as ast,
                    sum(stl) as stl, sum(blk) as blk,
                    sum(tov) as tov
                FROM boxscores
                WHERE game_date >= '{start_date}' AND game_date <= '{end_date}'
                GROUP BY player_name, team_abbreviation
                ORDER BY player_name
                """
        elif sum_or_individual.lower() == "i" and len(player_names) == 0:
            matchup = input("Enter a matchup or leave blank for all (i.e:CLE vs. ORL):")

            if matchup == "":
                query = f"""
                    SELECT game_date, player_name, position, team_abbreviation,matchup, 
                        wl, min, pts, reb, ast, stl, blk, tov, fgm, fga, fg_pct, fg3m, fg3a, fg3_pct
                    FROM boxscores JOIN player_info ON boxscores.player_id = player_info.person_id
                    WHERE game_date >= '{start_date}' AND game_date <= '{end_date}'
                    ORDER BY game_date desc
                    """
            else:
                reverse_matchup = matchup.split(" vs. ")
                reverse_matchup = f"{reverse_matchup[1]} vs. {reverse_matchup[0]}"
                query = f"""
                    SELECT game_date, player_name,team_abbreviation,matchup, 
                        wl, min, pts, reb, ast, stl, blk, tov, fgm, fga, fg_pct, fg3m, fg3a, fg3_pct
                    FROM boxscores
                    WHERE (game_date >= '{start_date}' AND game_date <= '{end_date}' AND matchup = '{matchup}' 
                        OR matchup = '{reverse_matchup}')
                    ORDER BY game_date desc
                """

        print(query)
        print("Executing:")
        starttime = datetime.now()

        rows = execute_query(query)
        write_to_csv(rows, sum_or_individual, "../data/output.csv")


except Error as e:
    print("ERROR: " + str(e))
print(f"{len(rows)} rows in set")
endtime = datetime.now()
duration = endtime - starttime
total_seconds = duration.total_seconds()
milliseconds = total_seconds * 1000
print("Done")
print(f"Execution time: {milliseconds:.2f} ms")
