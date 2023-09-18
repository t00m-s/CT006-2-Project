$(document).ready(function () {

    $('#check').on('click', function () {
        scrollDown();
    });

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


    const socket = io.connect('http://localhost:5001', {query: 'id_project=' + id_project});

    socket.on('connect', function () {
        socket.send({message: 'user has connected!', id_project: id_project});
    });

    socket.on('message', function (msg) {
        aggiungiMessaggio(msg);
        console.log('Received message');
    });

    $('#sendBtn').on('click', function () {
        mandaMessaggio();
    });
    $('#message').on('keypress', function (e) {
        if (e.which === 13) {
            mandaMessaggio();
        }
    });

    function mandaMessaggio() {
        let msg = $('#message');
        socket.send({message: msg.val(), id_project: id_project});
        msg.val('');
    }
});


function scrollDown() {
    $('#messages').animate({scrollTop: $(document).height()}, 100);
}


function isMe(obj) {
    let my_selector = $('#current_user_id');
    if (my_selector.length <= 0) {
        return false;
    }
    let my_id = my_selector.val();
    if (obj.user_id !== undefined && my_id === obj.user_id) {
        return true;
    }
    return false;
}

function aggiungiMessaggio(obj) {
    $("#messages").append('<div class="card mx-2 rounded">' + obj.user_name + ': ' + obj.message + '</div>');
    scrollDown();
}
