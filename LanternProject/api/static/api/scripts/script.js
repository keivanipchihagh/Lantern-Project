$(document).ready(function() {

    var toggled = false

    setInterval(function() {
        if (toggled == false)
            $('.spinner').toggleClass('spinner-notice')
    }, 5000)

    $('.toggler, #close').on('click', appToggler)
    $('.overlay .overlay-btn, #back').on('click', chatToggler)
    $('.body .input-area .textarea').on('focus', function() { $('.input-area').css('box-shadow', '0px -10px 10px 1px rgb(0 0 0 / 4%)') })
    $('.send').on('click',function() { sendMessage() })

    $(".input-area .textarea").on('input', function() {
        if (($(this).text().trim().length == 0))
            $('.input-area .send').attr('class', 'material-icons icon-hide send')
        else
            $('.input-area .send').attr('class', 'material-icons icon-show send')
    })   

    $("[contenteditable]").focusout(function(){
        var element = $(this);
        if (!element.text().trim().length) {
            $('.input-area').css('box-shadow', 'none')
            element.empty();
        }
    });

    $("[contenteditable]").keydown(function(e){
        if (e.keyCode === 13) {
            sendMessage()
            e.preventDefault();
            return false;
        }
    });

    function sendMessage() {
        var contenteditable = document.querySelector('[contenteditable]')
        content = (contenteditable.textContent || contenteditable.innerText).trim()
        if (content != '') {
            console.log(content)
            contenteditable.innerHTML = ''
        }
    }

    function appToggler() {
        $('.spinner').toggleClass('spinner-active')
        $('.toggler img').fadeToggle('fast')
        $('.app').fadeToggle('fast')
        $('.toggler .chevron-up').fadeToggle('fast')

        chatToggler()
    }    

    function chatToggler() {
        $('.header-secondary, .header-primary').toggle('fast')
        $('.header').toggleClass('header-shrink')
        $('.spinner').toggleClass('spinner-slow')

        $('.overlay').toggleClass('overlay-hide')
        setTimeout(function() { $('.overlay').toggle() }, 300)

        $('.footer').toggleClass('footer-hide')      
        setTimeout(function() { $('.footer').toggle() }, 300)
        
        
        $('.body').toggleClass('body-hide')
        setTimeout(function() { $('.body').toggle() }, 300)

        toggled = !toggled
    }
})

// const App = new Vue({

//     // el: "#chatbox-app",
//     el: "#app",

//     data: {
//         messages: [],
//         api_key: '123456789',
//         room_token: '',

//         // Ready server
//         ready: false,

//         message: '',
//         emptyMessage: true,

//         // State of App (Minimized | Maximized)
//         expandHeader: false,
//         showHeader: false,
//         expandApp: false,

//         // Visibility of the App
//         showApp: true,

//         // Theme
//         isDark: false,

//         // Etc toggle
//         dotToToggle: 0,
//     },

//     methods: {

//         sendMessage: function () {
//             document.querySelector('#chat-message-submit').click()
//         },
//         toggleHeader: function() {
//             if (!this.expandApp)
//                 this.expandHeader = !this.expandHeader         
//         },
//         toggleApp: function () {

//             if (!this.ready)
//                 this.openRoom()
//             else {
//                 this.expandApp = !this.expandApp
//                 $("#toggler").attr({ "uk-icon": function (index, currentvalue) { return (currentvalue == "icon: chevron-down") ? "icon: chevron-up" : "icon: chevron-down" }})            
//             }
//         },
//         closeApp: function () {
//             this.showApp = false
//         },
//         changeTheme: function () {
//             this.isDark = !this.isDark
//         },
//         openRoom: function () {

//             var self = this
//             var dots = [$("#dot_1"), $("#dot_2"), $("#dot_3")]
//             var await = setInterval(function() {dots[self.dotToToggle++].toggleClass('uk-etc-dot-show uk-etc-dot-hide'); if (self.dotToToggle == 3) self.dotToToggle = 0; }, 500)

//             $.ajax({
//                 url: 'http://127.0.0.1:8000/api/v1/services/rooms/start',
//                 type: 'GET',
//                 context: this,      // Essential for VueJS
//                 data: {
//                     'key': this.api_key
//                 },
//                 error: function () {
//                     console.log('There was a problem creating a room.');
//                 },
//                 success: function (data) {
//                     this.ready = true                       // Ready status
//                     this.room_token = data               // Set room token                    
//                     this.startSocket()                      // Start socket
//                     console.log('Room started.');

//                     // Open chat when ready
//                     this.expandApp = !this.expandApp
//                     $("#toggler").attr({ "uk-icon": function (index, currentvalue) { return (currentvalue == "icon: chevron-down") ? "icon: chevron-up" : "icon: chevron-down" }, "title": function (index, currentvalue) { return (currentvalue == "minimize") ? "maximize" : "minimize" } })            

//                     clearInterval(await)
//                     dots.map(function(e) {
//                         e.addClass('uk-etc-dot-hide')
//                     })
//                 },
//             });
//         },
//         startSocket: function () {

//             const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/rooms/' + this.room_token + '/');
//             self = this

//             chatSocket.onmessage = function (e) {
//                 const data = JSON.parse(e.data)

//                 var message = { id: data['id'], message: data['message'], datetime: data['datetime'], sender: 'agent' }

//                 // Push agent messages only
//                 if (!App.messageExists(message['id'])) App.messages.push(message)
//             }

//             document.querySelector('#chat-message-submit').onclick = function (e) {
//                 // const message = self.message

//                 var message = { id: App.messages.length, message: App.message.replace(/\n/g, ''), datetime: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), sender: 'client' }

//                 chatSocket.send(JSON.stringify({
//                     'id': message['id'],
//                     'message': message['message'],
//                     'datetime': message['datetime'],
//                     'room_key': self.room_token,
//                     'sender': message['sender'],
//                 }));

//                 self.message = ''
//                 App.messages.push(message)
//             }

//             chatSocket.onclose = function (e) { console.error('Server connection was terminated.') }
//         },
//         messageExists: function (id) {
//             for (var i = 0; i < this.messages.length; i++) if (this.messages[i]['id'] == id) return true
//             return false
//         },
//     },

//     mounted: function () {
//         $('#app-content').css({ 'max-height': $(document).height() * 0.5 })       
//     },

//     watch: {
//         message: function(val) { this.emptyMessage = (val == '' || val == undefined) ? true : false }
//     },

//     components: {
//         'Message': {
//             props: ['message', '_sender', 'datetime', '_id'],

//             template: `
//                 <div id="this.id" class="uk-grid-small uk-flex-bottom uk-flex-right uk-text-left uk-flex client" v-if="this.sender == 'client'" uk-grid>                    
//                     <div class="uk-width-auto uk-flex-1"><div class="uk-card uk-card-body uk-card-small uk-border-rounded-type1 uk-card-primary uk-float-right"><p class="uk-margin-remove">{{ message }}</p><p class="uk-margin-remove uk-time-p">{{ datetime }}</p></div></div>
//                     <div class="uk-width-auto"><img class="uk-border-circle" width="32" height="32" src="../../../static/api/images/avatar.jpg" /></div>
//                 </div>
//                 <div id="this.id" class="uk-grid-small uk-flex-bottom uk-flex-right uk-text-left uk-flex agent" v-else uk-grid>                    
//                     <div class="uk-width-auto"><img class="uk-border-circle" width="32" height="32" src="../../../static/api/images/avatar.jpg" /></div>
//                     <div class="uk-width-auto uk-flex-1"><div class="uk-card uk-card-body uk-card-small uk-border-rounded-type2 uk-card-default uk-float-left"><p class="uk-margin-remove">{{ message }}</p><p class="uk-margin-remove uk-time-p">{{ datetime }}</p></div></div>
//                 </div>`,

//             data: function () {
//                 return {
//                     sender: this._sender,
//                     id: this._id,
//                 }
//             }
//         }
//     }
// })