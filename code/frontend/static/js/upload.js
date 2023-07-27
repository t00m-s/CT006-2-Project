Dropzone.autoDiscover = false;
$(document).ready(function () {
    console.log('test');

    let input_box = $("#drop_box").dropzone({
        url: 'addproject',
        uploadMultiple: true,
        clickable: "#btn-form",
        autoProcessQueue: false,
        parallelUploads: 10,
        maxFiles: 10,
        dictDefaultMessage: "Drop File(s) Here or Click to Upload",
        acceptedFiles: 'application/pdf,text/plain,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        addedfile: file => {
            console.log(file);
            console.log('File aggiunto!');
        },
        init: function () {
            const sono_io = this;
            $('button[type=submit]').on('click', function (e) {

                //TODO FARE UN AJAX CHE PRENDE TUTTI I DATI DEL FORM E CI PUSHO DENTRO I FILE
                e.preventDefault();
                e.stopPropagation();
                sono_io.processQueue();
                $('#form_upload').submit();
            })
        }
    });
    console.log(input_box);
    /*$('#btn-form').on('click', function () {

        $('#fileID').click();
    }); */
});
