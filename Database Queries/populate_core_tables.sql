INSERT INTO core_site (url, private_key, public_key, date_joined, date_expires, service)
	VALUES ("127.0.0.1:8000", "123456789", "123456789", NOW(), NOW(), 1);

INSERT INTO core_user (firstname, lastname, email, username, password, role, status, user_key, last_online, date_joined, site_id)
	VALUES ("Keivan", "Ipchi Hagh", "keivanipchihagh@gmail.com", "keivanipchi", "25251380", "staff", "idle", "123456789", NOW(), NOW(), 1);
    
INSERT INTO core_user (firstname, lastname, email, username, password, role, status, user_key, last_online, date_joined, site_id)
	VALUES ("Kiana", "Ipchi Hagh", "kianaipchi@gmail.com", "kianaipchi", "13881388", "admin", "online", "987654321", NOW(), NOW(), 1);