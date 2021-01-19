drop table Game_Developers;
drop table Competitions;
drop table Professional_Gamers;
drop table Streamers;
drop table Teams_Games;
drop table Teams;
drop table Games_Genres;
drop table Games;
drop table Organizations;
drop table Genres;
drop type company_type;

CREATE TYPE company_type AS ENUM ('Independent', 'Company', 'Individual');

create table Genres (
    name varchar(128) primary key
);

create table Organizations (
    org_name varchar(128) primary key,
    country varchar(128),
    year integer,
    CEO varchar(128)
);

create table Games (
    name varchar(128) primary key,
    release_date date,
    is_esports boolean
);

create table Games_Genres( 
    game_name varchar(128),
    genre_name varchar(128),
    primary key (game_name, genre_name),
    foreign key (game_name) references Games(name),
    foreign key (genre_name) references Genres(name)
);

create table Teams (
    name varchar(128) primary key,
    org_name varchar(128),
    foreign key (org_name) references Organizations(org_name)
);

create table Teams_Games(
    team_name varchar(128),
    game_name varchar(128),
    region varchar(5),
    primary key (team_name, game_name),
    foreign key (team_name) references Teams(name),
    foreign key (game_name) references Games(name)
);

create table Streamers (
    ign varchar(128),
    platform varchar(128),
    language varchar(128),
    average_viewers integer,
    channel_link varchar(512),
    game_name varchar(128), 
    team_name varchar(128),
    primary key (ign, platform),
    foreign key (game_name) references Games(name),
    foreign key (team_name) references Teams(name)
);

create table Professional_Gamers (
    player_name varchar(128) primary key,
    player_id varchar(128),
    earnings money,
    country varchar(128),
    team_name varchar(128),
    game_name varchar(128),
    region varchar(5),
    foreign key (game_name) references Games(name),
    foreign key (team_name) references Teams(name)
);

create table Competitions (
    comp_name varchar(128) primary key,
    start_date date,
    end_date date,
    prize_pool money,
    winning_team varchar(128) not null,
    game_name varchar(128) not null,
    foreign key (game_name) references Games(name),
    foreign key (winning_team) references Teams(name)
);

create table Game_Developers (
    dev_name varchar(128),
    type company_type,
    country varchar(128),
    year_founded numeric not null,
    game_name varchar(128),
    primary key(dev_name, game_name),
    foreign key (game_name) references Games(name)
);
