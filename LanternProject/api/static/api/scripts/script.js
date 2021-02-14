const ChatboxApp = new Vue({

    // el: "#chatbox-app",
    el: "#app",

    data: {
        packages: [],
        api_key: '123456789',
        session_token: '',
        
        // Ready server
        ready: false,

        // State of App (Minimized | Maximized)
        expandHeader: false,
        showHeader: false,
        expandApp: false,
        active: false,

        // Visibility of the App
        showApp: true,

        // Theme
        theme: 'light',

        // Position
        position: 'right',        
    },

    methods: {

        sendMessage: function () {
            document.querySelector('#chat-message-submit').click()
        },
        toggleHeader: function() {
            this.expandHeader = !this.expandHeader

            var self = this
            if (this.expandHeader)
                setTimeout(function() { self.showHeader = true }, 350)
            else
                self.showHeader = false
        },
        toggleApp: function () {

            $("#toggler").attr({ "uk-icon": function (index, currentvalue) { return (currentvalue == "icon: chevron-down") ? "icon: chevron-up" : "icon: chevron-down" }, "title": function (index, currentvalue) { return (currentvalue == "minimize") ? "maximize" : "minimize" } })
            this.expandApp = !this.expandApp            

            if (!this.active) {
                this.startSession()
                this.active = !this.active
            }

            document.querySelector('#chat-message-input').focus()
        },
        closeApp: function () {
            this.showApp = false
        },
        changeTheme: function () {
            this.theme = (this.theme == 'light') ? 'dark' : 'light'
        },
        changePosition: function () {
            this.position = (this.position == 'left') ? 'right' : 'left'
        },
        startSession: function () {

            $("#chatbox-status").text('Starting Session...')

            $.ajax({
                url: 'http://127.0.0.1:8000/api/v1/services/sessions/start',
                type: 'GET',
                context: this,      // Essential for VueJS
                data: {
                    'key': this.api_key
                },
                error: function () {
                    console.log('There was a problem creating a session.');
                },
                success: function (data) {
                    this.ready = true
                    this.session_token = data       // Set session token
                    this.startSocket()              // Start socket
                    console.log('Session started successfully.');
                },
            });
        },
        startSocket: function () {

            const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/session/' + this.session_token + '/');

            chatSocket.onmessage = function (e) {
                const data = JSON.parse(e.data)

                var package = { id: data['id'], message: data['message'], datetime: data['datetime'], sender: 'agent' }

                // Push agent packages only
                if (!App.messageExists(package['id'])) App.packages.push(package)
            }

            document.querySelector('#chat-message-submit').onclick = function (e) {
                const messageInputDom = document.querySelector('#chat-message-input')
                const message = messageInputDom.value

                var package = { id: App.packages.length, message: message.replace(/\n/g, ''), datetime: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), sender: 'me' }

                chatSocket.send(JSON.stringify({
                    'id': package['id'],
                    'message': package['message'],
                    'datetime': package['datetime'],
                }));

                messageInputDom.value = ''
                App.packages.push(package)
            }

            chatSocket.onclose = function (e) { console.error('Server unexpectedly closed the connection.') }
        },
        messageExists: function (id) {
            for (var i = 0; i < this.packages.length; i++) if (this.packages[i]['id'] == id) return true
            return false
        },
    },

    mounted: function () {
        $('#app-content').css({ 'max-height': $(document).height() * 0.5 })
    },

    components: {
        'Package': {
            props: ['message', '_sender', 'datetime', '_id'],

            template: `
                <div id="this.id" class="uk-grid-small uk-flex-bottom uk-flex-right uk-text-left uk-flex" v-bind:class="[(this.sender != 'me') ? 'me' : 'agent']" uk-grid>
                    <div class="uk-width-auto uk-flex-1" v-if="this.sender != 'me'"><div class="uk-card uk-card-body uk-card-small uk-border-rounded-me" v-bind:class="[(this.sender != 'me') ? ['uk-card-primary', 'uk-float-right'] : ['uk-card-default', 'uk-float-left']]"><p class="uk-margin-remove">{{ message }}</p><p class="uk-margin-remove uk-time-p">{{ datetime }}</p></div></div>
                    <div class="uk-width-auto" v-if="this.sender != 'me'"><img class="uk-border-circle" width="32" height="32" src="../../../static/api/images/avatar.jpg" /></div>
                    <div class="uk-width-auto" v-if="this.sender == 'me'"><img class="uk-border-circle" width="32" height="32" src="../../../static/api/images/avatar.jpg" /></div>
                    <div class="uk-width-auto uk-flex-1" v-if="this.sender == 'me'"><div class="uk-card uk-card-body uk-card-small uk-border-rounded-agent" v-bind:class="[(this.sender != 'me') ? ['uk-card-primary', 'uk-float-right'] : ['uk-card-default', 'uk-float-left']]"><p class="uk-margin-remove">{{ message }}</p><p class="uk-margin-remove uk-time-p">{{ datetime }}</p></div></div>
                </div>`,

            data: function () {
                return {
                    sender: this._sender,
                    id: this._id,
                }
            }
        }
    }
})