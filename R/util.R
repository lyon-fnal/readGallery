# Utility functions

#' Add the Fermilab public dCache URI to the front of file paths
#'
#' @param files A list of file locations (should start with /pnfs)
#' @return The file list with the Fermilab public dCache URI prepended
#' @export
#' @examples
#' xrootify("/pnfs/GM2/scratch/users/lyon/myFile.root")
xrootify <- function(files) {
  paste0('root://fndca1.fnal.gov', files)
}


#' Print out the python configuration including PYTHONPATH
#' @export
galleryPyConfig <- function() {
  reticulate::py_config()

  cat("\nPython Path is:\n")
  main <- reticulate::py_run_string("import sys ; syspath = sys.path")
  cat(main$syspath)
}
