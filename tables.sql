CREATE TABLE customer_tbl (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    phone_number VARCHAR(13) NOT NULL,
    curp VARCHAR(18) NOT NULL UNIQUE,
    rfc VARCHAR(13) NOT NULL UNIQUE,
    address VARCHAR NOT NULL
    );

CREATE TABLE item_tbl (
    item_id SERIAL PRIMARY KEY,
    item_name VARCHAR(30) NOT NULL,
    item_price NUMERIC(7, 2) NOT NULL
    );

CREATE TABLE item_purchase_tbl (
    order_id SERIAL PRIMARY KEY,
    purchase_date DATE NOT NULL,
    purchase_price NUMERIC(7, 2) NOT NULL,
    comments VARCHAR,
    item_id INT NOT NULL REFERENCES item_tbl (item_id),
    customer_id INT NOT NULL REFERENCES customer_tbl (customer_id)
    );