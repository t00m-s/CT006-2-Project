$(document).ready(function () {

    var socket = io.connect('http://localhost:5001');

    socket.on('connect', function () {
        socket.send('User has connected!');
    });

    socket.on('message', function (msg) {
        $("#messages").append('<li>' + msg + '</li>');
        console.log('Received message');
    });

    $('#sendBtn').on('click', function () {
        socket.send($('#message').val());
        $('#message').val('');
    });

});
