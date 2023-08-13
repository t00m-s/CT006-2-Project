$(document).ready(function () {

    const id_project = $('#id_project').val();
    $.ajax({
        url: "/chat/" + id_project,
        success: function (response) {
            $.each(response, function (key, val) {
                aggiungiMessaggio(val);
            });
        },
        error: function () {
            alert('ERROR WHILE GETTING OLD CHAT MESSAGES');
        }
    });


    const socket = io.connect('http://localhost:5001');

    socket.on('connect', function () {
        socket.send({message: 'user has connected!', id_project: id_project});
    });

    socket.on('message', function (msg) {
        aggiungiMessaggio(msg);
        console.log('Received message');
    });

    $('#sendBtn').on('click', function () {
        let msg = $('#message');
        socket.send({message: msg.val(), id_project: id_project});
        msg.val('');
    });

});


function aggiungiMessaggio(obj) {
    $("#messages").append('<li>' + obj.user_name + ': ' + obj.message + '</li>');
}
