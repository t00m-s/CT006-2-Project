/**
 * Returns the basepath of the file
 * @params file full file path
 */
function filterFile(file) {
  return file.split("/").pop();
}


$(document).ready(function() {
  $('.opener').on("click",function() {
    let container = $(this).parent(".stateContainer");

    container.find(".collapsible").toggle();
    if(container.hasClass("hovered"))
      container.removeClass("hovered");
    else
      container.addClass("hovered");

    let upDown = container.find(".upDown").find("i");

    if(upDown.hasClass("bi-chevron-down")){
      upDown.removeClass("bi-chevron-down").addClass("bi-chevron-up");
    }else{
      upDown.removeClass("bi-chevron-up").addClass("bi-chevron-down");
    }



  });
});