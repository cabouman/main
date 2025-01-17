# Copyright 2020, General Electric Company. All rights reserved. See https://github.com/xcist/code/blob/master/LICENSE

'''
Write view data to file (binary).
Mingye Wu, GE Research

'''
def WriteRawViewChunk(cfg, viewId):
    # access mode
    if viewId == cfg.sim.startViewId:
        accessMode = 'wb'
        cfg.dump_views = b''
    elif (viewId-cfg.sim.startViewId)%cfg.physics.dump_period==0 or viewId == cfg.sim.stopViewId:
        accessMode = 'ab'
    else:
        accessMode = None

    # filename
    scanTypeInd = [cfg.sim.isAirScan, cfg.sim.isOffsetScan, cfg.sim.isPhantomScan].index(1)
    extName = ['.air', '.offset', '.scan'][scanTypeInd]
    fname = cfg.resultsName + extName
    
    # Change the dim from row->col to col->row
    dims = [cfg.scanner.detectorColCount, cfg.scanner.detectorRowCount]
    thisView = cfg.thisView.reshape(dims).T.ravel()
    cfg.dump_views += thisView.tobytes()
    
    # write or append raw data
    if accessMode is None: return cfg

    with open(fname, accessMode) as f:
        f.write(cfg.dump_views)
    cfg.dump_views = b''
    
    return cfg
