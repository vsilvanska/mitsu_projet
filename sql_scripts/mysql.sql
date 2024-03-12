-- Створення таблиці "Люди"
CREATE TABLE People (
    person_id INT PRIMARY KEY AUTO_INCREMENT,
    person_name VARCHAR(100) NOT NULL,
    table_id INT,
    FOREIGN KEY (table_id) REFERENCES Tables(table_id)
);

-- Створення таблиці "Сервер"
CREATE TABLE Servers (
    server_id INT PRIMARY KEY AUTO_INCREMENT,
    server_name VARCHAR(100) NOT NULL
);

-- Створення таблиці "Роль"
CREATE TABLE Roles (
    role_id INT PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(100) NOT NULL
);

-- Створення таблиці "Публікація"
CREATE TABLE Publications (
    publication_id INT PRIMARY KEY AUTO_INCREMENT,
    publication_name VARCHAR(255) NOT NULL,
    server_id INT,
    role_id INT,
    FOREIGN KEY (server_id) REFERENCES Servers(server_id),
    FOREIGN KEY (role_id) REFERENCES Roles(role_id)
);
