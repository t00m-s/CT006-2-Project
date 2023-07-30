Dropzone.autoDiscover = false;
$(document).ready(function () {
    let input_box = $("#form_upload").dropzone({
        url: 'addproject',
        uploadMultiple: true,
        clickable: "#btn-form",
        addRemoveLinks: true,
        previewsContainer: '.previews',
        dictRemoveFile: "Rimuovi",
        autoProcessQueue: false,
        parallelUploads: 100,
        maxFiles: 100,
        dictDefaultMessage: '',
        acceptedFiles: 'application/pdf,text/plain,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document',

        init: function () {
            const sono_io = this;
            $('button[type=submit]').on('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                sono_io.processQueue();

            });
            sono_io.on("sendingmultiple", function () {
                // Gets triggered when the form is actually being sent.
                // Hide the success button or the complete form.
            });
            sono_io.on("successmultiple", function (files, response) {
                window.location.replace("/projects");
            });
            sono_io.on("errormultiple", function (files, response) {
                alert(response);
            });
            sono_io.on("addedfile", file => {
                dropdownOpen();
            });
        }
    });
    $('#type').select2({
        width: '100%' // need to override the changed default
    });

});

tinymce.init({
    selector: 'textarea#tiny',
    plugins: [
        'a11ychecker', 'advlist', 'advcode', 'advtable', 'autolink', 'checklist', 'export',
        'lists', 'link', 'image', 'charmap', 'preview', 'anchor', 'searchreplace', 'visualblocks',
        'powerpaste', 'fullscreen', 'formatpainter', 'insertdatetime', 'media', 'table', 'help', 'wordcount'
    ],
    toolbar: 'undo redo | a11ycheck casechange blocks | bold italic backcolor | alignleft aligncenter alignright alignjustify |' +
        'bullist numlist checklist outdent indent | removeformat | code table help'
});

function dropdownOpen() {
    if ($("#card-dropdown:visible").length === 0) {
        $("#card-dropdown").toggle();
    }
}
