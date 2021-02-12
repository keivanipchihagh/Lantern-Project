config = {
    'lantern-project': {
        'id': '012023',                                  // Unique ID for the client
        'version': '1.0.0',                              // App version

        'settings': {
            'position': {
                'default': 'right',                     // Default position (right | left)
                'control': 'true',                      // User control over position (true | false)
                'padding-bottom': '30px',               // Bottom padding
                'padding-sides': '40px',                // Sides padding
            },
            'size': {
                'width': '420px',                       // Width
                'height': '500px',                      // Height
                'override-height': 'false'              // When 'true', max-height will be ignored (true | false)
            },
            'theme': {
                'default': 'light',                     // Default theme (light | dark)
                'control': 'true'                       // User control over (true | false)
            },
            'dir': {
                'default': 'LTR'                        // Text direction (LTR | RTL)
            },
            'general': {
                'title': 'Live Support',                // Title
                'header-high-contrast': 'false'         // High contrast for header
            }
        },
    }
}

const chatboxApp = new Vue({

    el: "#chatbox-app",

    data: {
        packages: [],        
        session_token: null,
        message: '',

        roomName: null,
        chatSocket: null,

        // General settings
        title: '',
        headerHighContrast: false,

        // Visible
        showSettings: true,        

        // Ready server
        ready: false,

        // State of App (Minimized | Maximized)
        expandApp: false,
        active: false,

        // Visibility of the App
        showApp: true,

        // Theme | Default: 'light' | Default-Control: 'true'
        theme: 'light',
        themeControl: true,

        // Position | Default: 'right' | Default-Control: 'true'
        position: 'right',
        positionControl: true,
        paddingBottom: 0,
        paddingSides: 0,

        // Size
        width: 0,
        height: 0,
        overrideHeight: false,

        // Text direction | Default: 'LTR'
        dir: 'LTR',        
    },

    methods: {

        sendMessage: function () {
            document.querySelector('#chat-message-input').focus();
            document.querySelector('#chat-message-submit').click();
        },

        toggleApp: function () {
            $("#toggler").attr({ "uk-icon": function (index, currentvalue) { return (currentvalue == "icon: chevron-down") ? "icon: chevron-up" : "icon: chevron-down" }, "title": function (index, currentvalue) { return (currentvalue == "minimize") ? "maximize" : "minimize" } })
            this.expandApp = !this.expandApp

            if (!this.active) {
                // this.startSession()

                this.active = !this.active
                this.ready = true
            }            
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
                url: 'http://127.0.0.1:8000/api/v1/sessions/start',
                type: 'GET',
                context: this,      // Essential for VueJS
                error: function (jqXHR, textStatus, errorThrown) {
                    console.log(textStatus);
                    console.log(errorThrown);
                    console.log(jqXHR);
                },
                success: function (data) {
                    this.session_token = data; console.log('Session started successfully.');
                },
            });
        },
    },

    mounted: function () {

        // let newItem = new Vue(Object.assign({}, 'package', {
        //     parent: this,
        //     propsData: {
        //         message: 'Hi',
        //         _sender: 'me',
        //         datetime: new Date().getTime(),
        //         _id: 1
        //     },
        // })).$mount('#chat-log');

        // console.log(newItem);

        // ------------------------------------------------------- Channels --------------------------------------------------------------------                

        const roomName = JSON.parse(document.getElementById('room-name').textContent);
        const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/' + roomName + '/' );

        chatSocket.onmessage = function (e) {
            const data = JSON.parse(e.data);            
            document.querySelector('#chat-log').innerHTML += (data.message + '\n');
        };

        chatSocket.onclose = function (e) {
            console.error('Chat socket closed unexpectedly');
        };

        // document.querySelector('#chat-message-input').focus();
        // document.querySelector('#chat-message-input').onkeyup = function (e) {
        //     if (e.keyCode === 13)
        //         document.querySelector('#chat-message-submit').click();
        // };

        document.querySelector('#chat-message-submit').onclick = function (e) {
            const messageInputDom = document.querySelector('#chat-message-input');
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInputDom.value = '';
        };
        // ------------------------------------------------------- Channels --------------------------------------------------------------------

        // global
        this.token = config['lantern-project']['token']

        // settings - theme
        this.theme = config['lantern-project']['settings']['theme']['default']
        this.themeControl = (config['lantern-project']['settings']['theme']['control'] == 'true')

        // settings - position
        this.position = config['lantern-project']['settings']['position']['default']
        this.positionControl = (config['lantern-project']['settings']['position']['control'] == 'true')
        this.paddingBottom = config['lantern-project']['settings']['position']['padding-bottom']
        this.paddingSides = config['lantern-project']['settings']['position']['padding-sides']

        // settings - size
        this.width = config['lantern-project']['settings']['size']['width']
        this.height = config['lantern-project']['settings']['size']['height']
        this.overrideHeight = (config['lantern-project']['settings']['size']['override-height'] == 'true')

        // settings - dir
        this.dir = config['lantern-project']['settings']['dir']['default']

        // settings - general
        this.title = config['lantern-project']['settings']['general']['title']
        $("#title").html('&nbsp; ' + this.title)
        this.headerHighContrast = (config['lantern-project']['settings']['general']['header-high-contrast'] == 'true')

        // Hides the Settings panel if no settings are shown
        if (!(this.positionControl || this.themeControl))
            this.showSettings = false

        // Set settings
        $('#chatbox-app').css('padding-bottom', this.paddingBottom)
        $('#chatbox-app').children(0).css({ 'padding-left': this.paddingSides, 'padding-right': this.paddingSides, 'width': this.width })
        $('#chatbox-content').css({'max-height': (this.overrideHeight) ? this.height : $(document).height() * 0.5})
    },

    watch: {
        'session_token': function(token) {
          if (token != null)
            this.ready = true
        }
    },

    components: {
        'package': {
            props: ['message', '_sender', 'datetime', '_id'],

            template: `
                <div id="this.id" class="uk-grid-small uk-flex-bottom uk-flex-right uk-text-right uk-flex" v-bind:class="[(this.sender == 'me') ? 'me' : 'agent']" uk-grid>
                    <div class="uk-width-auto uk-flex-1" v-if="this.sender == 'me'"><div class="uk-card uk-card-body uk-card-small uk-border-rounded-me" v-bind:class="[(this.sender == 'me') ? ['uk-card-primary', 'uk-float-right'] : ['uk-card-default', 'uk-float-left']]"><p class="uk-margin-remove">{{ message }}</p><p class="uk-margin-remove uk-time-p">{{ datetime }}</p></div></div>
                    <div class="uk-width-auto" v-if="this.sender == 'me'"><img class="uk-border-circle" width="32" height="32" src="../../../static/api/images/avatar.jpg" /></div>
                    <div class="uk-width-auto" v-if="this.sender != 'me'"><img class="uk-border-circle" width="32" height="32" src="../../../static/api/images/avatar.jpg" /></div>
                    <div class="uk-width-auto uk-flex-1" v-if="this.sender != 'me'"><div class="uk-card uk-card-body uk-card-small uk-border-rounded-agent" v-bind:class="[(this.sender == 'me') ? ['uk-card-primary', 'uk-float-right'] : ['uk-card-default', 'uk-float-left']]"><p class="uk-margin-remove">{{ message }}</p><p class="uk-margin-remove uk-time-p">{{ datetime }}</p></div></div>
                </div>
                `,

            data: function () {
                return {
                    sender: this._sender,
                    id: this._id,
                }
            }
        }
    }
})