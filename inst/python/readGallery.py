#!/bin/env python

# Python package to read data from Gallery

import ROOT
import time

def read_header(h):
  """Make the ROOT C++ jit compiler read the specified header."""
  ROOT.gROOT.ProcessLine('#include "%s"' % h)

def provide_get_valid_handle(klass):
  """Make the ROOT C++ jit compiler instantiate the
     Event::getValidHandle member template for template
     parameter klass."""
  ROOT.gROOT.ProcessLine('template gallery::ValidHandle<%(name)s> gallery::Event::getValidHandle<%(name)s>(art::InputTag const&) const;' % {'name' : klass})

# Let's load the gallery header
read_header("gallery/ValidHandle.h")

def createFileVector(fileList) :
  """Gallery requires a std::vector of file locations (not a python list).
     This function does that conversion."""
  theFiles = ROOT.vector(ROOT.string)()
  [ theFiles.push_back(x) for x in fileList ]
  return theFiles

def createInputTag(tag):
  """Given an input tag string (like artg4:GhostNearWorldDetector), return a real art::InputTag object"""
  return ROOT.art.InputTag(tag)

class GalleryTimer:
  """A little class to collect timings from a Gallery read run. Used internally"""
  def __init__(self):
    self._allStart = time.clock()
    self._totalReadStart = None
    self._eventStart = None
    self.allTime = None
    self.totalReadTime = None
    self.eventTimes = []

  def startTotalRead(self):
    self._totalReadStart = time.clock()

  def startEvent(self):
    self._eventStart = time.clock()

  def doneEvent(self):
    self.eventTimes.append(time.clock() - self._eventStart)

  def done(self):
    t = time.clock()
    self.totalReadTime = t - self._totalReadStart
    self.allTime = t - self._allStart

  def __str__(self):
    print 'NICE STUFF'

class GalleryReaders:
  """A helper class you can use to fill multiple readers"""
  def __init__(self, readerList):
    self.readerList = readerList

  def prepare(self, ROOT, ev):
    [ x.prepare(ROOT, ev) for x in self.readerList ]

  def fill(self, ROOT, ev):
    rets = [ x.fill(ROOT, ev) for x in self.readerList ]
    return all(rets)

def getGalleryData(fileVector, readerObject):
  """Get data from gallery. First argument is a vector of files to run over.
     The second argument is an object that has the following methods...
         readerObject.prepare(ev)  where ev is a ROOT.gallery.Event. In this method the object should call its
                                   getValidHandle methods and store them away
         readerObject.fill(ev) where ev is a ROOT.gallery.Event. This method gets the event and should do
                                   everything that needs to happen to fill. The method should return a boolean.
                                   If false is returned, then the event loops end
      The function returns the time it took to run the read"""


  gt = GalleryTimer()

  print 'Opening first file...'
  ev = ROOT.gallery.Event(fileVector)
  readerObject.prepare(ROOT, ev)

  gt.startTotalRead()

  while not ev.atEnd():

    gt.startEvent()
    ret = readerObject.fill(ROOT, ev)
    gt.doneEvent()

    if not ret:
      break

    ev.next()

  gt.done()
  return gt
