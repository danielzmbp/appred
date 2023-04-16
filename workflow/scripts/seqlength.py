from Bio import SeqIO
import pandas as pd


l = []
for i in SeqIO.parse(snakemake.input[0], "fasta"):
	l.append(len(i.seq))
df = pd.DataFrame(l)
df.columns = ["length"]
df.to_csv(snakemake.output[0], index=False)