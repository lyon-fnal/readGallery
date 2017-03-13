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
#' See the vignette for more information
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
  cat(stringr::str_interp("Timings: Overall time = $[.3f]{allTime} s\n", list(allTime=timings$allTime)))
  cat(stringr::str_interp('Time per event: min=$[.3f]{mn}   mean=$[.3f]{avg}   max=$[.3f]{ma}\n',
                          list(mn=min(et), ma=max(et), avg=mean(et))))

  invisible(timings)
}

#' Extract the data from a reader as a data frame
#'
#' The value data in the reader is a list of rows. This function will convert that into an R data frame. Typically,
#' you simply pass the python reader object to this function and it will call reader$values() and reader$colnames()
#' to get that information. If you have a complicated reader (perhaps it holds more than one value list), then you may
#' need to use other methods from your reader object and not the defaults.
#' You can specify those methods with the \code{values} and \code{colnames} parameters respectively. If you do
#' not specify the \code{reader} object, then you must provide those two other parameters.
#'
#' @param reader The reader from which to extract the data frame. Unless overridden (see parameters below),
#'               reader$values() and reader$colnames() will be called to get that data.
#' @param values The values (in the form of a python list of rows) to convert to a data frame. If not specified, then
#'               \code{reader$values()} will be used.
#' @param colnames The column names that correspond to the values. These must be in the same order as the elements
#'                 in a row. If not specified, then \code{reader$colnames()} will be used.
#' @return A data frame
#' @export
#' @examples
#' \dontrun{
#' myReader %>% galleryReader_df
#'
#' galleryReader_df(myReader, colnames=theColumnNames)
#'
#' galleryReader_df(values=myReader$hitValues(), colnames=myReader$hitColNames())
#' galleryReader_df(values=myReader$trackValues(), colnames=myReader$trackColNames())
#' }
galleryReader_df <- function(reader, values, colnames){
  # If reader is missing, then values and volnames must be filled
  if ( missing(reader) && (missing(values) || missing(colnames))) {
    stop("reader is missing, so both values and colnames parameters must be specified")
  }

  # Fill in missing arguments from reader
  if ( missing(values) ) { values = reader$values() }
  if ( missing(colnames) ) { colnames = reader$colnames() }

  # See http://stackoverflow.com/questions/42642266/turn-a-list-of-lists-with-unnamed-entries-into-a-data-frame-or-a-tibble
  df <- as.data.frame(do.call(rbind, values))
  df[] <- lapply(df, unlist)
  names(df) <- colnames
  df
}
