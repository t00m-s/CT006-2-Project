/**
 * Returns the basepath of the file
 * @params file full file path
 */
function filterFile(file) {
  return file.split("/").pop();
}


$(document).ready(function() {
  $('.stateContainer').on("click",function() {
    $(this).children(".collapsible").toggle();
    if($(this).hasClass("hovered"))
      $(this).removeClass("hovered");
    else
      $(this).addClass("hovered");

    let upDown = $(this).children(".upDown");

    if(upDown.hasClass("bi-chevron-down")){
      upDown.removeClass("bi-chevron-down").addClass("bi-chevron-up");
    }else{
      upDown.removeClass("bi-chevron-up").addClass("bi-chevron-down");
    }



  });
});