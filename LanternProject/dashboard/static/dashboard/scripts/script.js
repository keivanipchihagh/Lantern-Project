// Profile Section
const Profile = new Vue({

    el: "#profile",

    data: {
        user_key: '123456789'
    },

    mounted: function () {
        self = this
        $('form#form_pi').submit(function(e) {
            $.ajax({
                url: 'http://127.0.0.1:8000/dashboard/v1/user/' + self.user_key + '/profile/pi',
                type: $(this).attr('method'),
                data: $(this).serialize(),
                error: function(){$("#submit_btn").val('Oops! Somthing went wrong').attr('class', 'btn white m-b danger').prop('disabled', true) },
                success: function (response) {
                    $("#submit_btn").val(response).attr('class', (response == 'Updated, Reloading...' ? 'btn white m-b success' : 'btn white m-b warn'))
                    setTimeout(function() { location.reload() }, 500)
                },
            });
        })
    },
})

// Chatroom Section
const Chatroom = new Vue({

    el: "#chatroom",

    data: {
        packages: [],
        message: '',
        user_key: '123456789',
    },

    methods: {

        sendMessage: function () {            
            document.querySelector('#chat-message-submit').click()
        },        
        openChat: function (room_key) {
            self = this
            document.querySelector('#chatTitle').innerText = 'Chat - ' + room_key
            const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/rooms/' + room_key + '/');
            self = this
            
            chatSocket.onmessage = function (e) {
                const data = JSON.parse(e.data)

                var package = { id: data['id'], message: data['message'], datetime: data['datetime'], sender: 'client' }

                // Push agent packages only
                if (!self.messageExists(package['id'])) self.packages.push(package)
            }
            
            document.querySelector('#chat-message-submit').onclick = function (e) {
                const message = self.message                

                var package = { id: self.packages.length, message: message.replace(/\n/g, ''), datetime: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), sender: 'agent' }
                
                chatSocket.send(JSON.stringify({
                    'id': package['id'],
                    'message': package['message'],
                    'datetime': package['datetime'],
                    'room_key': room_key,
                    'sender': package['sender'],
                }));

                self.message = ''
                self.packages.push(package)
            }

            chatSocket.onclose = function (e) { console.error('Server connection was terminated.') }

            this.getChat(room_key, this.user_key)
        },

        getChat: function(room_key, user_key) {
            var self = this            

            $.ajax({
                url: 'http://127.0.0.1:8000/dashboard/v1/fetch/room',
                type: 'GET',
                context: this,      // Essential for VueJS
                data: {
                    'room_key': room_key,
                    'user_key': user_key
                },
                error: function () {
                    console.log('There was a problem fetching messages from server.');
                },
                success: function (data) {
                    var i = 0
                    self.packages = []
                    for (i; i < data.length; i++) {
                        var entry = JSON.parse(data[i].replace(/'/g, '"'))
                        self.packages.push({id: entry['id'], message: entry['content'], datetime: entry['datetime'], sender: entry['sender']})
                    }                    
                },
            });
        },

        closeChat: function(room_key) {
            // Close the room, delete the chats and remove the room from dashboard
            $.ajax({
                url: 'http://127.0.0.1:8000/dashboard/v1/close/room',
                type: 'GET',
                data: { 'room_key': room_key, 'user_key': this.user_key },
                error: function () { console.error('Session could not be closed') },
                success: function () {
                    console.log('Session Closed.')

                    $("#assigned_" + room_key).remove()
                    $("#open_" + room_key).remove()
                    $('#chatTitle').text('Chat')
                    $("#assigned_rooms_count").text(parseInt($("#assigned_rooms_count").text()) - 1)
                    $("#open_rooms_count").text(parseInt($("#open_rooms_count").text()) - 1)
                },
            });
        },

        messageExists: function (id) {
            for (var i = 0; i < this.packages.length; i++) if (this.packages[i]['id'] == id) return true
            return false
        },        
    },

    mounted: function () {

    },

    watch: {
        
    },

    components: {
        'Package': {
            props: ['message', '_sender', 'datetime', '_id'],

            template: `
                <!-- Agent - start -->
                <div class="m-b" v-if="this.sender != 'client'">
                    <a href="" class="pull-right w-40 m-l-sm"><img src="../../../static/dashboard/images/a3.jpg" class="w-full img-circle" alt="..."></a>
                    <div class="clear text-right">
                        <div class="p-a p-y-sm info inline text-left r">{{ message }}</div>
                        <div class="text-muted text-xs m-t-xs">{{ datetime }}</div>
                    </div>
                </div>
                <!-- Agent - end -->
                
                <!-- User - start -->
                <div class="m-b" v-else>
                <a href="" class="pull-left w-40 m-r-sm"><img src="../../../static/dashboard/images/a3.jpg" class="w-full img-circle" alt="..."></a>
                    <div class="clear">
                        <div><div class="p-a p-y-sm dark-white inline r">{{ message }}</div></div>
                        <div class="text-muted text-xs m-t-xs"><i class="fa fa-ok text-success"></i>{{ datetime }}</div>
                    </div>
                </div>
                <!-- User - end -->`,

            data: function () {
                return {
                    sender: this._sender,
                    id: this._id,
                }
            }
        }
    }
})