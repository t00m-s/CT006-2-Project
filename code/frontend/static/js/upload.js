const descri = tinymce.init({
  selector: "textarea#tiny",
  plugins: [
    "advlist",
    "autolink",
    "lists",
    "link",
    "image",
    "charmap",
    "preview",
    "anchor",
    "searchreplace",
    "visualblocks",
    "fullscreen",
    "insertdatetime",
    "media",
    "table",
    "help",
    "wordcount",
  ],
  toolbar:
    "undo redo | a11ycheck casechange blocks | bold italic backcolor | alignleft aligncenter alignright alignjustify |" +
    "bullist numlist checklist outdent indent | removeformat | code table help",
});

Dropzone.autoDiscover = false;
$(document).ready(function () {
  let input_box = $("#form_upload").dropzone({
    url: "addproject",
    uploadMultiple: true,
    clickable: "#btn-form",
    addRemoveLinks: true,
    previewsContainer: ".previews",
    dictRemoveFile: "Rimuovi",
    maxFilesize: 10,
    autoProcessQueue: false,
    parallelUploads: 100,
    maxFiles: 100,
    dictDefaultMessage: "",
    acceptedFiles: "application/pdf",
    init: function () {
      const sono_io = this;
      $("button[type=submit]").on("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        tinymce.get("tiny").save();
        sono_io.processQueue();
      });
      sono_io.on("sendingmultiple", function () {
        // Gets triggered when the form is actually being sent.
        // Hide the success button or the complete form.
      });
      sono_io.on("successmultiple", function (files, response) {
        window.location.replace("/viewproject/" + response.new_project_id);
      });
      sono_io.on("errormultiple", function (files, response) {
        alert(response);
      });
      sono_io.on("addedfile", (file) => {
        cardDropdownOpen();
      });
      /*
       * Quando un file viene rimosso se non ce ne sono altri viene
       * chiuso il form sottostante
       */
      sono_io.on("removedfile", (file) => {
        if ($(".dz-preview:visible").length === 0) cardDropdownClose();
      });
    },
  });
  $("#type").select2({
    width: "100%", // need to override the changed default
  });
});

function cardDropdownOpen() {
  if ($("#card-dropdown:visible").length === 0) {
    $("#card-dropdown").toggle();
  }
}

function cardDropdownClose() {
  if ($("#card-dropdown:visible").length > 0) {
    $("#card-dropdown").toggle();
  }
}
