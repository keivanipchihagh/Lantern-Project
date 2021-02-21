const ChatApp = new Vue({

    el: "#profile",    

    data: {
        user_key: '123456789'
    },

    methods: {

        update_pi: function() {            
            self = this

            $.ajax({
                url: 'http://127.0.0.1:8000/dashboard/v1/profile/' + self.user_key + '/update/pi',
                headers: { "X-CSRFToken": $('#csrfmiddlewaretoken').val() },
                type: 'GET',
                context: this,      // Essential for VueJS
                data: $('#form_pi').serialize(),
                error: function(xhr, ajaxOptions, thrownError){
                    alert(thrownError + '\n' + xhr.status + '\n' + ajaxOptions);
                },
                success: function (data) {
                },
            });
        },
    },

    mounted: function () {
        self = this
        $('#form_pi').submit(function(e) {            
            $.ajax({
                url: 'http://127.0.0.1:8000/dashboard/v1/profile/' + self.user_key + '/update/pi',
                type: 'PUT',
                context: this,      // Essential for VueJS
                data: $('#form_pi').serialize(),
                error: function(xhr, ajaxOptions, thrownError){
                    alert(thrownError + '\n' + xhr.status + '\n' + ajaxOptions);
                },
                success: function (data) {
                    alert(data)
                },
            });
        })
        
    },

    watch: {
        
    },

    components: {        
    }
})