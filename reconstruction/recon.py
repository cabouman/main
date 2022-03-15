# Copyright 2020, General Electric Company. All rights reserved. See https://github.com/xcist/code/blob/master/LICENSE

from catsim.CommonTools import *

# Need to import all the recons that can be specified by cfg.recon.recontype
from reconstruction.fdk_equiAngle import fdk_equiAngle


def recon(cfg):

    prep = load_prep(cfg)

    img = fdk_equiAngle(cfg, prep)
    # img = feval('reconstruction.' + cfg.recon.reconType, cfg, prep)

    save_raw(cfg, img)

     
def load_prep(cfg):

    prep = rawread(cfg.resultsName + '.prep',
                  [cfg.protocol.viewCount, cfg.scanner.detectorRowCount, cfg.scanner.detectorColCount],
                  'float')
                  
    return prep


def save_raw(cfg, matrix):

    if cfg.recon.unit =='hu':
        matrix = matrix*(1000/(cfg.recon.mu))
        matrix = matrix + cfg.recon.huOffset
    elif cfg.recon.unit == '/mm':
        matrix = matrix
    elif cfg.recon.unit == '/cm':
        matrix = matrix*10

    matrix_size_string = str(cfg.recon.imageSize) + 'x' + str(cfg.recon.imageSize) + 'x' + str(cfg.recon.sliceCount)
    fname = cfg.resultsName + '.recon_' + matrix_size_string + '.raw'
    # rawwrite(fname, matrix)
    matrix.tofile(fname)