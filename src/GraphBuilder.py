from graphProcessing.BuildGraph import *
from graphProcessing.ReadWrite import *

import argparse
from os.path import join
import pandas as pd

def buildGraph(corpus_dir, pref_filename, tag_filename):
	print("reference loading")
	df_tag = pd.read_table(join(corpus_dir, tag_filename))
	df_pref = pd.read_table(join(corpus_dir, pref_filename))

	print("building the graph")
	G = TriGraph(df_tag, df_pref)
	G.buildNodeList(False)

	df_table = G.buildMapping()

	# dump table.csv
	print("dumping the table.csv")
	df_table.to_csv(join(corpus_dir, 'table.csv'), index = False);

	# dump typeMap.txt
	print("dumping the typeMap.txt")
	with open(join(corpus_dir, 'typeMap.txt'),'w') as fout:
		for key in G.dict:
			fout.write(key + ' ' + key[:4] + '\n')

	return G


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--prefFileName', type=str, default='toy_preference.txt',
                       help='preference file name')
	parser.add_argument('--tagFileName', type=str, default='toy_tags.txt',
					   help='tags file name')
	parser.add_argument('--corpus_dir', type=str, default='./corpus',
                       help='Data directory')


	args = parser.parse_args()

	G = buildGraph(args.corpus_dir, args.prefFileName, args.tagFileName)

	writeGraph(G, 'graph')

	

if __name__ == '__main__':
	main()