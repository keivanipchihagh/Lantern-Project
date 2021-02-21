-- INSERT INTO core_site (url, name, private_key, public_key, date_joined, date_expires, service)
-- 	VALUES ("127.0.0.1:8000", "localhost", "123456789", "123456789", NOW(), NOW(), 1);

delete from core_user;

INSERT INTO core_user (firstname, lastname, email, username, password, phonenumber, role, country, city, bio, rating, user_key, site_id)
	VALUES ("Keivan", "Ipchi Hagh", "keivanipchihagh@gmail.com", "keivanipchi", "25251380", "09197270223", "Staff", "Iran", "Tehran", "Die with memories, not dreams", "10", "123456789", 1);
    