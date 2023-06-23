#!/usr/bin/env python
#  Copyright (c) Microsoft Corporation. 
#  Licensed under the MIT license. 

import sys
import gzip
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--data", required=True, help="gz file containing test data")
parser.add_argument("--testids", required=True, help="multi-ref test set with string replaced with IDs")
parser.add_argument("--out", required=True, help="output multi-ref file")

args = parser.parse_args()

data = {}

with gzip.open(args.data, 'rt', encoding="utf-8") as f:
	for line in f:
		line = line.rstrip()
		line = line.replace('“','"')
		line = line.replace('”','"')
		keys, src, tgt = line.split('\t')
		data[keys] = (src, tgt)

with open(args.out, 'wt', encoding="utf-8") as fo:
	with open(args.testids, 'rt', encoding="utf-8") as fi:
		for line in fi:
			line = line.rstrip()
			els = line.split('\t')
			header = els[0]
			if header != 'multiref':
				print(f"Ignoring line: {line}", file=sys.stderr)
			rscore1, rids1 = els[1].split(',', 1)
			if rids1 not in data.keys():
				print(f"Error: can't find data for ref ID: {rids1}", file=sys.stderr)
				continue
			src, r1 = data[rids1]
			scores = [ rscore1 ]
			refs = [ r1 ]
			for el in els[2:]:
				rscoreI, ridsI = el.split(',', 1)
				if ridsI in data:
					srcI, rI = data[ridsI]
					if srcI == src:
						scores.append(rscoreI)
						refs.append(rI)

					else:
						print(f"Error: mismatch source for ref ID: {ridsI}", file=sys.stderr)
				else:
					print(f"Error: can't find data for ref ID: {ridsI}", file=sys.stderr)
			# Write multi-ref instance:
			fo.write(f'{src}')
			for i in range(len(scores)):
				fo.write('\t%s|%s' % (scores[i], refs[i]))
			fo.write('\n')
