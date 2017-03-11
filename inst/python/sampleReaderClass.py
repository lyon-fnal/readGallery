class GhostDetectorArtRecordReader:
  """Reader object to read Ghost Detector Art Record objects"""

  def __init__(self, inputTag):
    self.vals = []
    self.inputTag = inputTag
    self.getValidHandle = None
    self.names = ["fileEntry", "eventEntry", "particleID", "trackID", "parentTrackID", "x", "y", "z",
                "px", "py", "pz"]

  def colnames(self):
    return self.names

  def prepare(self, ROOT, ev):
    self.vals = []  # Protect againt re-run
    self.getValidHandle = ev.getValidHandle(ROOT.vector(ROOT.gm2truth.GhostDetectorArtRecord))

  def fill(self, ROOT, ev):
    gh_cyl_h = self.getValidHandle(self.inputTag)  # Get the valid handle

    if not gh_cyl_h.empty():                       # Does it have data?

      gh_cyl = gh_cyl_h.product()                  # Get the corresponding data product vector

      for g in gh_cyl:                             # Loop over elements and fill
        if g.trackID == 1 and g.parentTrackID == 0:

          self.vals.append(
            [ev.fileEntry(), ev.eventEntry(), g.particleID, g.trackID, g.parentTrackID,
            g.position.x(), g.position.y(), g.position.z(),
            g.momentum.x(), g.momentum.y(), g.momentum.z()
            ])

    return True
