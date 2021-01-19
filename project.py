import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser
 
'# The E-sports Community'
 
@st.cache
def get_config(filename='project/code/database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}
 
 
@st.cache
def query_db(sql: str):
    # print(f'Running query_db(): {sql}')
 
    db_info = get_config()
 
    # Connect to an existing database
    conn = psycopg2.connect(**db_info)
 
    # Open a cursor to perform database operations
    cur = conn.cursor()
 
    # Execute a command: this creates a new table
    cur.execute(sql)
 
    # Obtain data
    data = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
 
    # Make the changes to the database persistent
    conn.commit()
 
    # Close communication with the database
    cur.close()
    conn.close()
 
    df = pd.DataFrame(data=data, columns=column_names)
 
    return df
 
'## List of Games by Genre'
sql_all_genres = "select name from genres order by name;"
all_genres = query_db(sql_all_genres)['name'].tolist()
genre_select = st.selectbox('Choose a Genre:', all_genres)
if genre_select:
    f'Show {genre_select} games:'
    sql_table = f"select game_name from games_genres where genre_name = '{genre_select}' order by game_name;"
    df = query_db(sql_table)
    st.dataframe(df)

'## Profession Players by Team'
sql_all_teams = "select distinct name from teams t, professional_gamers pg where t.name = pg.team_name order by name;"
all_teams = query_db(sql_all_teams)['name'].tolist()
team_select = st.selectbox('Choose a Team:', all_teams)
if team_select:
    f'Professional players on {team_select}:'
    sql_teams = f"""select distinct player_name, player_id, game_name
                from professional_gamers pg JOIN teams t 
                on pg.team_name = t.name
                where pg.team_name = '{team_select}'
                order by player_name;"""
    team_info = query_db(sql_teams)
    st.dataframe(team_info)

'## Professional Players by Game'
sql_all_games = "select name from games where is_esports order by name;"
all_games = query_db(sql_all_games)['name'].tolist()
game_select = st.selectbox('Choose a Game:', all_games)
if game_select:
    f'Professional players who play {game_select}:'
    sql_games = f"""select pg.player_name, pg.player_id, s.channel_link
                from professional_gamers pg left join streamers s on s.ign = pg.player_id
                where pg.game_name = '{game_select}'
                order by pg.player_name;"""
    game_info = query_db(sql_games)
    st.dataframe(game_info)

'## Professional Players who Play for a Foreign Team'
sql_region = 'select distinct tg.region from teams_games tg, professional_gamers pg where tg.region != pg.region and tg.team_name = pg.team_name and tg.game_name = pg.game_name;'
region = query_db(sql_region)['region'].tolist()
region_radio = st.radio('Choose a Team Region:', region)
if region_radio:
    sql_customers = f"""select pg.player_id, pg.country as nationality, tg.team_name, tg.region
    from professional_gamers pg JOIN teams_games tg
    on tg.team_name = pg.team_name
    and tg.game_name = pg.game_name
    where pg.region != '{region_radio}'
    and tg.region is not null
    and tg.region = '{region_radio}'
    order by tg.team_name,  pg.country;"""
    gamer_name = query_db(sql_customers)
    st.dataframe(gamer_name)

'## Winners of Competition in Prize Range'
sql_min_prize = 'select MIN(prize_pool) as min_prize from competitions;'
min_prize = query_db(sql_min_prize).loc[0]
min_prize = float(min_prize['min_prize'].replace('$', '').replace(',', ''))
sql_max_prize = 'select MAX(prize_pool) as max_prize from competitions;'
max_prize = query_db(sql_max_prize).loc[0]
max_prize = float(max_prize['max_prize'].replace('$', '').replace(',', ''))
range_select = st.slider('Select a Prize Range:', min_prize, max_prize, (min_prize, max_prize))
if range_select:
    sql_teams = f"""select winning_team, comp_name as competition, game_name, prize_pool
    from competitions
    where prize_pool >= cast({range_select[0]} as money)
    and prize_pool <= cast({range_select[1]} as money)
    order by prize_pool desc;
    """
    team_prizes = query_db(sql_teams)
    st.dataframe(team_prizes)

'## Tournament Earnings by Team'
sql_all_team_earn = 'select distinct winning_team from competitions order by winning_team;'
all_team_earn = query_db(sql_all_team_earn)['winning_team'].tolist()
team_earn_select = st.multiselect('Choose Team(s)', all_team_earn)
if team_earn_select:
    team_earn_list = ','.join(["'" + x + "'" for x in team_earn_select])
    sql_earnings = f"""select winning_team, game_name, COUNT(*) as num_winnings, SUM(prize_pool) as total_earnings
    from competitions
    where winning_team in ({team_earn_list})
    group by winning_team, game_name
    order by SUM(prize_pool) desc;
    """
    team_earnings = query_db(sql_earnings)
    st.dataframe(team_earnings)

'## Tournament Earnings by Country'
sql_country_earn = "select distinct country from organizations o, competitions c where c.winning_team = o.org_name order by country;"
tourney_countries = query_db(sql_country_earn)['country'].tolist()
con_tourney_select = st.multiselect('Choose Region(s)', tourney_countries)
if con_tourney_select:
    countries_selected = ','.join(["'" + elem + "'" for elem in con_tourney_select])
    sql_tourney = f"""select o.country, c.game_name, SUM(c.prize_pool) as total_earnings
                      from competitions c JOIN organizations o
                      on c.winning_team = o.org_name
                      where o.country in ({countries_selected})
                      group by o.country, c.game_name
                      order by SUM(c.prize_pool) desc;"""
    df_region_info = query_db(sql_tourney)
    st.dataframe(df_region_info) 
    

'## Average Stream Viewers by Game'
sql_viewer_games = "select distinct game_name from streamers order by game_name;"
viewer_games = query_db(sql_viewer_games)['game_name'].tolist()
viewer_games_select = st.multiselect('Choose Game(s)', viewer_games)
if viewer_games_select:
    games_select = ','.join("'" + game + "'" for game in viewer_games_select)
    sql_viewers = f"""select game_name, round(AVG(average_viewers), 2) as avg_viewers
    from streamers
    where game_name in ({games_select})
    group by game_name
    order by AVG(average_viewers) desc;
    """
    df_viewer_games = query_db(sql_viewers)
    st.dataframe(df_viewer_games)

'## Streamer by Game'
sql_streamer = "select distinct game_name from streamers order by game_name;"
streamer_games = query_db(sql_viewer_games)['game_name'].tolist()
streamer_games_select = st.selectbox('Choose Game(s)', viewer_games)
if streamer_games_select:
    sql_streamers = f"""select ign, language, channel_link
                        from streamers
                        where game_name = '{streamer_games_select}'
                        order by ign;"""
    df_streamer = query_db(sql_streamers)
    st.dataframe(df_streamer)
