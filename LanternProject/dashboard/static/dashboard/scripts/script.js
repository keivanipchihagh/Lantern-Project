const ChatApp = new Vue({

    // el: "#chatbox-app",
    el: "#chat-app",

    data: {
        packages: [],
        message: '',
        session_token: '589c12f50202230bf06cd6c3cdf53afc',
    },

    methods: {

        sendMessage: function () {
            document.querySelector('#chat-message-submit').click()
        },                
        startSocket: function () {

            const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/session/' + this.session_token + '/');
            self = this
            
            chatSocket.onmessage = function (e) {
                const data = JSON.parse(e.data)

                var package = { id: data['id'], message: data['message'], datetime: data['datetime'], sender: 'me' }

                // Push agent packages only
                if (!ChatApp.messageExists(package['id'])) ChatApp.packages.push(package)
            }
            
            document.querySelector('#chat-message-submit').onclick = function (e) {
                const message = self.message                

                var package = { id: ChatApp.packages.length, message: message.replace(/\n/g, ''), datetime: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), sender: 'agent' }

                chatSocket.send(JSON.stringify({
                    'id': package['id'],
                    'message': package['message'],
                    'datetime': package['datetime'],
                }));

                self.message = ''
                ChatApp.packages.push(package)
            }

            chatSocket.onclose = function (e) { console.error('Server connection was terminated.') }
        },
        messageExists: function (id) {
            for (var i = 0; i < this.packages.length; i++) if (this.packages[i]['id'] == id) return true
            return false
        },
    },

    mounted: function () {
        this.startSocket()
    },

    watch: {
        
    },

    components: {
        'Package': {
            props: ['message', '_sender', 'datetime', '_id'],

            template: `
                <!-- Agent - start -->
                <div class="m-b" v-if="this.sender != 'me'">
                    <a href="" class="pull-right w-40 m-l-sm"><img src="../../static/dashboard/images/a3.jpg" class="w-full img-circle" alt="..."></a>
                    <div class="clear text-right">
                        <div class="p-a p-y-sm info inline text-left r">{{ message }}</div>
                        <div class="text-muted text-xs m-t-xs">{{ datetime }}</div>
                    </div>
                </div>
                <!-- Agent - end -->
                
                <!-- User - start -->
                <div class="m-b" v-else>
                <a href="" class="pull-left w-40 m-r-sm"><img src="../../static/dashboard/images/a3.jpg" class="w-full img-circle" alt="..."></a>
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