#!/bin/env python

# Generate a gallery Reader class from a skeleton

import readGallery
import os

skel = """from readGallery import GalleryReaderBase  # Necessary for the base class

class %(skelName)s(GalleryReaderBase):
  def __init__(self, inputTag):
    GalleryReaderBase.__init__(self, inputTag)
    self.names = %(names)s
    # !!!! Modify the names accordingly - MUST MATCH self.vals.append CALL BELOW

  def prepare(self, ROOT, ev):
    GalleryReaderBase.prepare(self, ROOT, ev)
    self.getValidHandle = ev.getValidHandle(%(rootKlass)s)

  def fill(self, ROOT, ev):
    # !!!! Check all of the below. Add conditions. Trim calls. Fill in arguments. Check return value

    validHandle = self.getValidHandle(self.inputTag)  # Get the valid handle for %(extractClass)s

    if not validHandle.empty():                       # Does it have data?

      p = validHandle.product()                       # Get the corresponding data product (maybe a vector)

      # Fill from %(fillClass)s
      %(warning)s
      %(fill)s

    return True"""


readVector = """for e in p:                             # Loop over elements and fill
        # !!!! Add a condition here?

        self.vals.append(
          [ ev.fileEntry(), ev.eventEntry(), %(fillCalls)s ])
"""

readSingle = """self.vals.append(
        [ ev.fileEntry(), ev.eventEntry(), %(fillCalls)s ])
"""

def nameForVector(n):

  ret = []
  if n in ['pos', 'position']:
    ret.extend(['x', 'y', 'z'])
  elif n  in ['p', 'momentum', 'mom']:
    ret.extend(['px', 'py', 'pz'])
  elif n in ['s', 'spin', 'pol', 'polorization']:
    ret.extend(['sx', 'sy', 'sz'])
  else:
    ret.extend(['UNKNOWNx', 'UNKNOWNy', 'UNKNOWNz'])

  return ret

def fillName(n, rt, nargs, isFunc, names, fillCalls):   # Remove constructors, destructors, etc

  parens = ''
  if isFunc:
    parens = '()'

  if rt in ['double', 'float', 'unsigned int', 'long', 'int', 'bool', 'string']:
    names.append(n)
    if nargs == 0:
      fillCalls.append( n+parens )
    else:
      fillCalls.append( n+'(<args required>)' )

  elif rt == 'CLHEP::Hep3Vector':
    names.extend( nameForVector(n) )

    if nargs == 0:
      fillCalls.extend( [ n + parens +'.'+x+'()' for x in ['x', 'y', 'z']] )
    else:
      fillCalls.extend( [ n + '(args required).'+x+'()' for x in ['x', 'y', 'z']] )

  elif rt == 'const vector<double>&':
    names.extend( nameForVector(n) )

    if nargs == 0:
      fillCalls.extend( [ n + parens + '['+x+']' for x in ['0','1','2']] )
    else:
      fillCalls.extend( [ n + '(<args required>)['+x+']' for x in ['0','1','2']] )

  else:
    names.append(n)
    fillCalls.append(n+'_UNKNOWN_RETURN_TYPE' + parens)

def fillClassNames(fillClass, klass):
  ROOT = readGallery.getROOT()
  tclass = ROOT.TClass(fillClass)

  # There must be public methods
  publicMethods = tclass.GetListOfAllPublicMethods()

  if len(publicMethods) == 0:
    return {}   # Probably bad class name

  # Loop over methods
  names = []
  fillCalls = []
  for aMethod in publicMethods:
    n = aMethod.GetName()
    rt = aMethod.GetReturnTypeNormalizedName()
    nargs = aMethod.GetNargs()

    # Remove constructor, destructor, etc
    if n == klass or n == '~'+klass or n == 'operator=':
      continue

    fillName(n, rt, nargs, True, names, fillCalls)

  # Loop over memberdata
  memberData = tclass.GetListOfAllPublicDataMembers()
  for aMD in memberData:
    n = aMD.GetName()
    rt = aMD.GetTrueTypeName()
    nargs = 0

    fillName(n, rt, 0, False, names, fillCalls)

  return {'names':names, 'fillCalls':fillCalls}


def readerClassSkel(extractClass, fillClass=None, wrapExtractVector=True, wrapFillVector=None,
                    writeFile=None):
  """Generate a skeleton Gallery Reader class for reading data from Gallery events.
     Arguments:
        extractClass = the fully qualified name of the class that is extracted from the event.
                       e.g. gm2ringsim::GeantTrackRecord or gm2truth::GhostDetectorArtRecord
                       Do *not* wrap in std::vector (instead set the vectorWrap parameter)
        fillClass = If this is the same as the extractClass (typically that's true), then don't set. If
                    you get a different class from the extracted class, then set that class here. Same
                    rules as for extractClass. The names will be pulled from this class. You will need to
                    modify the skeleton text accordingly.
        wrapExtractVector = Set to true if the extracted data is wrapped in a std::vector (typically it is).
        wrapFillVector = Set to true if the filled data is wrapped in a std::vector
        writeFile = Name of the file where to write the output. If None, then return string

        NOTE! readGallery.provide_get_valid_handle must already have been called on the class
  """
  if not fillClass:
    fillClass = extractClass

  if wrapFillVector == None:
    wrapFillVector = wrapExtractVector

  # Separate name space and class name
  ns = ''
  klass = fillClass
  if klass.find('::') >= 0:
    ns, klass = fillClass.split("::")

  # Let's determine the names for the fill class
  d = fillClassNames(fillClass, klass)
  if d == {}:
    print 'ERROR: Unknown class'
    return

  names = d['names']
  fillCalls = d['fillCalls']

  # Add fileEntry and eventEntry to names
  namesPre = ['fileEntry', 'eventEntry']
  namesPre.extend(names)
  names = namesPre

  # Make the skelName
  skelName = klass + "Reader"

  # Fill in the skeleton
  fillpart = ''
  varName = ''
  readPart = ''
  warning = ''

  if wrapFillVector:
    readPart = readVector
    varName = 'e'
  else:
    readPart = readSingle
    varName = 'p'
  if extractClass != fillClass:
    varName = 'f'
    warning = '# WARNING - YOU ARE NOT FILLING FROM THE OBJECT YOU EXTRACTED - CHANGE CODE ACCORDINGLY - note "f" below'

  fillpart = readPart % {'fillCalls': ', '.join([varName+'.' + x for x in fillCalls])}

  rootKlass = 'ROOT.' + extractClass.replace('::', '.')
  if wrapExtractVector:
    rootKlass = 'ROOT.vector(' + rootKlass + ')'

  whole = skel % {'skelName': skelName, 'names':names, 'rootKlass':rootKlass, 'fill':fillpart,
                  'warning': warning, 'extractClass':extractClass, 'fillClass':fillClass}

  if writeFile:
    open(writeFile, 'w').write(whole)
    print 'Wrote to %s' % writeFile

  return whole





