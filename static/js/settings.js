// Execute the script after page loads.
$('document').ready(function(){
    $('#set_new_password').click(function(){
        $.ajax({
            url: '/auth/_new_password',
            data: {
                old_password: $('#old_password').val(),
                new_password: $('#new_password').val()
            },
            success: function(data) {
                if (data['success'] == true)  {
                    if (!$('#message_box').length) {
                        $('#modal-new-password').prepend(`<div id='message_box' class="alert alert-success" role="alert">
                                Password has been successfully changed.
                            </div>`)
                    } else {
                        $('#message_box').removeClass('alert-danger')
                        $('#message_box').addClass('alert-success')
                        $('#message_box').text('Password has been successfully changed.')
                    }
                } else {
                    if (!$('#message_box').length) {
                        $('#modal-new-password').prepend(`<div id='message_box' class="alert alert-danger" role="alert">
                                Incorrect old password.
                            </div>`)
                    } else {
                        $('#message_box').removeClass('alert-success')
                        $('#message_box').addClass('alert-danger')
                        $('#message_box').text('Incorrect old password.')
                    }
                }
            }
        })
    })
});