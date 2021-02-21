# Lantern Project
Lightweight web-based platform designed provide synchronous chat capability &amp; AI-driven conversation with customers. The goal is to provide a system that can connect clients to agents for support by various means of communications like: live chat, AI chat, Email, ...

**NOTE: SOME FILES HAVE BEEN REMOVED DUE TO COPY RIGHT, THE PROJECT WILL NOT RUN WITHOUT THESE FILES & CONFIGURATIONS.**

## Demo
![gif](https://github.com/keivanipchihagh/Lantern-Project/blob/main/README%20files/gif-1.gif)

## RoadMap
- [x] API Front-End design (Vue.js, UIkit)
	- [x] Basic Template
	- [ ] Responsive Frame	
- [x] API WebSocket (Django, channels)
	- [x] Single-layer costumer
	- [ ] Multi-layer costumers
	- [x] Security (Handshake, Session token)
- [x] Database (MySql)
	- [x] Core Message
	- [x] Core User
	- [x] Core Site
	- [ ] Core Log
- [ ] Dashboard Front-End desgin (Vue.js, FlatFull)
	- [ ] Layout
	- [x] Profile Section (Admin | Agent | Staff)
		- [x] Basic information update
		- [ ] Image upload
		- [ ] Password change - (Confirmation Email)
	- [x] Chatroom Section (Agent | Admin)
		- [x] Basics
		- [ ] WebSocket
	- [ ] Home Section (Admin | Agent | Staff)
	- [ ] Charts Section (Admin | Staff)
	- [ ] Newsletter (Admin | Staff)
	- [ ] Security (Handshake, Session token)


## Installation
1. download & install *docker* ([get-docker](https://docs.docker.com/get-docker/))
2. Install python packages
	- Django +3 (```$ pip install django```)
	- channels (```$ pip install channels```)
 	- redis-server (```$ pip install redis```)
 	- channels_redis (```$ pip install channels_redis```)
3. Run *docker* services (```docker run -p 6379:6379 -d redis:5```)
4. Run ```$ py manage.py runserver ```

## Used Technologies / Languages
- [VueJS](www.vuejs.org) v2.0
- [jQuery](www.jquery.com) v3.5.1
- [UIkit](www.getuikit.com) v3.6.14
- [Django](www.djangoproject.com) v3.1.0

## Credits
- **Admin dashboard template** from [FlatFull](https://flatfull.com)
 
