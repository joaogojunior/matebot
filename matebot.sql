create database matebot;
create user usuario_db@localhost identified by 'senha_db';
grant all privileges on matebot.* to usuario_db@localhost;
