-- INSERT INTO core_site (url, private_key, public_key, date_joined, date_expires, service)
-- 	VALUES ("127.0.0.1:8000", "123456789", "123456789", NOW(), NOW(), 1);

INSERT INTO core_user (firstname, lastname, email, username, password, phonenumber, role, country, city, bio, rating, user_key, image, site_id)
	VALUES ("Keivan", "Ipchi Hagh", "keivanipchihagh@gmail.com", "keivanipchi", "25251380", "09197270223", "staff", "Iran", "Tehran", "Die with memories, not dreams", 10.0, "123456789", null, 1);
    
INSERT INTO core_user (firstname, lastname, email, username, password, phonenumber, role, country, city, bio, rating, user_key, image, site_id)
	VALUES ("Kiana", "Ipchi Hagh", "kianaipchihagh@gmail.com", "kianaipchi", "13881388", "09197270223", "admin", "Iran", "Tehran", "Hello dear!", 10.0, "987654321", null, 1);
    
INSERT INTO core_log (title, datetime, user_id)
	VALUES ("Sign In", NOW(), 1);
    
INSERT INTO core_log (title, datetime, user_id)
	VALUES ("Sign In", NOW(), 2);