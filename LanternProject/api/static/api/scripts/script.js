$(document).ready(function () {

    var toggledChat = false
    var socketStarted = false
    var token = '123456789'
    var chatSocket = null
    var messages = []
    var room_key = null

    setInterval(function () { if (toggledChat == false) $('.spinner').toggleClass('spinner-notice') }, 5000)

    $('.toggler, #close').on('click', appToggler)
    $('.overlay .overlay-btn, #back').on('click', chatToggler)
    $('.body .input-area .textarea').on('focus', function () { $('.input-area').css('box-shadow', '0px -10px 10px 1px rgb(0 0 0 / 4%)') })
    $('.send').on('click', function () { sendMessage() })

    $(".input-area .textarea").on('input', function () {
        if (($(this).text().trim().length == 0))
            $('.input-area .send').attr('class', 'material-icons icon-hide send')
        else
            $('.input-area .send').attr('class', 'material-icons icon-show send')
    })

    $("[contenteditable]").focusout(function () {
        var element = $(this);
        if (!element.text().trim().length) {
            $('.input-area').css('box-shadow', 'none')
            element.empty();
        }
    });

    $("[contenteditable]").keydown(function (e) {
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

            message = {id: messages.length, content: content, datetime: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), room_key: room_key}

            chatSocket.send(JSON.stringify({
                'id': message.id,
                'content': message.content,
                'datetime': message.datetime,
                'room_key': message.room_key,
            }));

            contenteditable.innerHTML = ''
        }
    }

    function appToggler() {
        $('.spinner').toggleClass('spinner-active')
        $('.toggler img').fadeToggle('fast')
        $('.app').fadeToggle('fast')
        $('.toggler .chevron-up').fadeToggle('fast')

        // chatToggler()
    }

    function chatToggler() {

        if (!socketStarted) openRoom()
        else showChat()
    }

    function showChat() {
        $('.header-secondary, .header-primary').toggle('fast')
        $('.header').toggleClass('header-shrink')
        $('.spinner').toggleClass('spinner-slow')

        $('.overlay').toggleClass('overlay-hide')
        setTimeout(function () { $('.overlay').toggle() }, 300)

        $('.footer').toggleClass('footer-hide')
        setTimeout(function () { $('.footer').toggle() }, 300)


        $('.body').toggleClass('body-hide')
        setTimeout(function () { $('.body').toggle() }, 300)

        toggledChat = !toggledChat
    }

    function openRoom() {

        $.ajax({
            url: 'http://127.0.0.1:8000/api/v1/hosts/' + window.location.hostname + '/services/rooms/start',
            type: 'GET',
            context: this,      // Essential for VueJS
            data: {
                'token': token,
            },
            error: function (xhr) {
                $('.overlay-btn').css('background', 'red').find('span').text(xhr.responseText)
            },
            success: function (data) {
                room_key = data
                startSocket()                      // Start socket
                socketStarted = true
                showChat()                
            },
        });
    }

    function startSocket() {

        chatSocket = new WebSocket('ws://' + window.location.host + '/ws/rooms/' + room_key + '/');

        chatSocket.onmessage = function (e) {
            const message = JSON.parse(e.data)

            $('#cards-container').append('<div id="' + message.id + '" class="card-wrapper right"><div class="card"><div class="card-header">You</div><div class="card-content">' + message.content + '</div><div class="card-footer">' + message.datetime + '</div></div></div>')
            messages.push(message)

            // Scroll to bottom
            var element = document.querySelector('#cards-container')
            element.scrollTop = element.scrollHeight;
        }

        chatSocket.onclose = function (e) { console.error('Server connection was terminated.'); console.log(e);}
    }
})