CREATE TABLE statuses (
  id serial not null primary key,
  name varchar
);

CREATE TABLE users (
  id serial not null primary key,
  username varchar unique,
  password varchar
);

CREATE TABLE boards (
  id serial not null primary key,
  title varchar,
  is_active boolean,
  user_id integer references users(id),
  status_ids integer[]
);

CREATE TABLE cards (
  id serial not null primary key,
  title varchar,
  board_id integer references boards(id),
  status_id integer references statuses(id),
  order_num integer
)