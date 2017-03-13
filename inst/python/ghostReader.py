from readGallery import GalleryReaderBase  # Necessary for the base class

class GhostDetectorArtRecordReader(GalleryReaderBase):
  def __init__(self, inputTag):
    GalleryReaderBase.__init__(self, inputTag)
    self.names = ['fileEntry', 'eventEntry', 'particleID', 'trackID', 'parentTrackID',
                   'x', 'y', 'z', 'px', 'py', 'pz']

  def prepare(self, ROOT, ev):
    GalleryReaderBase.prepare(self, ROOT, ev)
    self.getValidHandle = ev.getValidHandle(ROOT.vector(ROOT.gm2truth.GhostDetectorArtRecord))

  def fill(self, ROOT, ev):
    # We don't need to call super.fill here

    gh_cyl_h = self.getValidHandle(self.inputTag)  # Get the valid handle

    if not gh_cyl_h.empty():                       # Does it have data?

      gh_cyl = gh_cyl_h.product()                  # Get the corresponding data product vector

      for g in gh_cyl:                             # Loop over elements and fill
        if g.trackID == 1 and g.parentTrackID == 0:

          self.vals.append(
               [ev.fileEntry(), ev.eventEntry(), g.particleID, g.trackID, g.parentTrackID,
                g.position.x(), g.position.y(), g.position.z(),
                g.momentum.x(), g.momentum.y(), g.momentum.z() ]
          )

    return True
