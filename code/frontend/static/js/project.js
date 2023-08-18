/**
 * Returns the basepath of the file
 * @params file full file path
 */
function filterFile(file) {
  return file.split("/").pop();
}
