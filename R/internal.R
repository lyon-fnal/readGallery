#' Create the file vector
#'
#' The files must be presented to gallery as a std::vector
#' @param fileList A list of files to process
#' @return The python representation of the std::vector<std::string>
createFileVector <- function(fileList) {
  if ( length(fileList) == 1) {
    fileList <-  list(fileList)
  }
  pkg.env$readGalleryPy$createFileVector(fileList)
}

#' Create a reader object that consists of a list of readers
#'
#' @param listOfReaderObjects The list of readers to put in the object
#' @return A python representation of the GalleryReaders object
readersFromList <- function(listOfReaderObjects) {
  pkg.env$readGalleryPy$GalleryReaders(listOfReaderObjects)
}

