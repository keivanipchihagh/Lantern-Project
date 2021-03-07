$(document).ready(function() {

    $('.toggler, #close').on('click', appToggler)
    $('.body-card .card-btn, #back').on('click', chatToggler)
    $('.body-chat .input-area .textarea').on('focus', function() { $('.input-area').css('box-shadow', '0px -10px 10px 1px rgb(0 0 0 / 4%)') })

    $("[contenteditable]").focusout(function(){
        var element = $(this);
        console.log(element);
        if (!element.text().trim().length) {
            $('.input-area').css('box-shadow', 'none')
            element.empty();
        }
    });

    function appToggler() {
        $('.spinner').toggleClass('spinner-active')
        $('.toggler img').fadeToggle('fast')
        $('.app').fadeToggle('fast')
        $('.toggler .chevron-up').fadeToggle('fast')
    }    

    function chatToggler() {
        $('.header-secondary, .header-primary').toggle('fast')
        
        $('.header').toggleClass('header-shrink')

        $('.footer').toggleClass('footer-hide')      
        setTimeout(function() { $('.footer').toggle($(this).hasClass('footer-hide')) }, 300)

        $('.body-card').toggleClass('body-card-hide')
        $('.body-chat').fadeToggle('slow')
        setTimeout(function() { $('.body-card').toggle($(this).hasClass('body-card-hide')) }, 300)
        
        $('.body').toggleClass('body-extend')
    }    
})

// const App = new Vue({

//     el: '#app',

//     data: {
//         options: [],
//         selectedOption: null,
//         tabIndex: -1,
        
//         /*
//             -1 : Not Active
//              0 : Minimized
//              1 : Maximized
//              2 : Form
//         */

//         apikey: '123456789',
//         sitename: 'localhost',
//     },

//     methods: {

//         toggleApp: function () {
//             $('.app-toggler-icon,.app-toggler-logo').toggle();
//             $('.app-container').fadeToggle('fast');

//             if (this.tabIndex == -1) this.StartApp()
//             this.tabIndex = (this.tabIndex == -1) ? 1 : (this.tabIndex == 0) ? 1 : 0
//         },

//         toggleForm: function(id) {

//             sphO = $('.body-nav').find('.nav-item:eq(' + id + ') .text-meta')

//             if (id != -1) {
//                 this.selectedOption = id
//                 this.selectedPlaceholder = sphO.text()
//             } else {
//                 id = this.selectedOption
//             }

//             self = this
//             $('.body-nav').find('.nav-item:not(:eq(' + id + '))').toggleClass('nav-item-hide')
//             $('.nav-button').toggle()

//             $('.body-form').animate({ 'opacity': (self.tabIndex == 2) ? '0' : '1' }, 'fast');
//             self.tabIndex = (self.tabIndex == 1) ? 2 : 1
//         },

//         toggleChat: function() {
//         },

//         StartApp: function () {
//             $('.app-toggler-spinner').fadeIn('fast');
//             self = this

//             $.ajax({
//                 url: 'http://127.0.0.1:8000/api/v1/sites/' + self.sitename + '/services',
//                 type: 'GET',
//                 context: this,
//                 data: {
//                     action: "initialize",
//                     apikey: self.apikey,                    
//                 },
//                 error: function (error) { $('.app-toggler').text(error.responseJSON.msg).toggleClass('app-failure'); $('.app-container').remove() },
//                 success: function (data) {
                    
//                     data['app']['formtitles'].split(',').forEach(formtitle => { $('form select').append('<option value="' + formtitle + '">' + formtitle + '</option>') })

//                     $('.app-title').text(data['app']['title'])
//                     $('.app-placeholder').text(data['app']['placeholder'])

//                     data['options'].forEach(function(option, i) {
//                         if (option.service == true) $('.body-nav').append('<div id="nav_' + (i + 1) + '" class="nav-item"><h5>' + option.title + '</h5><span id="nav_' + (i + 1) + '_placeholder" class="text-meta">' + option.placeholder + '</span><button class="button nav-button" onclick="App.toggleForm(\'' + (i + 1) + '\')"><span class="material-icons">send</span><span class="btn-text">start</span></button></div>')
//                         self.options.push(option)
//                     });
//                     $('.app-toggler-spinner').fadeOut('fast');
//                 },
//             });
//         },
//     },
// })

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