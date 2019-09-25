
// Execute the script after page loads.
$('document').ready(function(){
    
    $('#pwd_user_find').click(function() {
    $.ajax({
        url: '/auth/_reset_pwd',
        data: {
            username: $('#pwd_username').val(),
            step: 1
            },
        success: function(data) {
            if (data['done'] == true) {
                
                // If there is error msg - remove it
                if ($('#alert_err').length) {
                    $('#alert_err').remove()
                }

                $('#modal-parent').append(`<p class='text-info text-center'>Please, answer the following question: </p>`);
                $('#modal-parent').append(`<p class='text-center'>${data.secret_q}</p>`);
                $('#modal-parent').append(`
                <div class="input-group">
                    <input type="text" class="form-control" id='secret_q_ans'>
                    <div class="input-group-append">
                        <button class="btn btn-primary" id='check_ans'>Check</button>
                    </div>
                </div>
                `)

                // Disable DOM from step 1
                $('#pwd_username').attr('disabled', 'disabled')
                $('#pwd_user_find').attr('disabled', 'disabled')

            } else {
                // If error msg already exists - don't create more.
                if (!$('#alert_err').length) {
                    $('#modal-parent').prepend(`<div id='alert_err' class="alert alert-danger" role="alert">
                            Can't find such user, please - check your username.
                        </div>`)
                }
            }
        }
        });
    });

    // I use 'on' because this button is created dynamically.
    $('#modal-parent').on('click', '#check_ans', function() {
        $.ajax({
            url: '/auth/_reset_pwd',
            data: {
                username: $('#pwd_username').val(),
                step: 2,
                secret_q_ans: $('#secret_q_ans').val()
                },
            success: function(data) {
                if (data['done'] == true) {
                    
                    // If there is error msg - remove it
                    if ($('#alert_err').length) {
                        $('#alert_err').remove()
                    }


                    $('#modal-parent').append(`<p class='text-info text-center'>Please, specify the new password: </p>`);
                    $('#modal-parent').append(`
                    <div class="input-group">
                        <input type="text" class="form-control" id='new_pwd'>
                        <div class="input-group-append">
                            <button class="btn btn-primary" id='set_pwd'>Set password</button>
                        </div>
                    </div>
                    `)

                    // Disable DOM from step 2
                    $('#secret_q_an').attr('disabled', 'disabled')
                    $('#check_ans').attr('disabled', 'disabled')
    
                } else {
                    // If error msg already exists - don't create more.
                    if (!$('#alert_err').length) {
                        $('#modal-parent').prepend(`<div id='alert_err' class="alert alert-danger" role="alert">
                                Wrong answer - please try again.
                            </div>`)
                    }
                }
            }
            });
        });


// I use 'on' because this button is created dynamically.
$('#modal-parent').on('click', '#set_pwd', function() {
    $.ajax({
        url: '/auth/_reset_pwd',
        data: {
            username: $('#pwd_username').val(),
            step: 3,
            new_pwd: $('#new_pwd').val()
            },
        success: function(data) {
            if (data['done'] == true) {
                
                // If there is error msg - remove it
                if ($('#alert_err').length) {
                    $('#alert_err').remove();
                }
                
                // I have 2 JQueries - 1 from bootstrap and 1 general, so disable conflicts
                jQuery.noConflict(); 
                // Hide modal (JQuery Bootstrap method)
                $('#forgotPassModal').modal('hide');

                // Disable DOM from step 3
                $('#new_pwd').attr('disabled', 'disabled');
                $('#set_pwd').attr('disabled', 'disabled');

            } else {
                // If error msg already exists - don't create more.
                if (!$('#alert_err').length) {
                    $('#modal-parent').prepend(`<div id='alert_err' class="alert alert-danger" role="alert">
                            Something went wrong. Please try again.
                        </div>`)
                }
            }
        }
        });
    });

});