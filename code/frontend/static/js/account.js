$(document).ready(function () {
    $('#show_email').on('click', function () {
        let user_email = $('#user_email');
        user_email.prop('disabled', false);
        user_email.prop('readonly', false);
        $(this).hide();
    });

    $('#edit_password').on('click', function () {
        $('#hidden_conferma').show();
        let pass = $('#user_password');
        pass.prop('disabled', false);
        pass.prop('readonly', false);
        pass.val('');
        let pass2 = $('#user_password_2');
        pass2.prop('disabled', false);
        pass2.prop('readonly', false);
        pass2.val('');
        $(this).hide();
    });


    $('#reset').on('click', function () {
        $('#show_email').show();
        $('#edit_password').show();
        $('#hidden_conferma').hide();
        let pass = $('#user_password');
        let pass2 = $('#user_password_2');
        let user_email = $('#user_email');
        user_email.prop('disabled', true);
        user_email.prop('readonly', true);
        pass.prop('disabled', true);
        pass.prop('readonly', true);
        pass2.prop('disabled', true);
        pass2.prop('readonly', true);
        pass2.val('');

    });
})
