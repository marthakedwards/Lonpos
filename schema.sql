drop table if exists coord;
create table coord (
  x tinyint unsigned not null,
  y tinyint unsigned not null,
  color text not null,
  board_id references board(id)
);