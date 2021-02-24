INSERT INTO core_site (name, url, private_key, public_key, date_joined, date_expires, service)
	VALUES ("localhost", "127.0.0.1:8000", "123456789", "123456789", NOW(), NOW(), 1);

INSERT INTO core_user (firstname, lastname, email, username, password, phonenumber, role, country, city, bio, rating, user_key, image, site_id)
	VALUES ("Keivan", "Ipchi Hagh", "keivanipchihagh@gmail.com", "keivanipchi", "25251380", "09197270223", "Staff", "Iran", "Tehran", "Die with memories, not dreams", 10.0, "123456789", null, 1);
    
INSERT INTO core_user (firstname, lastname, email, username, password, phonenumber, role, country, city, bio, rating, user_key, image, site_id)
	VALUES ("Kiana", "Ipchi Hagh", "kianaipchihagh@gmail.com", "kianaipchi", "13881388", "09197270223", "Admin", "Iran", "Tehran", "Hello dear!", 10.0, "987654321", null, 1);
    
INSERT INTO core_log (title, datetime, site_id, user_id)
	VALUES ("Sign In", NOW(), 1, 1);
    
INSERT INTO core_log (title, datetime, site_id, user_id)
	VALUES ("Sign In", NOW(), 1, 2);
    
INSERT INTO dashboard_menu (name, icon, label, category)
	VALUES ("home", "fa fa-tachometer", null, "Shared");

INSERT INTO dashboard_menu (name, icon, label, category)
	VALUES ("chatroom", "fa fa-child", null, "Shared");

INSERT INTO dashboard_menu (name, icon, label, category)
	VALUES ("newsletter", "fa fa-newspaper-o", null, "Shared");
    
INSERT INTO dashboard_menu (name, icon, label, category)
	VALUES ("profile", "fa fa-user-o", null, "Shared");
    
INSERT INTO dashboard_menu (name, icon, label, category)
	VALUES ("settings", "fa fa-cogs", null, "Shared");
    
INSERT INTO dashboard_newsletter (title, type, date_published, content, tags, user_id)
	VALUES ('Welcome to Lantern-Project', 'Announcement', NOW(), 'Bonjour! Ciao! Willkommen! Hello!<br/>We are so thrilled you decided to join our community! Hats off on making this excellent desicion! You are now officially in the loop to hear all about our awesome features, new released and many many more.', 'Staff Accouncement', 1);