from completegenomicstools.main import subparsers
from completegenomicstools.formats import DepthOfCoverageFile
import completegenomicstools
import itertools
import csv
import os
import glob
import subprocess
import sys

##################################################################
# prepcgh command
##################################################################
def prepcgh(args):
    tfile = DepthOfCoverageFile(args.tumorfile)
    nfile = DepthOfCoverageFile(args.normalfile)
    if(nfile.header['GENOME_REFERENCE']!=tfile.header['GENOME_REFERENCE']):
        raise Exception('Genome references not matching between tumor and normal')
    if(nfile.header['WINDOW_WIDTH']!=tfile.header['WINDOW_WIDTH']):
        raise Exception('Window widths not matching between tumor and normal')
    windowsize=int(tfile.header['WINDOW_WIDTH'])/2

    circosfile=None
    textfile=sys.stdout
    if(args.outprefix is not None):
        circosfile=open(args.outprefix+".circos",'w')
        textfile=open(args.outprefix+".txt",'w')
    for (tline,nline) in itertools.izip(tfile,nfile):
        if(args.outprefix is not None):
            circosfile.write("%s %d %d %f\n" % (tline[0].replace("chr","hs"),tline[1]-windowsize,tline[1]+windowsize,tline[5]/nline[5]))
        textfile.write("%s\t%d\t%d\t%f\n" % (tline[0],tline[1]-windowsize,tline[1]+windowsize,tline[5]/nline[5]))
    if(args.outprefix is not None):
        circosfile.close()
        textfile.close()

###
prepcgh_parser = subparsers.add_parser('prepcgh',help="Prepare CGH files from tumor/normal pairs")
prepcgh_parser.add_argument(
    "-t","--tumor-file",required=True,
    dest="tumorfile",help="The name of a depthOfCoverage file from Complete Genomics associate with a tumor")
prepcgh_parser.add_argument(
    "-n","--normal-file",required=True,
    dest="normalfile",
    help="The name of a depthOfCoverage file from Complete Genomics associated with a paired normal")
prepcgh_parser.add_argument(
    "-o","--output-prefix",
    dest="outprefix",
    help="The prefix used for output; output file will be outprefix.txt and outprefix.circos.  If not specified, output will be the text format and will go to stdout")
prepcgh_parser.set_defaults(func=prepcgh)

##################################################################
# generatemastervar command
##################################################################
def generatemastervar(args):
    varfile=glob.glob(os.path.join(args.exportroot,'ASM',"var-GS*"))
    if(len(varfile)>1):
        raise Exception('Only one file matching var-GS* should be present in the ASM directory')
    if(len(varfile)==0):
        raise Exception('No file matching var-GS* was found')        
    varfile=varfile[0]
    callargs=['cgatools','generatemastervar',
              '--beta',
              '--reference',args.reference,
              '--output',args.output,
              '--variants',varfile,
              '--repmask-data',args.repmask,
              '--export-root',args.exportroot,
              '--segdup-data',args.segdup]
    if(args.annotations is not None):
        callargs+=['--annotations',args.annotations]
    retcode=subprocess.call(callargs)
    exit(retcode)

###
gmastervar_parser = subparsers.add_parser(
    'generatemastervar',
    help="""A small wrapper around the cgatools generatemastervar command so that one does not need to specify the variant file directly.  Instead, the variant file is discovered based on the export root""")
gmastervar_parser.add_argument(
    '--reference',dest='reference',
    help="The path to the Complete Genomics reference file.  The file typically ends in .crr",
    required=True)                         
gmastervar_parser.add_argument(
    '--repmask-data',dest='repmask',
    help="The path to the repeat mask file",
    required=True)
gmastervar_parser.add_argument(
    '--segdup-data',dest='segdup',
    help="The path to the segmental duplication file",
    required=True)
gmastervar_parser.add_argument(
    '--export-root',dest='exportroot',
    help="The export root for the sample.  This directory is the directory containing the ASM directory",
    required=True)
gmastervar_parser.add_argument(
    '--output',dest="output",
    help="The output file name",
    required=True)
gmastervar_parser.add_argument(
    '--annotations',dest='annotations',
    help="comma-separated list of annotations to add to each row of the mastervar file.  See the cgatools documentation for more details or type 'cgatools generatemastervar --help' at the command line.  The default is as used by cgatools.")
gmastervar_parser.set_defaults(func=generatemastervar)

##################################################################
# junc2circos command
##################################################################
def junc2circos(args):
    f = csv.reader(open(args.junctionfile,'r'),delimiter="\t")
    line = f.next()
    while(len(line)==2):
        line=f.next()
    f.next()
    for line in f:
        print "%s %s %d %d\n%s %s %d %d" % (line[0],line[1].replace('chr','hs'),
                                                  int(line[2]),int(line[2])+int(line[4]),
                                                  line[0],line[5].replace('chr','hs'),
                                                  int(line[6]),int(line[6])+int(line[8]))


junc2circos_parser=subparsers.add_parser(
    'junc2circos',
    help='Convert a Complete Genomics junction file to circos format')
junc2circos_parser.add_argument(
    "junctionfile",
    help="Name of a complete genomics junction file (or junctiondiff file)")
junc2circos_parser.set_defaults(func=junc2circos)



##################################################################
# somatic2annovar command
##################################################################
def somatic2annovar(args):
    """
    :param fname: Filename of the somatic call file as generated by a call to cgatools calldiff
    :type fname: string
    """

    fname=args.SomaticOutput
    csvfile = csv.DictReader(open(fname,'r'),delimiter="\t")
    for row in csvfile:
        row['begin']=str(int(row['begin'])+1)
        if(row['reference']==""): 
            row['reference']="-"
            row['end']=str(int(row['end'])+1)
        if(row['alleleSeq']==""): row['alleleSeq']="-"
        print "\t".join([row['chromosome'],row['begin'],
                         row['end'],row['reference'],
                         row['alleleSeq'],row['varType'],row['LocusClassification'],
                         row['SomaticCategory'],row['SomaticScore']])

###
s2a_parser = subparsers.add_parser('somatic2annovar',help='Convert SomaticOutput.tsv file to annovar input format')
s2a_parser.add_argument("SomaticOutput",help="filename of a Complete Genomics SomaticOutput.tsv file, the result of running cgatools calldiff")
s2a_parser.set_defaults(func=somatic2annovar)


##################################################################
# genotypes2snpdiff command
##################################################################
def genotypes2snpdiff(args):
    # assumes pileup format input for now
    pfile = completegenomicstools.formats.PileupFile(args.genfile)
    outfile=sys.stdout
    if(args.outfile is not None):
        outfile=open(args.outfile)
    outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" %
                  ("Chromosome",
                   "Offset0Based",
                   "GenotypesStrand",
                   "Genotypes",
                   "GenQuality",
                   "VarQuality",
                   "RMSmapping",
                   "Coverage",
                   "Bases",
                   "Qualities"))
    for p in pfile:
        if(p.coverage>=args.mindepth):
            outfile.write("%s\t%d\t+\t%s%s\t%d\t%d\t%d\t%d\t%s\t%s\n" %
                          (p.chromosome,
                           p.position,
                           p.genotypes[0],
                           p.genotypes[1],
                           p.qual,
                           p.varqual,
                           p.rmsmapping,
                           p.coverage,
                           p.bases,
                           p.qualities))
    if(args.outfile is not None):
        outfile.close()

gen2snpdiff_parser = subparsers.add_parser(
    'genotypes2snpdiff',
    help="Convert a genotype file such a pileup file (the only format currently supported) to a snpdiff input file")
gen2snpdiff_parser.add_argument(
    "-o","--output",dest="outfile",
    help="name of output file, uses stdout as default")
gen2snpdiff_parser.add_argument(
    "-d","--min-depth",default=6,dest="mindepth",
    help="Minimum depth of coverage to be included")
gen2snpdiff_parser.add_argument(
    "genfile",
    help="Genotype filename currently only the pileup format is supported")
gen2snpdiff_parser.set_defaults(func=genotypes2snpdiff)

##################################################################
# testvariant2annovar command
##################################################################
def testvariant2annovar(args):
    f = csv.reader(open(args.testvariantoutfile,'r'),delimiter="\t")
    headers=f.next()
    nsamples=len(headers)-8
    set1=set(xrange(nsamples))
    settypes=['00','01','11','0N','1N','NN','0','1','N']
    print("\t".join(headers[1:3]+headers[5:7]+headers[8:]+settypes))
    for row in f:
        set1genotypes={'00':0,
                       '01':0,
                       '11':0,
                       '0N':0,
                       '1N':0,
                       'NN':0,
                       '0':0,
                       '1':0,
                       'N':0}
        for genotype in row[8:]:
            set1genotypes[genotype]+=1
        beginval=int(row[2])+1
        if(row[5]==""):
            row[5]='-'
            beginval=int(row[2])
        if(row[6]==""):
            row[6]='-'
            beginval=int(row[2])
        output="%s\t%d\t%s\t%s\t%s\t%s\t" % (row[1],
                                             beginval,
                                             row[3],
                                             row[5],
                                             row[6],
                                             "\t".join(row[8:]))
        output+="\t".join([str(set1genotypes[x]) for x in settypes])
        print(output)
                                         
        

tv2a_parser = subparsers.add_parser(
    'testvariant2annovar',
    help="Takes the output of cgatools testvariant command, optionally a grouping parameter, and outputs the 'summarized', annovar-ready format file"
    )
tv2a_parser.add_argument(
    "testvariantoutfile",
    help="The name of the cgatools testvariant output file")
#tv2a_parser.add_argument(
#    '-g','--group',dest="group",
#    help="If not specified, summarization of genotypes will be done with all samples together.  If specified as a comma-separated list of integers representing the columns in the testvariant output file, then the columns in this group will form one of two groups that will be summarized separately.  This can be useful when there are, for example, affected and unaffected individuals that should be treated differently.")
tv2a_parser.set_defaults(func=testvariant2annovar)
                         


from mako.template import Template
def cancer2circos(args):
    s = """

<colors>
<<include etc/colors.conf>>
</colors>

<fonts>
<<include etc/fonts.conf>>
</fonts>

<<include ideogram.conf>>
<<include ticks.conf>>

karyotype   = data/karyotype.human.txt

<image>
dir = ./
file  = circos-cancer.png
#file = circos-example.svg
# radius of inscribed circle in image
radius         = 2000p
background     = white
# by default angle=0 is at 3 o'clock position
angle_offset   = -90
24bit             = yes
auto_alpha_colors = yes
auto_alpha_steps  = 5
</image>

chromosomes_units = 1000000
#chromosomes       = hs11
chromosomes_display_default = yes

# chromosomes_radius = hs2:0.9r;hs3:0.8r

# Links (bezier curves or straight lines) are defined in <links> blocks.
# Each link data set is defined within a <link>.
# As with highlights, parameters defined
# in the root of <links> affect all data sets and are considered
# global settings. Individual parameters value can be refined by
# values defined within <link> blocks, or additionally on each
# data line within the input file.

<links>

z      = 0
radius = 0.725r
bezier_radius = 0.3r

<link diff>
show         = yes
color        = red_a3
thickness    = 5
file         = ${difflink}
#record_limit = 1000
</link>
</links>

<plots>
<plot>

show  = yes
type  = scatter
file  = ${cnfile}
fill_color = lblue
stroke_color     = blue
stroke_thickness = 1
glyph = circle
glyph_size = 6
min   = 0.2
max   = 3
r0    = 0.75r
r1    = 0.975r

background       = yes
background_color = vlgrey
#background_stroke_color = black
#background_stroke_thickness = 1

axis           = yes
axis_color     = lgrey
axis_thickness = 2
axis_spacing   = 0.001

<rules>

<rule>
importance   = 100
condition    = _VALUE_ > 1.2
stroke_color = dgreen
fill_color   = green
#glyph        = rectangle
</rule>

<rule>
importance   = 85
condition    = _VALUE_ < 0.8
stroke_color = dred
fill_color   = red
#glyph        = triangle
</rule>

</rules>


</plot>
</plots>

anglestep       = 0.5
minslicestep    = 10
beziersamples   = 40
debug           = no
warnings        = no
imagemap        = no

# don't touch!
units_ok        = bupr
units_nounit    = n
"""

    outfile=sys.stdout
    if(args.outfile is not None):
        outfile=open(args.outfile,'w')
    outfile.write(Template(s).render(cnfile=args.copynumberfile,difflink=args.linkfile))
    outfile.write('\n')
    outfile.close()
                  

cancer2circos_parser = subparsers.add_parser(
    'cancer2circos',
    help='After converting junction files (using cgent junc2circos) and circos-format copy number difference files (using cgent prepcgh), use this command to generate an input file for circos.  NOTE: This command is meant to be a quick way of getting a plot.  Circos is VERY flexible and this command cannot capitalize on that flexibility.  Using circos independently is recommended.')

cancer2circos_parser.add_argument(
    "linkfile",
    help="The link file, typically generated with cgent junc2circos")
cancer2circos_parser.add_argument(
    "copynumberfile",
    help="The copynumber file as generated by cgent prepcgh")
cancer2circos_parser.add_argument(
    '-o','--outfile',dest="outfile",
    help="The file to which the circos input file will be written")

cancer2circos_parser.set_defaults(func=cancer2circos)
