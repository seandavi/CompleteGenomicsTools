snpdiff
-----------------------------------

::

    COMMAND NAME
        snpdiff - Compares snp calls to a Complete Genomics variant file.
    
    DESCRIPTION
        Compares the snp calls in the "genotypes" file to the calls in a Complete 
        Genomics variant file. The genotypes file is a tab-delimited file with at 
        least the following columns (additional columns may be given):
        
            Chromosome      (Required) The name of the chromosome.
            Offset0Based    (Required) The 0-based offset in the chromosome.
            GenotypesStrand (Optional) The strand of the calls in the Genotypes 
                            column (+ or -, defaults to +).
            Genotypes       (Optional) The calls, one per allele. The following 
                            calls are recognized:
                            A,C,G,T A called base.
                            N       A no-call.
                            -       A deleted base.
                            .       A non-snp variation.
        
        The output is a tab-delimited file consisting of the columns of the 
        original genotypes file, plus the following additional columns:
        
            Reference         The reference base at the given position.
            VariantFile       The calls made by the variant file, one per allele. 
                              The character codes are the same as is described for 
                              the Genotypes column.
            DiscordantAlleles (Only if Genotypes is present) The number of 
                              Genotypes alleles that are discordant with calls in 
                              the VariantFile. If the VariantFile is described as 
                              haploid at the given position but the Genotypes is 
                              diploid, then each genotype allele is compared 
                              against the haploid call of the VariantFile.
            NoCallAlleles     (Only if Genotypes is present) The number of 
                              Genotypes alleles that were no-called by the 
                              VariantFile. If the VariantFile is described as 
                              haploid at the given position but the Genotypes is 
                              diploid, then a VariantFile no-call is counted twice.
        
        The verbose output is a tab-delimited file consisting of the columns of the
        original genotypes file, plus the following additional columns:
        
            Reference   The reference base at the given position.
            VariantFile The call made by the variant file for one allele (there is 
                        a line in this file for each allele). The character codes 
                        are the same as is described for the Genotypes column.
            [CALLS]     The rest of the columns are pasted in from the VariantFile,
                        describing the variant file line used to make the call.
        
        The stats output is a comma-separated file with several tables describing 
        the results of the snp comparison, for each diploid genotype. The tables 
        all describe the comparison result (column headers) versus the genotype 
        classification (row labels) in different ways. The "Locus classification" 
        tables have the most detailed match classifications, while the "Locus 
        concordance" tables roll these match classifications up into "discordance" 
        and "no-call". A locus is considered discordant if it is discordant for 
        either allele. A locus is considered no-call if it is concordant for both 
        alleles but has a no-call on either allele. The "Allele concordance" 
        describes the comparison result on a per-allele basis.
    
    OPTIONS
      -h [ --help ] 
            Print this help message.
    
      --reference arg
            The input crr file.
    
      --variants arg
            The input variant file.
    
      --genotypes arg
            The input genotypes file.
    
      --output-prefix arg
            The path prefix for all output reports.
    
      --reports arg (=Output,Verbose,Stats)
            Comma-separated list of reports to generate. A report is one of:
                Output  The output genotypes file.
                Verbose The verbose output file.
                Stats   The stats output file.
            
    
    
    SUPPORTED FORMAT_VERSION
        0.3 or later
    
calldiff
-----------------------------------

::

    COMMAND NAME
        calldiff - Compares two Complete Genomics variant files.
    
    DESCRIPTION
        Compares two Complete Genomics variant files. Divides the genome up into 
        superloci of nearby variants, then compares the superloci. Also refines the
        comparison to determine per-call or per-locus comparison results.
        
        Comparison results are usually described by a semi-colon separated string, 
        one per allele. Each allele's comparison result is one of the following 
        classifications:
        
            ref-identical   The alleles of the two variant files are identical, and
                            they are consistent with the reference.
            alt-identical   The alleles of the two variant files are identical, and
                            they are inconsistent with the reference.
            ref-consistent  The alleles of the two variant files are consistent, 
                            and they are consistent with the reference.
            alt-consistent  The alleles of the two variant files are consistent, 
                            and they are inconsistent with the reference.
            onlyA           The alleles of the two variant files are inconsistent, 
                            and only file A is inconsistent with the reference.
            onlyB           The alleles of the two variant files are inconsistent, 
                            and only file B is inconsistent with the reference.
            mismatch        The alleles of the two variant files are inconsistent, 
                            and they are both inconsistent with the reference.
            phase-mismatch  The two variant files would be consistent if the 
                            hapLink field had been empty, but they are 
                            inconsistent.
            ploidy-mismatch The superlocus did not have uniform ploidy.
        
        In some contexts, this classification is rolled up into a simplified 
        classification, which is one of "identical", "consistent", "onlyA", 
        "onlyB", or "mismatch".
        
        A good place to start looking at the results is the superlocus-output file.
        It has columns defined as follows:
        
            SuperlocusId   An identifier given to the superlocus.
            Chromosome     The name of the chromosome.
            Begin          The 0-based offset of the start of the superlocus.
            End            The 0-based offset of the base one past the end of the 
                           superlocus.
            Classification The match classification of the superlocus.
            Reference      The reference sequence.
            AllelesA       A semicolon-separated list of the alleles (one per 
                           haplotype) for variant file A, for the phasing with the 
                           best comparison result.
            AllelesB       A semicolon-separated list of the alleles (one per 
                           haplotype) for variant file B, for the phasing with the 
                           best comparison result.
        
        The locus-output file contains, for each locus in file A and file B that is
        not consistent with the reference, an annotated set of calls for the locus.
        The calls are annotated with the following columns:
        
            SuperlocusId            The id of the superlocus containing the locus.
            File                    The variant file (A or B).
            LocusClassification     The locus classification is determined by the 
                                    varType column of the call that is inconsistent
                                    with the reference, concatenated with a 
                                    modifier that describes whether the locus is 
                                    heterozygous, homozygous, or contains no-calls.
                                    If there is no one variant in the locus (i.e., 
                                    it is heterozygous alt-alt), the locus 
                                    classification begins with "other".
            LocusDiffClassification The match classification for the locus. This is
                                    defined to be the best of the comparison of the
                                    locus to the same region in the other file, or 
                                    the comparison of the superlocus.
        
        The somatic output file contains a list of putative somatic variations of 
        genome A. The output includes only those loci that can be classified as 
        snp, del, ins or sub in file A, and are called reference in the file B. 
        Every locus is annotated with the following columns:
        
            VarScoreA               The alternative score of the variation in 
                                    genome A; this is the reference score for SNPs,
                                    and the evidence score for other variations.
            RefScoreB               Minimum of the reference scores of the locus in
                                    genome B.
            SomaticCategory         The category used for determining the 
                                    VarScoreARank and the RefScoreBRank.
            VarScoreARank           The fraction of all called mutations in genome 
                                    A whose VarScoreA is less than VarScoreA for 
                                    this mutation.
            RefScoreBRank           The fraction of locations that are called 
                                    reference in both genome A and genome B where 
                                    the reference score of genome B is less than 
                                    RefScoreB for this locus.
            SomaticScore            Equal to 1.0 - 
                                    (1.0-min(VarScoreARank,RefScoreBRank))^2. This 
                                    column can be interpreted as a somatic score 
                                    such that a higher score indicates greater 
                                    likelihood that the listed varition is indeed 
                                    somatic, as opposed to a false negative in 
                                    genome B or a false positive in the genome A. 
                                    See the methods doc for more detail.
    
    OPTIONS
      -h [ --help ] 
            Print this help message.
    
      --reference arg
            The input crr file.
    
      --variantsA arg
            The "A" input variant file.
    
      --variantsB arg
            The "B" input variant file.
    
      --output-prefix arg
            The path prefix for all output reports.
    
      --reports arg (=SuperlocusOutput,SuperlocusStats,LocusOutput,LocusStats)
            Comma-separated list of reports to generate. (Beware any reports whose 
            name begins with "Debug".) A report is one of:
                SuperlocusOutput      Report for superlocus classification.
                SuperlocusStats       Report for superlocus classification stats.
                LocusOutput           Report for locus classification.
                LocusStats            Report for locus stats.
                VariantOutput         Both variant files annotated by comparison 
                                      results.If the somatic output report is 
                                      requested, file A is also annotated with the 
                                      same score ranks as produced in that report.
                SomaticOutput         Report for the list of simple variations that
                                      are present only in file "A", annotated with 
                                      the score that indicates the probability of 
                                      the variation being truly somatic. Requires 
                                      beta, export-rootA, and export-rootB options 
                                      to be provided as well. Note: generating this
                                      report slows calldiff by 10x-20x.
                DebugCallOutput       Report for call classification.
                DebugSuperlocusOutput Report for debug superlocus information.
                DebugSomaticOutput    Report for distribution estimates used for 
                                      somatic rescoring. Only produced if 
                                      SomaticOutput is also turned on.
            
    
      --locus-stats-column-count arg (=15)
            The number of columns for locus compare classification in the locus 
            stats file.
    
      --max-hypothesis-count arg (=32)
            The maximum number of possible phasings to consider for a superlocus.
    
      --no-reference-cover-validation 
            Turns off validation that all bases of a chromosome are covered by 
            calls of the variant file.
    
      --export-rootA arg
            The "A" export package root, for example /data/GS00118-DNA_A01; this 
            directory is expected to contain ASM/REF and ASM/EVIDENCE 
            subdirectories.
    
      --export-rootB arg
            The "B" export package root.
    
      --beta 
            This flag enables the SomaticOutput report, which is beta 
            functionality.
    
    
    SUPPORTED FORMAT_VERSION
        0.3 or later
    
listvariants
-----------------------------------

::

    COMMAND NAME
        listvariants - Lists the variants present in a variant file.
    
    DESCRIPTION
        Lists all called variants present in the specified variant files, in a 
        format suitable for processing by the testvariants command. The output is a
        tab-delimited file consisting of the following columns:
        
            variantId  Sequential id assigned to each variant.
            chromosome The chromosome of the variant.
            begin      0-based reference offset of the beginning of the variant.
            end        0-based reference offset of the end of the variant.
            varType    The varType as extracted from the variant file.
            reference  The reference sequence.
            alleleSeq  The variant allele sequence as extracted from the variant 
                       file.
            xRef       The xRef as extrated from the variant file.
    
    OPTIONS
      -h [ --help ] 
            Print this help message.
    
      --beta 
            This is a beta command. To run this command, you must pass the --beta 
            flag.
    
      --reference arg
            The reference crr file.
    
      --output arg (=STDOUT)
            The output file (may be omitted for stdout).
    
      --variants arg
            The input variant files (may be positional args).
    
      --variant-listing arg
            The output of another listvariants run, to be merged in to produce the 
            output of this run.
    
      --list-long-variants 
            In addition to listing short variants, list longer variants as well 
            (10's of bases) by concatenating nearby calls.
            
    
    
    SUPPORTED FORMAT_VERSION
        0.3 or later
    
