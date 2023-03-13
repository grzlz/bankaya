INSERT INTO item_tbl (item_name, item_price)
VALUES 
    ('Monitor', 5000),
    ('Mouse', 200),
    ('Keyboard', 500),
    ('Chair', 3500),
    ('Headphones', 99.99);


INSERT INTO customer_tbl (first_name, last_name, phone_number, curp, rfc, address)
VALUES 
    ('Bruce', 'Wayne', '525555555555', 'RAGM860718HQRDPL46', 'RAMG860718AS8', 'Calle Azul numero 5'),
    ('Bruno', 'Mars', '535555555555', 'GAGM560718HQRDPL34', 'GAGM560718LO3', 'Calle Roja numero 6'),
    ('Mars', 'Volta', '525555555555', 'SOGA830528MQRDPL83', 'SOGA839528WT3', 'Calle Morada numero 8'),
    ('Nikola', 'Telsa', '525555555555', 'SOGA830528MQRDPL84', 'SOGA839528WT4', 'Calle Verde numero 3'),
    ('Thomas', 'Edison', '534444444444', 'SOGA830528MQRDPL85', 'SOGA839528WT5', 'Calle Amarilla numero 1'); 

INSERT INTO item_purchase_tbl (purchase_date, purchase_price, comments, item_id, customer_id)
VALUES 
    ('2023-03-08', 5000, 'Monitor grande', 1, 1),
    ('2023-03-07', 200, 'Entregaron a tiempo', 2, 2),
    ('2023-03-06', 500, 'Entregaron a tiempo', 3, 2),
    ('2023-03-05', 3500, 'La silla fue fácil de armar', 4, 5),
    ('2023-03-04', 99.99, '5 estrellas excelente servicio', 5, 4);
