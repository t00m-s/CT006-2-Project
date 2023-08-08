function getFile(fileID) {
  let tmp = "/viewfile/" + fileID;
  document.getElementById("file").innerHTML =
    '<embed type="application/pdf" src=' + tmp + "></embed>";
  document.getElementById("file").classList.remove("d-none");
}
