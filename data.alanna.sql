INSERT INTO people VALUES (
'100000001','alanna', NULL, NULL, NULL, NULL,'5509 - 111 Ave Edmonton AB Canada', 'f', NULL);

INSERT INTO people VALUES (
'100000002', 'timothy', NULL, NULL, NULL, NULL,'5509 - 111 Ave Edmonton AB Canada', 'm', NULL);

INSERT INTO people VALUES (
'100000003', 'mr lahey', NULL, NULL, NULL, NULL, 'Sunnydale Trailer Park', 'm', NULL);

INSERT INTO people VALUES (
'100000004', 'bubbles', NULL, NULL, NULL, NULL, 'Sunnysale Trailer Park', 'm', NULL);

INSERT INTO drive_licence VALUES (
'100001', '100000001', 'class 5', NULL, NULL, NULL);

INSERT INTO drive_licence VALUES (
'100002', '100000002', 'nondriving', NULL, NULL, NULL);

INSERT INTO drive_licence VALUES (
'100003', '100000003', 'class 5', NULL, NULL, NULL);

INSERT INTO drive_licence VALUES (
'100004', '100000004', 'nondriving', NULL, NULL, NULL);

INSERT INTO drive_condition (
1, 'zero alcohol');

INSERT INTO restriction (
'100001', 1);

INSERT INTO vehicle_type VALUES (
1, 'SUV');

INSERT INTO vehicle_type VALUES (
2, 'truck');

INSERT INTO vehicle_type VALUES (
3, 'car');

INSERT INTO vehicle_type VALUES (
4, 'cop car');

INSERT INTO vehicle VALUES (
'10001','buick','celebrity', NULL, 'egg shell', 3);

INSERT INTO vehicle VALUES (
'10002', 'gm', 'jeep', NULL, 'red', 1);

INSERT INTO vehicle VALUES (
'10022', 'dodge', 'minivan', NULL, 'pink', 1);

INSERT INTO vehicle VALUES (
'10222', 'ford', 'minivan', NULL, 'green', 1);

INSERT INTO vehicle VALUES (
'10003', 'gm', 'sedan', NULL, 'white', 4);

INSERT INTO vehicle VALUES (
'10004', 'buick', 'celebrity', NULL, 'black', 3); 

INSERT INTO vehicle VALUES (
'10044', 'buick', 'century', NULL, 'red', 3);

INSERT INTO vehicle VALUES (
'10444', 'gm', 'cadillac', NULL, 'blue', 3);

INSERT INTO owner VALUES (
'100000001', '10001', 'y');

INSERT INTO owner VALUES (
'100000002', '10002', 'y');

INSERT INTO owner VALUES (
'100000002', '10022', 'y');

INSERT INTO owner VALUES (
'100000002', '10222', 'y');

INSERT INTO owner VALUES (
'100000003', '10003', 'y');

INSERT INTO owner VALUES (
'100000004', '10004', 'y');

INSERT INTO owner VALUES (
'100000004', '10044', 'y');

INSERT INTO owner VALUES (
'100000004', '10444', 'y');

INSERT INTO auto_sale VALUES (
101, '100000002', '100000001', '10001', '31-MAR-2000', 500.00);

INSERT INTO auto_sale VALUES (
211, '100000001', '100000003', '10002', '07-MAR-2011', 500.00); 

INSERT INTO auto_sale VALUES (
102, '100000003', '100000002', '10002', '08-MAR-2011', 1000.00);

INSERT INTO auto_sale VALUES (
122, '100000003', '100000002', '10022', '08-MAR-2011', 50.00);

INSERT INTO auto_sale VALUES (
121, '100000003', '100000002', '10222', '08-MAR-2012', 5000.00);

INSERT INTO auto_sale VALUES (
103, '100000001', '100000003', '10003', '20-APR-2013', 10000.00);

INSERT INTO auto_sale VALUES (
104, '100000001', '100000004', '10004', '20-APR-2000', 100.00);

INSERT INTO auto_sale VALUES (
144, '100000001', '100000004', '10044', '1-APR-2000', 1500.00);

INSERT INTO auto_sale VALUES (
141, '100000002', '100000004', '10444', '31-MAR-2000', 100.00);

INSERT INTO ticket_type VALUES (
'parking', 50);

INSERT INTO ticket_type VALUES (
'speeding', 80);

INSERT INTO ticket_type VALUES (
'drinking', 160);

INSERT into ticket VALUES (
1001, '100000001', '10001', '100000003', 'parking', '01-JAN-2015', NULL, NULL);

INSERT into ticket VALUES (
1011, '100000001', '10001', '100000003', 'speeding', '31-MAR-2014', NULL, NULL);

INSERT into ticket VALUES (
1111, '100000001', '10001', '100000003', 'speeding', '03-JAN-2015', NULL, NULL);

INSERT into ticket VALUES (
1101, '100000001', '10001', '100000003', 'drinking', '04-JAN-2015', NULL, NULL);

INSERT into ticket VALUES (
1002, '100000002', '10002', '100000003', 'parking', '01-JAN-2000', NULL, NULL);

INSERT into ticket VALUES (
1003, '100000003', '10003', '100000003', 'drinking','01-JAN 2010', NULL, NULL);
