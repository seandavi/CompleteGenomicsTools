import csv
import pdb
import collections

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


class SimpleGenotype(tuple):
    """
    Store a genotype as a simple pair of alleles.
    """
    def __init__(self,alleles):
        if(len(alleles)!=2):
            raise(Exception("need two alleles"))
        super(SimpleGenotype,self).__init__(alleles)

    def __str__(self):
        return("%s;%s" % (self))


class SuperlocusVariantRecord:
    """
    Encapsulates a single row of a SuperlocusVariantRecord

    The attributes look like this:
    
    def __init__(self,row):
        self.superLocusId=int(row[0])
        self.chromosome=row[1]
        self.start=int(row[2])
        self.end=int(row[3])
        self.alleleClasses=row[4].split(';')
        self.refAllele=row[5]
        self.tumorAlleles=SimpleGenotype(row[6].split(";"))
        self.normalAlleles=SimpleGenotype(row[7].split(";"))
    """
    def __init__(self,row):
        self.superLocusId=int(row[0])
        self.chromosome=row[1]
        self.start=int(row[2])
        self.end=int(row[3])
        self.alleleClasses=row[4].split(';')
        self.refAllele=row[5]
        self.tumorAlleles=SimpleGenotype(row[6].split(";"))
        self.normalAlleles=SimpleGenotype(row[7].split(";"))
        
    def __str__(self):
        return("%d\t%s\t%d\t%d\t%s;%s\t%s\t%s\t%s" % (self.superLocusId,
                                                      self.chromosome,
                                                      self.start,
                                                      self.end,
                                                      self.alleleClasses[0],
                                                      self.alleleClasses[1],
                                                      self.refAllele,
                                                      str(self.tumorAlleles),
                                                      str(self.normalAlleles)))
    
class SuperlocusVariantFile:
    """
    This class encapsulates the so-called SuperlocusOutput.tsv file generated
    by running cgatools calldiff.  An example looks like this:

    SuperlocusId    Chromosome      Begin   End     Classification  Reference       AllelesA        AllelesB
    1       chr1    41980   41981   alt-identical;alt-identical     A       G;G     G;G
    2       chr1    55925   55926   alt-consistent;alt-consistent   T       ?;?     C;C
    3       chr1    57951   57952   alt-identical;alt-identical     A       C;C     C;C
    4       chr1    58210   58211   alt-identical;alt-identical     A       G;G     G;G
    5       chr1    59039   59040   ref-identical;alt-consistent    T       T;N     T;C
    6       chr1    61986   61989   ref-consistent;alt-consistent   AAG     ?;?     AAG;GAC
    7       chr1    68893   68896   ref-consistent;alt-consistent   TAG     ?;TAA   ?;?
    8       chr1    69452   69453   ref-consistent;alt-consistent   G       ?;?     G;A
    9       chr1    69510   69511   alt-identical;alt-identical     A       G;G     G;G
    10      chr1    69551   69552   ref-consistent;alt-consistent   G       G;C     ?;?
    11      chr1    82733   82734   alt-identical;ref-consistent    T       C;N     C;T
    12      chr1    87189   87190   ref-consistent;alt-consistent   G       G;A     ?;?
    107     chr1    737909  737910  ref-identical;onlyA     G       G;A     G;G
    350     chr1    909308  909309  alt-identical;onlyB     T       C;T     C;C
    567     chr1    997442  997468  ref-identical;onlyA     CCTTGTCCCCGTTCCCTCCGTCCCTC      CCTTGTCCCCGTTCCCTCCGTCCCTC;     CCTTGTCCCCGTTCCCTCCGTCCCTC;?CCCGTTCCCTCCGTCCCTC
    923     chr1    1453631 1453633 ref-identical;onlyA     CA      CA;     CA;CA
    1072    chr1    1584626 1584632 ref-consistent;onlyB    CACCCG  CA?;CA? CACCCG;TGCCCA
    1101    chr1    1594200 1594200 alt-identical;onlyA             T;T     T;
    1102    chr1    1594209 1594210 ref-identical;onlyB     C       C;C     C;T
    1103    chr1    1594220 1594221 ref-identical;onlyB     C       C;C     C;A
    """

    def __init__(self,fname):
        self.fh=csv.reader(open(fname,'r'),delimiter="\t")
        self.colnames=self.fh.next()

    def _iter(self):
        for i in self.fh:
            yield i

    def __iter__(self):
        return(self)

    def next(self):
        row=self._iter().next()
        return(SuperlocusVariantRecord(row))

class PileupRecord:
    convertdict={'A':('A','A'),
                 'G':('G','G'),
                 'C':('C','C'),
                 'T':('T','T'),
                 'M':('A','C'),
                 'R':('A','G'),
                 'W':('A','T'),
                 'S':('C','G'),
                 'Y':('C','T'),
                 'K':('G','T'),
                 'N':('N','N')}
    
    def __init__(self,row):
        """
        Takes a row of a pileup file and generates a pileup record.  Note
        that the pileup record here only deals with SNVs and not indels

        Accessors include:

        chromosome
        position
        reference
        genotypes (a tuple of length 2)
        qual
        varqual
        rmsmapping
        coverage
        bases
        qualities
        """
        self.chromosome=row[0]
        self.position=int(row[1])-1
        self.reference=row[2].upper()
        if(len(row[3])>1):
            self.genotypes=('.','.')
        else:
            self.genotypes=self.convertdict[row[3].upper()]
        self.qual=int(row[4])
        self.varqual=int(row[5])
        self.rmsmapping=int(row[6])
        self.coverage=int(row[7])
        self.bases=row[8]
        self.qualities=row[9]

    def isVariant(self):
        if((self.genotypes[0]==self.reference) & (self.genotypes[1]==self.reference)):
            return(False)
        return(True)

    def isHeterozygous(self):
        return(self.genotypes[0]!=self.genotypes[1])

    def __str__(self):
        return("%s\t%d\t%s/%s" % (self.chromosome,
                                  self.position,
                                  self.genotypes[0],
                                  self.genotypes[1]))

class PileupFile:
    buffer=collections.deque()
    
    def __init__(self,fname):
        self.fh=open(fname,'r')
        self._getNextBlock()

    def _getNextBlock(self):
        row = self._iter().next()
        # if indel, must deal with it
        if(row[2]=="*"):
            tmpgenotype=row[3].split("/")
            if(tmpgenotype[0]==tmpgenotype[1]):
                # the following case means that an indel was not called
                if(tmpgenotype[0]=="*"):
                    self._getNextBlock() # go get more lines
                    return
                # a deletion was found on both strands
                if(tmpgenotype[1].startswith('-')):
                    numberofdels=len(tmpgenotype[1])
                    while(numberofdels>1):
                        row=self._iter().next()
                        tmprecord=PileupRecord(row)
                        tmprecord.genotypes=("-","-")
                        self.buffer.append(tmprecord)
                        numberofdels-=1
                    return
                # Just skip insertions
                if(tmpgenotype[1].startswith("+")):
                    self._getNextBlock()
                    return
            # still working with indel, but now not the same on both strands
            else:
                # could be first allele
                if(tmpgenotype[0].startswith('-') ):
                    numberofdels=len(tmpgenotype[0])
                    while(numberofdels>1):
                        row=self._iter().next()
                        tmprecord=PileupRecord(row)
                        tmprecord.genotypes=(tmprecord.genotypes[0],"-")
                        self.buffer.append(tmprecord)
                        numberofdels-=1
                    return
                # or second allele
                if(tmpgenotype[1].startswith('-') ):
                    numberofdels=len(tmpgenotype[1])
                    while(numberofdels>1):
                        row=self._iter().next()
                        tmprecord=PileupRecord(row)
                        tmprecord.genotypes=(tmprecord.genotypes[0],"-")
                        self.buffer.append(tmprecord)
                        numberofdels-=1
                    return
                # just skip insertions
                if((tmpgenotype[0].startswith("+")) | (tmpgenotype[1].startswith("+"))):
                    self._getNextBlock()
                    return
        else:
            self.buffer.append(PileupRecord(row))

    def _iter(self):    
        for i in self.fh:
            yield i.strip().split("\t")

    def __iter__(self):
        return(self)

    def next(self):
        try:
            return(self.buffer.popleft())
        except IndexError:
            self._getNextBlock()
            try:
                return(self.buffer.popleft())
            except IndexError:
                raise StopIteration
