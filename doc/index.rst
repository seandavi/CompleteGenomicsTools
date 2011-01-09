.. Complete Genomics Tools documentation master file, created by
   sphinx-quickstart on Sun Jan  9 14:42:45 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Complete Genomics Tools's documentation!
===================================================

`Complete Genomics <http://completegenomics.com>`_ is a sequencing company that offers human whole-genome sequencing.  They also provide primary data analysis and generally ship a disk with data back to the customer that contains raw data as well as processed data.  While they do provide this service, they do not provide visualization of the data and do not provide multiple-sample analyses such as tumor/normal comparisons or family-based analysis.  This toolset is small and very utilitarian.

Installation
------------
The Complete Genomics Tools is meant to augment the tools already available from Complete Genomics.  In addition, the visualization pieces rely on the Circos library being installed.

This library assumes that these tools have been installed already:

* cgatools_

* Circos_ 

* annovar_

After making sure that these libraries are correctly installed, installation of Complete Genomics Tools can be done via two methods.  To install using `pip <http://pypi.python.org/pypi/pip>`_, simply:
::

   % pip install completegenomicstools

If you prefer to work with the source code, the repository is hosted on `GitHub <http://github.com/seandavi/CompleteGenomicsTools/>`_.

Calling and Annotating Somatic Variants
---------------------------------------
Given two samples, a tumor sample and an normal sample, one often wants to call and annotate somatic variants.  The Complete Genomics cgatools_ offers the calling functionality, but the variants must then be annotated.  A sample workflow looks like this:

::

   % cgatools calldiff ....
   % completegenomicstools somatic2annovar ....
   % summarize_annovar.pl ....


.. _cgatools: http://cgatools.sourceforge.net/
.. _Circos: http://mkweb.bcgsc.ca/circos/
.. _annovar: http://www.openbioinformatics.org/annovar/

Using Circos_ to Visualize Data
-------------------------------
Circos_ is a fantastic tool for visualizing genomic data.  However, setup and file formatting take a bit of work, so the cgent script includes functionality to convert junction files and CGH tracks to a format that can be used directly with Circos_.

CGH Data
^^^^^^^^



Junction Data
^^^^^^^^^^^^^
Complete Genomics provides junction files 


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

