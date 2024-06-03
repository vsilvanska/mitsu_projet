CREATE TABLE roles
(
    roles_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name_roles VARCHAR
);

CREATE TABLE users
(
    users_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name_users VARCHAR,
    password_users VARCHAR,
    email_users VARCHAR,
    roles_id INT,
    FOREIGN KEY (roles_id) REFERENCES roles(roles_id)
);

CREATE TABLE events
(
    events_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    title_e VARCHAR,
    date_e DATETIME,
    desc_e VARCHAR
);

CREATE TABLE link_users_events
(
    link_users_events_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    type_link_users_events VARCHAR,
    users_id INT,
    events_id INT,
    FOREIGN KEY (users_id) REFERENCES users(users_id),
    FOREIGN KEY (events_id) REFERENCES events(events_id)
);