
\copy genres(name) from 'project/data/data - genres.csv' (format csv, header, delimiter ',');
\copy organizations(org_name, country, year, CEO) from 'project/data/data - organizations.csv' (format csv, header, delimiter ',');
\copy games(name, release_date, is_esports) from 'project/data/data - games.csv' (format csv, header, delimiter ',');
\copy games_genres(game_name, genre_name) from 'project/data/data - games_genres.csv' (format csv, header, delimiter ',');
\copy teams(name, org_name) from 'project/data/data - teams.csv' (format csv, header, delimiter ',');
\copy teams_games(team_name, game_name, region) from 'project/data/data - teams_games.csv' (format csv, header, delimiter ',');
\copy streamers(ign, platform, language, average_viewers, channel_link, game_name, team_name) from 'project/data/data - streamers.csv' (format csv, header, delimiter ',');
\copy professional_gamers(player_name, player_id, earnings, team_name, game_name, country, region) from 'project/data/data - professional_gamers.csv' (format csv, header, delimiter ',');
\copy competitions(comp_name, start_date, end_date, prize_pool, winning_team, game_name) from 'project/data/data - competitions.csv' (format csv, header, delimiter ',');
\copy game_developers(dev_name, type, country, year_founded, game_name) from 'project/data/data - game_developers.csv' (format csv, header, delimiter ',');
