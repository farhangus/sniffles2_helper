from src.vcf import *
import statistics


def sniffles2_single(args, stdin, printout=False):
    # header
    print(f'#CHROM\tPOSITION\tGENOTYPE\tSVTYPE\tSVLEN\tCOVERAGE\tAF\tREF\tALT', end="\n") if printout else None
    gt_filter = [] if args.filer_gt == "" else args.filer_gt.split(",")
    # results
    for line in stdin:
        # skip comments
        if not line.startswith("#"):
            vcf_entry = VCFLineSV(line.rstrip("\n"))
            gt = vcf_entry.GENOTYPE
            if gt not in gt_filter:
                if (vcf_entry.DR+vcf_entry.DV) >= args.minsupp or not vcf_entry.has_coverage:
                    if vcf_entry.has_coverage:
                        af = "{:0.3f}".format(vcf_entry.AF) if vcf_entry.AF != "NA" else "NA"
                        coverage = vcf_entry.DR+vcf_entry.DV
                        if vcf_entry.SVTYPE == "BND":
                            print(f'{vcf_entry.CHROM}\t{vcf_entry.POS}\t{gt}\t{vcf_entry.SVTYPE}\t{vcf_entry.TRA}\t'
                                  f'{coverage}\t{af}\t{vcf_entry.DR}\t{vcf_entry.DV}\t'
                                  f'{vcf_entry.ID}:{vcf_entry.FILTER}', end="\n")
                        else:
                            print(f'{vcf_entry.CHROM}\t{vcf_entry.POS}\t{gt}\t{vcf_entry.SVTYPE}\t'
                                  f'{vcf_entry.SVLEN}\t{coverage}\t{af}\t{vcf_entry.DR}\t{vcf_entry.DV}\t'
                                  f'{vcf_entry.ID}:{vcf_entry.FILTER}',
                                  end="\n") if abs(vcf_entry.SVLEN) >= args.minsize else ""
                    else:
                        if vcf_entry.SVTYPE == "BND":
                            print(f'{vcf_entry.CHROM}\t{vcf_entry.POS}\t{gt}\t{vcf_entry.SVTYPE}\t{vcf_entry.TRA}\t'
                                  f'NA\tNA\tNA\tNA\t{vcf_entry.ID}:{vcf_entry.FILTER}', end="\n")
                        else:
                            print(f'{vcf_entry.CHROM}\t{vcf_entry.POS}\t{gt}\t{vcf_entry.SVTYPE}\t'
                                  f'{vcf_entry.SVLEN}\tNA\tNA\tNA\tNA\t{vcf_entry.ID}:{vcf_entry.FILTER}',
                                  end="\n") if abs(vcf_entry.SVLEN) >= args.minsize else ""


def sniffles2_population():
    pass


def sniffles2_cancer():
    pass


def survivor_parse():
    pass


# misc
def is_sv_translocation(the_svtype):
    return the_svtype == "BND" or the_svtype == "TRA"

