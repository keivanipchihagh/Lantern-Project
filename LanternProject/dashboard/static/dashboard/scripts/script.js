var user_key = '123456789'

// ----------------------------------------------------------- Profile ----------------------------------------------------------------------



// ----------------------------------------------------------- Profile ----------------------------------------------------------------------

$('form#form_pi').submit(function(e) {
    $.ajax({
        url: 'http://127.0.0.1:8000/dashboard/v1/profile/' + user_key + '/update/pi',
        type: $(this).attr('method'),
        data: $(this).serialize(),
        error: function(){$("#submit_btn").val('Oops! Somthing went wrong').attr('class', 'btn btn-sm white m-b danger').prop('disabled', true) },
        success: function (response) { $("#submit_btn").val(response).attr('class', (response == 'Updated!' ? 'btn btn-sm white m-b success' : 'btn white m-b warn')) },
    });
})