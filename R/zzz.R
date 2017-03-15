# We need an environment to hold the python import
# See bottom of http://stackoverflow.com/questions/12598242/global-variables-in-packages-in-r
pkg.env <- new.env(parent = emptyenv())

.onAttach <- function(libname, pkgname) {
  packageStartupMessage("readGallery - intializing")
}

.onLoad <- function(libname, pkgname) {

  # Add to the python path to pick up the import
  main <- reticulate::py_run_string(
    stringr::str_interp("import sys ; sys.path.append('${theDir}')",
                        list(theDir=system.file("python", package="readGallery")) ) )

  # Now import the package
  pkg.env$readGalleryPy <- reticulate::import("readGallery")
  pkg.env$galleryReaderSkel <- reticulate::import("galleryReaderSkel")
}


