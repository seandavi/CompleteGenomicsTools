from completegenomicstools.main import subparsers
from completegenomicstools.formats import DepthOfCoverageFile
import itertools

def prepcgh(args):
    tfile = DepthOfCoverageFile(args.tumorfile)
    nfile = DepthOfCoverageFile(args.normalfile)
    if(nfile.header['GENOME_REFERENCE']!=tfile.header['GENOME_REFERENCE']):
        raise Exception('Genome references not matching')
    windowsize=int(tfile.header['WINDOW_WIDTH'])/2
    for (tline,nline) in itertools.izip(tfile,nfile):
        print "%s\t%d\t%d\t%f" % (tline[0],tline[1]-windowsize,tline[1]+windowsize,tline[5]/nline[5])

prepcgh_parser = subparsers.add_parser('prepcgh',help="Prepare CGH files from tumor/normal pairs")
prepcgh_parser.add_argument("-t","--tumor-file",required=True,
                            dest="tumorfile",help="The name of a depthOfCoverage file from Complete Genomics associate with a tumor")
prepcgh_parser.add_argument("-n","--normal-file",required=True,
                            dest="normalfile",help="The name of a depthOfCoverage file from Complete Genomics associated with a paired normal")
prepcgh_parser.set_defaults(func=prepcgh)

