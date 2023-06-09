#!/usr/bin/env python
# -*- coding: UTF-8
'''
amp_scanner_predict.py
By: Dan Veltri (dan.veltri@gmail.com)
Last Updated 5.14.2018

Description: Makes AMP predictions given a FASTA file and trained Keras .h5 model as input.

Usage: python amp_scanner_predict.py <input_fasta> <input_model>

Proteins in <input_fasta> must be 20 classic AAs or X (treated as a padding character).
Keras and TensorFlow version of <input_model> HDF5 model should be same as the current system.

Output:	Saves to the current working directory -
		<input>_AMPCandidates.fa - FASTA file of peptides predicted as AMPs
		<input>_Prediction_Summary.csv - CSV file of prediction results

Citation: D. Veltri, U. Kamath and A. Shehu (2018) Bioinformatics, 34(16):2740–2747.
'''

from __future__ import print_function # enable python3 printing
from time import gmtime, strftime
print("STARTING JOB: " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))

from Bio import SeqIO
from keras.models import load_model
from keras.preprocessing import sequence
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2' # turns off tensorflow SSE compile warnings

fname = sys.argv[1] # Input FASTA file of peptides
model = sys.argv[2] # Saved Keras model in HDF5 format'
basefile = os.path.basename(fname)
basename = os.path.splitext(basefile)[0]
thrsh = 0.5 # greater than this value = AMP

# LOAD SEQUENCES
amino_acids = "XACDEFGHIKLMNPQRSTVWY"
aa2int = dict((c, i) for i, c in enumerate(amino_acids))
X_test = []
warn = []
ids = []
seqs = []
max_length = 200

print("Encoding sequences...")
for s in SeqIO.parse(fname,"fasta"):
    if(len(str(s.seq))<10 or len(str(s.seq))>200):
        warn.append('*')
    else:
        warn.append('')
    ids.append(str(s.id))
    seqs.append(str(s.seq))
    X_test.append([aa2int[aa] for aa in str(s.seq).upper()])

X_test = sequence.pad_sequences(X_test, maxlen=max_length)

# LOAD MODEL
print("Loading model and weights for file: " + model)
loaded_model = load_model(model)

# PREDICT AND SAVE
print("Making predictions and saving results...")
#fcand = open("results/" + basename + '_AMPCandidates.fasta','w') # prepended results directory to file name
fpsum = open("results/" + basename + '_amp.csv','w') # so taht it outputs there also changed fa to fasta
fpsum.write("SeqID,Prediction_Class,Prediction_Probability,Sequence\n")

preds = loaded_model.predict(X_test)

for i, pred in enumerate(preds):
    if(pred[0] > thrsh):
        fpsum.write("{},AMP{},{},{}\n".format(ids[i],warn[i],round(pred[0],4),seqs[i]))
       # fcand.write(">{}\n{}\n".format(ids[i],seqs[i]))
    else:
        fpsum.write("{},Non-AMP{},{},{}\n".format(ids[i],warn[i],round(pred[0],4),seqs[i]))

#fcand.close()
fpsum.close()

print("Saved files: " + basename + "_amp.csv")
print("JOB FINISHED: " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))

# END PROGRAM
