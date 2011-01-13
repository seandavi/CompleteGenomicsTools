import csv
import pdb

class DepthOfCoverageFile:
    """
    This class encapsulates a depthOfCoverage file from Complete genomics.  The files are
    of the format:

    ::

    #ASSEMBLY_ID    GS000001739-ASM
    #SOFTWARE_VERSION       1.10.0.22
    #GENERATED_BY   ExportWorkflow&ReportEngine
    #GENERATED_AT   2010-11-23 04:28:20.661551
    #FORMAT_VERSION 1.5
    #GENOME_REFERENCE       NCBI build 37
    #SAMPLE GS00359-DNA_G01
    #TYPE   DEPTH-OF-COVERAGE
    #WINDOW_SHIFT   100000
    #WINDOW_WIDTH   100000
    
    >chromosome     position        uniqueSequenceCoverage  weightSumSequenceCoverage       gcCorrectedCvg  avgNormalizedCoverage
    chr1    60000   6.788   68.392  71.216  61.1
    chr1    367719  0.076   37.931  41.632  58.6
    chr1    571368  13.994  181.219 164.797 58.0
    chr1    671368  5.019   50.891  50.253  58.4
    chr1    771368  46.721  82.199  80.000  63.3
    chr1    871368  59.413  64.112  69.093  58.3
    chr1    971368  41.707  44.378  56.517  60.8

    The class works as an iterator but also contains the header information.

    >>> import completegenomicstools.formats as f
    >>> x = f.DepthOfCoverageFile('fname')
    >>> x.header
    >>> x.header['GENOME_REFERENCE']
    >>> for line in x:
        print x

    
    """
    def __init__(self,fname):
        self.fh=csv.reader(open(fname,'r'),delimiter="\t")
        self.header={}
        self._readheader()
        self.colnames=self.fh.next()

    def _readheader(self):
        line=self.fh.next()
        while(len(line)==2):
            self.header[(line[0].replace("#",""))]=line[1]
            line=self.fh.next()
        return

    def _iter(self):
        for i in self.fh:
            yield i

    def __iter__(self):
        return(self)

    def next(self):
        tmp=self._iter().next()
        return(tuple([tmp[0],int(tmp[1]),
                     float(tmp[2]),
                     float(tmp[3]),
                     float(tmp[4]),
                     float(tmp[5])]))

    
        
