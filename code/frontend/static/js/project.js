function getFile(fileID) {
  let tmp = "/viewfile/" + fileID;
  document.getElementById("file").innerHTML =
    '<embed type="application/pdf" src=' + tmp + "></embed>"; // TODO make it work with multiple mime types
  document.getElementById("file").style.display = "block";
  console.log("Button clicked: " + fileID);
}
