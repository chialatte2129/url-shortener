DROP TABLE IF EXISTS urls;
DROP TABLE IF EXISTS url_visits;

CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    original_url TEXT NOT NULL
);

CREATE Table url_visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url_id INT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address TEXT NOT NULL,
    user_agent TEXT NOT NULL,
    FOREIGN KEY (url_id) REFERENCES urls(id)
);

-- Sample data for the 'urls' table
INSERT INTO urls (original_url) VALUES
    ('http://example.com/page1');

-- Sample data for the 'url_visits' table
INSERT INTO url_visits (url_id, ip_address, created, user_agent) VALUES
    (1, '192.168.1.1', '2024-1-23 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-23 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-23 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-22 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-21 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-21 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-20 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-20 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-20 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-20 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-19 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-18 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-18 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-18 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-18 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-17 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-17 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-17 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-17 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-17 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-16 00:00:00', ""),
    (1, '192.168.1.1', '2024-1-16 00:00:00', "");


CREATE INDEX url_index ON urls (id);