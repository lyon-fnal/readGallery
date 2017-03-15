# Do the gallery reader skeleton

#' Create a Gallery Reader Skeleton
#'
#' This function aids you in writing a Gallery Reader class.
#'
#' @param extractClass  - The name of the class, with namespace, that is extracted from Gallery
#' @param fillClass - The name of the class to be filled, Usually same as extractClass (default NULL does this)
#' @param wrapExtractVector - If TRUE, wrap the extract class in a vector
#' @param wrapFillVector - if TRUE, wrap the fill class in a vector (default, NULL, is to copy wrapExtractVector)
#' @param writeFile - Write the text to a file named \code{writeFile}
#'
#' @return [Invisibly] the text of the class
#' @export
readerClassSkel <- function(extractClass, fillClass=NULL, wrapExtractVector=TRUE, wrapFillVector=NULL,
                                  writeFile=NULL) {

  out <- pkg.env$galleryReaderSkel$readerClassSkel(extractClass, fillClass = fillClass,
                                                   wrapExtractVector = wrapExtractVector,
                                                   wrapFillVector = wrapFillVector,
                                                   writeFile = writeFile)
  invisible(out)
}
