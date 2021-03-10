window.onbeforeunload = function () {
    window.scrollTo(0, 0);
}

// Profile Section
const Profile = new Vue({

    el: "#profile",

    data: {
        username: 'keivanipchi'
    },

    mounted: function () {
        self = this
        $('form#profile_form').submit(function (e) {
            $.ajax({
                url: 'http://127.0.0.1:8000/dashboard/v1/user/' + self.username + '/profile/update',
                type: $(this).attr('method'),
                data: $(this).serialize(),
                error: function () {
                    $("#submit_btn").prop('disabled', true)
                    $("#error_model_body").text('We couldn\'t update your information at the moment. Please report the problem if persists.')
                    $('#error_model').modal('toggle');
                },
                success: function (response) {
                    $("#submit_btn").val(response).attr('class', (response == 'Updated, Reloading...' ? 'btn white m-b success' : 'btn white m-b warn'))
                    setTimeout(function () { location.reload() }, 500)
                },
            });
        })
    },
})

// Reserved Messages Section
const reservedMessages = new Vue({

    el: "#reservedmessages",

    data: {
        openedID: null,
        username: 'keivanipchi'
    },

    methods : {
        setActionId: function(id) {
            self = this            

            $("#controller_" + id).toggleClass('danger success')
            $("#controller_icon_" + id).toggleClass('fa-trash fa-check')

            if (!(self.openedID == null || self.openedID == id)) {
                $("#controller_" + self.openedID).toggleClass('danger success')
                $("#controller_icon_" + self.openedID).toggleClass('fa-trash fa-check')
            }

            self.openedID = (self.openedID == id) ? null : id
        },
        SendAction: function(id, action) {
            action = (action != null) ? action : (self.openedID == null || self.openedID != id) ? 'DELETE' : 'UPDATE'
            identifier = (action == 'INSERT') ? 'new' : id
            
            $.ajax({
                url: 'http://127.0.0.1:8000/dashboard/v1/user/' + self.username + '/reversedmessages/messages/modify',
                type: 'POST',
                data: {
                    id: identifier,
                    action: action,
                    title: $('#rm_Title_' + identifier).val(),
                    tag: $('#rm_Tag_' + identifier).val(),
                    color: $('#rm_Color_' + identifier).val(),
                    starred: $('#rm_Starred_' + identifier).is(":checked"),
                    content: $('#rm_Content_' + identifier).val(),
                    form: $("rm_form_" + id).serialize(),
                    csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
                },
                error: function(xhr, status, error) {
                    $("#error_model_body").text('We couldn\'t update your information at the moment. Please report the problem if persists.')
                    $('#error_model').modal('toggle');
                },
                success: function (response) {
                    if (response == '')
                        setTimeout(function () { location.reload() }, 500)
                    else {
                        $("#error_model_body").text('We couldn\'t process your action at the moment. Please report the problem if persists.')
                        $('#error_model').modal('toggle');
                    }                        
                },
            });
        }        
    },
})


// Chatroom Section
const Chatroom = new Vue({

    el: "#chatroom",

    data: {
        messages: [],
        rooms: [],
        message: '',
        username: 'keivanipchi',
    },

    methods: {
        copyToMessage: function(reservedMessageId) {
            self.message = $("#" + reservedMessageId).text()
        },
        sendMessage: function () {
            document.querySelector('#chat-message-submit').click()
        },
        assignRoom: function () {
            var self = this
            
            $.ajax({
                url: 'http://127.0.0.1:8000/dashboard/v1/user/' + self.username + '/chatroom/assign_room',
                type: 'GET',
                context: this,      // Essential for VueJS
                data: {
                },
                error: function () {
                    $("#error_model_body").text('We couldn\'t assign you a room at the moment. Please report the problem if persists.')
                    $('#error_model').modal('toggle');
                },
                success: function (data) {

                    const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/rooms/' + data.room_key + '/');
                    self = this

                    chatSocket.onmessage = function (e) {
                        const data = JSON.parse(e.data)

                        var room = { id: data['id'], message: data['message'], datetime: data['datetime'], sender: 'client' }

                        // Push agent messages only
                        if (!self.messageExists(room['id'])) self.messages.push(room)
                    }

                    document.querySelector('#chat-message-submit').onclick = function (e) {
                        const message = self.message

                        var room = { id: self.messages.length, message: message.replace(/\n/g, ''), datetime: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), sender: 'agent' }

                        chatSocket.send(JSON.stringify({
                            'id': room['id'],
                            'message': room['message'],
                            'datetime': room['datetime'],
                            'room_key': data.room_key,
                            'sender': room['sender'],
                        }));

                        self.message = ''
                        self.messages.push(room)
                    }

                    chatSocket.onclose = function (e) { console.error('RoomSocket closed the connection.') }

                    // Initialize chat
                    var i = 0                    
                    self.messages = []
                    for (i; i < data.messages.length; i++) {
                        var entry = JSON.parse(data.messages[i].replace(/'/g, '"'))
                        self.messages.push({ id: entry['id'], message: entry['content'], datetime: entry['datetime'], sender: entry['sender'] })
                    }
                },
            });
        },

        messageExists: function (id) {
            for (var i = 0; i < this.messages.length; i++) if (this.messages[i]['id'] == id) return true
            return false
        },

        closeRoom: function(room_key) {
            // Close the room, delete the chats and remove the room from dashboard
            $.ajax({
                url: 'http://127.0.0.1:8000/dashboard/v1/user/' + self.username + '/chatroom/close_room',
                type: 'GET',
                data: { 'room_key': room_key, 'username': this.username },
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
    },

    mounted: function () {
        self = this
        hall_key = $("#hall_key").val()
    },

    components: {
        'Message': {
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