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
        if (msg.val().trim() !== '') {
            socket.send({message: msg.val(), id_project: id_project});
            msg.val('');
        }
    }
});


function scrollDown() {  //TODO FIXARE SAFARI
    $('#messages').animate({scrollTop: 999999999999999}, 100);
}


function isMe(obj) {
    let my_selector = $('#current_user_id');
    if (my_selector.length <= 0) {
        //  console.log('bb');
        return false;
    }
    let my_id = my_selector.val();
    if (obj.user_id !== undefined && my_id == obj.user_id) {

        return true;
    }
    //console.log('ccc', obj.user_id, my_id);
    return false;
}

function aggiungiMessaggio(obj) {
    let allineamento = '';
    let textPos = '';
    let extraFix = ''
    if (isMe(obj)) {
        allineamento = 'justify-content-end';
        textPos = 'text-end ';
        extraFix = ' fix_pad_mex ';
    } else {
        allineamento = 'justify-content-start';
        textPos = 'text-start ';
    }

    $("#messages").append(
        '<div class="row ">' +
        '<small class="' + textPos + extraFix + '"><i>' + obj.user_name + '</i></small>' +
        '<div class=" d-flex ' + allineamento + '">' +
        '<div class="' + textPos + ' card p-2 mt-1 mb-1 rounded">' + obj.message + '<br>' +
        '<span class="text-end timestamp"> ' + obj.timestamp + '</span>' +
        ' </div>' +
        '</div>' +
        '</div>'
    );
    // + obj.user_name + ': ' + obj.message +  + '</div>'
    scrollDown();
}
