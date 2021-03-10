/* Sites */
INSERT INTO dashboard_site (host, url, private_key, public_key, date_joined, date_expires, livechat_service, ticket_service, virtualagent_service)
	VALUES ("127.0.0.1", "127.0.0.1:8000", "123456789", "123456789", NOW(), NOW(), 1, 1, 0);
    
/* Users */
INSERT INTO dashboard_user (firstname, lastname, email, username, password, phonenumber, role, title, rating, user_key, site_id)
	VALUES ("Keivan", "Ipchi Hagh", "keivanipchihagh@gmail.com", "keivanipchi", "25251380", "09197270223", "staff", "staff", 10.0, "123456789", 1);

INSERT INTO dashboard_user (firstname, lastname, email, username, password, phonenumber, role, title, rating, user_key, site_id)
	VALUES ("Kiana", "Ipchi Hagh", "kianaipchihagh@gmail.com", "kianaipchi", "13881388", "09197270223", "admin", "admin", 10.0, "987654321", 1);

/* Logs */
INSERT INTO dashboard_log (title, datetime, site_id, user_id)
	VALUES ("Sign In", NOW(), 1, 1);
    
INSERT INTO dashboard_log (title, datetime, site_id, user_id)
	VALUES ("Sign In", NOW(), 1, 2);
    
/* Menus */
INSERT INTO dashboard_menu (name, icon, label, category)
	VALUES ("home", "fa fa-tachometer", null, "Shared");

INSERT INTO dashboard_menu (name, icon, label, category)
	VALUES ("chatroom", "fa fa-child", null, "Shared");

INSERT INTO dashboard_menu (name, icon, label, category)
	VALUES ("newsletter", "fa fa-newspaper-o", null, "Shared");
    
INSERT INTO dashboard_menu (name, icon, label, category)
	VALUES ("profile", "fa fa-user-o", null, "Shared");

INSERT INTO dashboard_menu (name, icon, label, category)
	VALUES ("reserved messages", "fa fa-quote-right", null, "Shared");

INSERT INTO dashboard_menu (name, icon, label, category)
	VALUES ("settings", "fa fa-cogs", null, "Shared");
    
/* News Letters */
INSERT INTO dashboard_newsletter (title, type, date_published, content, tags, user_id)
	VALUES ('Welcome to Lantern-Project', 'Announcement', NOW(), 'Bonjour! Ciao! Willkommen! Hello!<br/>We are so thrilled you decided to join our community! Hats off on making this excellent desicion! You are now officially in the loop to hear all about our awesome features, new released and many many more.', 'Staff Accouncement', 1);
    
INSERT INTO dashboard_newsletter (title, type, date_published, content, tags, user_id)
	VALUES ('Release - Update v1.0.0', 'update', NOW(), 'Initial Release is out! <br/>We are drilled to announce that <b>Version 1.0.0</b> is officially out! This is the first release of the project after months of work. We have put our best effort to design, build and test every single component; however, as we are constantly developing the platform you might face some malfunctions here and there, so be patient and please notify the <b>Staff</b> if any problem persists.', 'staff,update,maintenance', 1);

/* Reserved Messages */    
INSERT INTO dashboard_reservedmessages (title, tag, content, starred, date_modified, user_id, color)
	VALUES ('starting the conversation', 'greeting', 'Greetings! How can I be of service?', 1, NOW(), 1, 'purple');
    
INSERT INTO dashboard_reservedmessages (title, tag, content, starred, date_modified, user_id, color)
	VALUES ('ending the conversation', 'ending', 'Glad I could help, Wish you a good day!', 0, NOW(), 1, 'teal');
    
INSERT INTO dashboard_reservedmessages (title, tag, content, starred, date_modified, user_id, color)
	VALUES ('Asking for details', 'clarification', 'I can certainly help you with that, but I will more details regarding your request.', 0, NOW(), 1, 'lime');