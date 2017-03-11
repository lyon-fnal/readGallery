#' Use an Art Data Product
#'
#' Before you read data, you must declare what data products you want to read. You pass in the
#' full C++ name of the object, including wrapped in \code{std::vector<>} if necessary.
#' Note that you may need to look at your console output for error messages.
#'
#' @param dataProductString The data product (perhaps with std::vector) that you want to use
#'
#' @return Nothing
#' @export
#'
#' @examples
#' \dontrun{
#' useDataProduct('std::vector<gm2truth::GhostDetectorArtRecord>')
#' useDataProduct('gm2info::SpecialEventInfoRecord')
#' }
useDataProduct <- function(dataProductString) {
  pkg.env$readGalleryPy$provide_get_valid_handle(dataProductString)
}


#' Create an Art Input Tag from the tag string
#'
#' @param tag The tag string. The tag can have up to three parts separated by colon:
#'            \code{moduleLabel:instanceLabel:processName}. Usually, you only need the \code{moduleLabel}.
#'            Sometimes you may need the \code{instanceLabel}. Rarely will you need the \code{processName}.
#'
#' @return The python representation of the C++ \code{art::InputTag} object
#' @export
#'
#' @examples
#' \dontrun{
#' ghostTag <- artInputTag('artg4:GhostCylinderDetector')
#' calTag <- artInputTag('artg4')
#' }
artInputTag <- function(tag) {
  pkg.env$readGalleryPy$createInputTag(tag)
}

#' Create a reader class from a string
#'
#' See Vignette for more information
#'
#' @param s
#'
#' @return The main python environment. Use it to extract the class. See Vignette
#' @export
#'
createReaderClass_from_string <- function(s){
  main <- reticulate::py_run_string(s)
  main
}

#' Create a reader class from a file
#'
#' See Vignette for more information
#'
#' @param f
#'
#' @return The main python environment. Use it to extract the class. See Vignette
#' @export
createReaderClass_from_file <- function(f){
  main <- reticulate::py_run_file(f)
  main
}

#' Read data from Gallery
#'
#' @param theFile A file or list of files to process
#' @param reader A reader or list of readers to use for processing
#'
#' @return Timing information
#' @export
getGalleryData <- function(theFile, reader) {

  # Convert file names to std::vector
  fileVec <- createFileVector(theFile)

  # If necessary, convert a list of readers to the GalleryReaders object
  if ( typeof(reader) == "list" ) {
    reader <- readersFromList( reader )
  }

  # GO!
  timings <- pkg.env$readGalleryPy$getGalleryData(fileVec, reader)
  et <- timings$eventTimes

  # Print out the timings
  cat(stringr::str_interp("Timings: Overall time = ${allTime} s\n", list(allTime=timings$allTime)))
  cat(stringr::str_interp('Time per event: min=${mn}   mean=${avg}   max=${ma}\n',
                          list(mn=min(et), ma=max(et), avg=mean(et))))

  invisible(timings)
}

#' Extract the data from a reader as a data frame
#'
#' @param reader THe reader from which to extract the data frame
#'
#' @return A data frame
#' @export
galleryReader_df <- function(reader){
  # See http://stackoverflow.com/questions/42642266/turn-a-list-of-lists-with-unnamed-entries-into-a-data-frame-or-a-tibble
  df <- as.data.frame(do.call(rbind, reader$vals))
  df[] <- lapply(df, unlist)
  names(df) <- reader$colnames()
  df
}
