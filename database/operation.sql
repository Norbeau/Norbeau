CREATE TABLE member_list (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(16) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    role ENUM('administrator', 'manager', 'user') NOT NULL
);
