#!/usr/bin/env python3

from igwn_ligolw import utils as ligolw_utils

while 1:
    ligolw_utils.load_filename("ligo_lw_test_01.xml", verbose=True).unlink()
