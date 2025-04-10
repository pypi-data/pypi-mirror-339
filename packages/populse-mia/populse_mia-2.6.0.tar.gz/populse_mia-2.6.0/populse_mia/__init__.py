# -*- coding: utf-8 -*-
"""
MIA is shorthand for “Multiparametric Image Analysis”. It is intended to be
a complete image processing environment mainly targeted at the analysis and
visualization of large amounts of MRI data.

MRI data analysis often requires a complex succession of data processing
pipelines applied to a set of data acquired in an MRI exam or over several
MRI exams. This analysis may need to be repeated a large number of times in
studies involving a large number of acquisition sessions. Such that manual
execution of the processing modules or simple ad-hoc scripting of the
process may become error-prone, cumbersome and difficult to reproduce. Data
processing pipelines exist in separate heterogeneous toolboxes, developed
in-house or by other researchers in the field. This heterogeneity adds to
the complexity of the modules are to be invoked manually.

MIA (populse_mia) aims to provide easy tools to perform complex data processing
based on a definition of the inputs and outputs of the individual pipelines
on a conceptual level, and implies identifying data with respect to their
role in an analysis project: “the scan type”, “the subject being scanned”,
“the group of this subject is part of”, etc.


:Contains:
    :Packages:
      - data_manager: handles the projects and their database
      - sources_images: a collection of images used in Mia
      - user_interface: mainly intended for the graphic interface of Mia
      - utils: various utilities for the Mia operation

    :Modules:
      - info.py: define software version, description and requirements
      - main.py: the first module used at the runtime of mia
      - __main__.py: make populse_mia accessible as a module
      - software_properties.py: handles the configuration of the software
      - test.py: unitary tests

"""

###############################################################################
# Populse_mia - Copyright (C) IRMaGe/CEA, 2018
# Distributed under the terms of the CeCILL license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html
# for details.
###############################################################################

from .info import __version__  # noqa: F401

# import importlib.metadata

# try:
#    __version__ = importlib.metadata.__version__ = importlib.metadata.version(
#        "populse_mia"
#    )

# except importlib.metadata.PackageNotFoundError:
#    __version__ = None
