insert into people values
('123456789','Tony Kar',183.2,64.6,'Blue','Blonde',
'14309 82 Ave NW Edmonton AB T1G 4E3','m',TO_DATE('1983-03-05','YYYY-MM-DD'));

insert into people values
('245136189','Amanda Kar',173.2,52.3,'Green','Blonde',
'14309 82 Ave NW Edmonton AB T1G 4E3','f',TO_DATE('1985-11-13','YYYY-MM-DD'));

insert into people values
('123321123','Sheena Alridge',161.1,50.3,'Brown','Black',
'8397 116 ST NW Edmonton AB T5E 1J2','f',TO_DATE('1992-01-03','YYYY-MM-DD'));

insert into people values
('909186324','Narayana Gopal',172.5,58.4,'Black','Black',
'12997 46 AVE NW Edmonton AB T3F 2A1','m',TO_DATE('1972-09-02','YYYY-MM-DD'));

insert into people values
('422831212','Kah Cheong Meng',168.3,55.6,'Brown','Brown',
'8397 29 ST NW Calgary AB F1J 4K4','m',TO_DATE('1960-02-29','YYYY-MM-DD'));

insert into people values
('268132514','Winston Brown',179.0,60.8,'Brown','Red',
'12 Ramrock Drive, Edmonton AB T1A 56J','m',TO_DATE('1968-03-31','YYYY-MM-DD'));

insert into people values
('888888888','Were Wolf',193.0,65.2,'Amber','Black',
'42 Universe End, Saskatoon','m',TO_DATE('1942-04-01','YYYY-MM-DD'));

insert into people values
('999999999','Generic Vendor',170.0,65.0,'Black','Black',
'Industrial District Edmonton','m',TO_DATE('1902-02-01','YYYY-MM-DD'));

insert into driving_condition values
(1, 'Must have corrective lenses');

insert into driving_condition values
(2, 'Only under supervision');

insert into drive_licence values
('304213298', '268132514', '3', null,
TO_DATE('2006-04-20', 'YY-MM-DD'),TO_DATE('2016-06-20', 'YY-MM-DD'));

insert into drive_licence values
('192341938', '123456789', '3', null, 
TO_DATE('2008-06-20', 'YY-MM-DD'),TO_DATE('2016-06-20', 'YY-MM-DD'));

insert into drive_licence values
('150753714', '123321123', '3', null, 
TO_DATE('2008-04-01', 'YY-MM-DD'),TO_DATE('2016-04-01', 'YY-MM-DD'));

insert into drive_licence values
('216843321', '422831212', 'nondriving', null, 
TO_DATE('2000-01-01', 'YY-MM-DD'),TO_DATE('2016-01-01', 'YY-MM-DD'));

insert into drive_licence values
('208312234', '245136189', 'nondriving', null, 
TO_DATE('2000-09-03', 'YY-MM-DD'),TO_DATE('2014-09-03', 'YY-MM-DD'));

insert into drive_licence values
('109231638', '909186324', '3', null, 
TO_DATE('1999-04-01', 'YY-MM-DD'),TO_DATE('2015-04-01', 'YY-MM-DD'));

insert into restriction values
('150735714', 1);

insert into vehicle_type values
(1, 'SUV');

insert into vehicle_type values
(2, 'Truck');

insert into vehicle_type values
(3, 'Car');

insert into vehicle_type values
(4, 'Motorcycle');

insert into vehicle values
('362154236', 'Honda', 'Yolo', 2013, 'Red', 3);

insert into vehicle values
('425132839', 'Audi', 'Rich', 2009, 'Black', 1);

insert into vehicle values
('192341231', 'Nissan', 'Big', 2011, 'Red', 1);

insert into vehicle values
('532373452', 'Chrysler', 'Ego', 1982, 'Silver', 3);

insert into vehicle values
('823122311', 'Chrysler', 'Ego', 2012, 'Black', 3);

insert into vehicle values
('156213241', 'Honda', 'Yolo', 2011, 'Black', 3);

insert into vehicle values
('712342131', 'Honda', 'Yolo', 2014, 'Blue', 3);

insert into vehicle values
('121561231', 'Dodge', 'Clunker', 2014, 'Black', 1);

insert into vehicle values
('612341345', 'Harley', 'Whywhy', 2014, 'White', 1);


insert into owner values
('268132514', '156213241', 'y');

insert into owner values
('123456789','192341231','y');

insert into owner values
('245136189','192341231','n');

insert into owner values
('245136189', '532373452', 'y');

insert into owner values
('123321123', '425132839', 'y');

insert into owner values
('909186324', '362154236', 'y');

insert into owner values
('888888888', '823122311', 'y');

insert into owner values
('909186324', '712342131', 'y');

insert into owner values
('123321123', '121561231', 'y');

insert into owner values
('123321123', '612341345', 'y');

insert into auto_sale values
(1, '999999999', '888888888', '532373452',
TO_DATE('1982-01-01', 'YY-MM-DD'), 5000);

insert into auto_sale values
(2, '999999999', '123321123', '425132839',
TO_DATE('2009-01-01', 'YY-MM-DD'), 7000);

insert into auto_sale values
(3, '999999999', '268132514', '156213241',
TO_DATE('2011-01-01', 'YY-MM-DD'), 9000);

insert into auto_sale values
(4, '999999999', '888888888', '192341231',
TO_DATE('2011-02-01', 'YY-MM-DD'), 15000);

insert into auto_sale values
(5, '888888888', '245136189', '192341231',
TO_DATE('2011-05-01', 'YY-MM-DD'), 3333);

insert into auto_sale values
(6, '888888888', '245136189', '532373452',
TO_DATE('2012-05-06', 'YY-MM-DD'), 4444);

insert into auto_sale values
(7, '999999999', '888888888', '823122311',
TO_DATE('2012-01-01', 'YY-MM-DD'), 8000);

insert into auto_sale values
(8, '999999999', '268132514', '362154236',
TO_DATE('2013-01-01', 'YY-MM-DD'), 6000);

insert into auto_sale values
(9, '245136189', '123321123', '192341231',
TO_DATE('2013-02-03', 'YY-MM-DD'), 3000);

insert into auto_sale values
(10, '999999999', '909186324', '712342131',
TO_DATE('2014-02-01', 'YY-MM-DD'), 5000);

insert into auto_sale values
(11, '268132514', '123456789', '362154236',
TO_DATE('2014-07-01', 'YY-MM-DD'), 5000);

insert into auto_sale values
(12, '999999999', '123321123', '121561231',
TO_DATE('2014-08-01', 'YY-MM-DD'), 15000);

insert into auto_sale values
(13, '999999999', '123321123', '612341345',
TO_DATE('2014-09-01', 'YY-MM-DD'), 12000);

insert into ticket_type values
('drinkdrive', 999);

insert into ticket_type values
('parking', 200);

insert into ticket_type values
('speeding', 300);

insert into ticket_type values
('runlight', 500);

insert into ticket values 
(1, '268132514', '362154236', '888888888', 'parking',
TO_DATE('2013-09-01', 'YY-MM-DD'), 'Strathcona', 'Parked across road');

insert into ticket values
(2, '123321123', '121561231', '888888888', 'speeding',
TO_DATE('2014-08-15', 'YY-MM-DD'), 'Strathcona', 'Over 50 in construction');

insert into ticket values
(3, '123321123', '121561231', '888888888', 'runlight',
TO_DATE('2014-08-15', 'YY-MM-DD'), 'Strathcona', 'No casualties');

insert into ticket values
(4, '123321123', '612341345', '888888888', 'speeding',
TO_DATE('2014-09-02', 'YY-MM-DD'), 'Strathcona', 'Over 50 in construction');