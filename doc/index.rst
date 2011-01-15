.. Complete Genomics Tools documentation master file, created by
   sphinx-quickstart on Sun Jan  9 14:42:45 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :hidden:

   cgatools

.. index:: somatic2annovar, cgatools, annovar, summarize_annovar.pl, SomaticScore, Circos

Welcome to Complete Genomics Tools's documentation!
===================================================

`Complete Genomics <http://completegenomics.com>`_ is a sequencing company that offers human whole-genome sequencing.  They also provide primary data analysis and generally ship a disk with data back to the customer that contains raw data as well as processed data.  While they do provide this service, they do not provide visualization of the data and do not provide multiple-sample analyses such as tumor/normal comparisons or family-based analysis.  This toolset is small and very utilitarian and meant to fill in gaps in what is offered by Complete Genomics.

Installation
------------
The Complete Genomics Tools is meant to augment the tools already available from Complete Genomics.  In addition, the visualization pieces rely on the Circos_ library being installed.

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

   % cgatools calldiff --reference=/data/sedavis/public/CG/build37.crr \
       --variantsA=/data/sedavis/sequencing/beppe/CGI/GS000002674-DID/GS000001738-ASM/GS00359-DNA_F01/ASM/var-GS000001738-ASM.tsv.bz2 \
       --variantsB=/data/sedavis/sequencing/beppe/CGI/GS000002675-DID/GS000001739-ASM/GS00359-DNA_G01/ASM/var-GS000001739-ASM.tsv.bz2 \
       --reports=SuperlocusOutput,SuperlocusStats,LocusOutput,LocusStats,VariantOutput,SomaticOutput \
       --export-rootA=/data/sedavis/sequencing/beppe/CGI/GS000002674-DID/GS000001738-ASM/GS00359-DNA_F01 \
       --export-rootB=/data/sedavis/sequencing/beppe/CGI/GS000002675-DID/GS000001739-ASM/GS00359-DNA_G01 \
       --beta

The :program:`calldiff` command takes as input two variant files and two matching "export roots".  The variant files have the name "var-..." and normally live in the export-root/ASM directory.  File A above is the tumor while file B represents the normal sample.  The export root is the directory directly above the ASM directory.

::

   % cgent somatic2annovar SomaticOutput.tsv > somatic.annovar.input

The :program:`somatic2annovar` command simply transforms the calldiff-generated SomaticOutput.tsv file into the appropriate input format for annovar.

::

   % summarize_annovar.pl --buildver=hg19 somatic.annovar.input /data/sedavis/public/annovar/hg19/

The :program:`summarize_annovar.pl` script simply runs a standard set of annovar scripts and combines the output into a single text file suitable for filtering in Excel, for example.  The final output, then, of these steps will be a tab-delimited text file containing the variants that are in the tumor but not in the normal.  The last column, the SomaticScore, is a value between 0 and 1, with higher numbers being more likely to be true somatic variants.  However, even numbers as low as 0.1 (or lower) still show a fairly high sensitivity and specificity.  See the cgatools documentation for more details on the calculation and interpretation of the SomaticScore.

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
Complete Genomics provides junction files separately for tumor and normal.  A first step is to "subtract" the junctions in the normal from the tumor:

::
   
   % cgatools junctiondiff ....

The command above will generate a junctiondiff file that contains junctions that appear to be present in the tumor but not the normal.  In order to use the junctiondiff output:

   % cgent junc2circos ....

The cgent junc2circos command will then convert the junctiondiff file into a "link" file to be used by Circos.  The actual construction of the circos plot still needs to be done by hand at this time.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

