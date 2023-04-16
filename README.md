# amppred
Snakemake pipeline to perform consensus antimicrobial prediction on a set of proteins in fasta format using three tools based on machine learning.
## Usage
Put the target files in the directory samples as a fasta file with the extension ".faa" and run:
`snakemake --use-conda -j <cores>`
## Requirements
- Conda
- Snakemake
- [Ampep](https://github.com/tlawrence3/amPEPpy)
- [AmpGram](https://github.com/michbur/AmpGram)
- [AMP scanner v2](https://www.dveltri.com/ascan/v2/ascan.html)
- Python packages: pandas, seaborn and scipy.
## Model references
- *Burdukiewicz, M. et al. Proteomic Screening for Prediction and Design of Antimicrobial Peptides with AmpGram. Int J Mol Sci 21, 4310 (2020).*
- *Lawrence, T. J. et al. amPEPpy 1.0: A portable and accurate antimicrobial peptide prediction tool. Bioinformatics btaa917- (2020) doi:10.1093/bioinformatics/btaa917.*
- *Daniel Veltri, Uday Kamath, Amarda Shehu, Deep learning improves antimicrobial peptide recognition, Bioinformatics, Volume 34, Issue 16, 15 August 2018, Pages 2740–2747, https://doi.org/10.1093/bioinformatics/bty179*