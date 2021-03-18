#!/usr/bin/env python3
"""
Author : Travis Simmons, Emmanuel Gonzalez
Date   : 2020-10-30
Purpose: Plant clustering for a full growing season using agglomerative clustering
"""

import argparse
import os
import sys
import numpy as np
import pandas as pd
import sklearn
import glob
from sklearn.cluster import AgglomerativeClustering



# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Plant clustering',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# Working 1/24/2021
#     parser.add_argument('csv_list',
#                         nargs='+',
#                         metavar='csv_list',
#                         help='Directory containing CSV files to match')

# Added 1/24/2021
    parser.add_argument('csv_list',
                        metavar='csv_list',
                        type = str,
                        help='Directory containing CSV files to match')


    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory',
                        metavar='outdir',
                        type=str,
                        default='pointmatching_out')

    parser.add_argument('-f',
                        '--filename',
                        help='Output filename',
                        metavar='filename',
                        type=str,
                        default='agglomerative_plant_clustering')

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Cluster points"""

    args = get_args()
    df_list = []

    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)
        
      # Working 1/24/2021
#     for csv in args.csv_list:
#         df = pd.read_csv(csv, engine='python')
#         df_list.append(df)
    
    # Added 1/24/2021
    identifications = glob.glob(os.path.join(args.csv_list,'*.csv'))
    
    for csv in identifications:
        df = pd.read_csv(csv, engine='python')
        df_list.append(df)
    # ----------------------------------------------------------------
    whole = pd.concat(df_list)

    # Creates a list of all unique genotypes in day 2 that we can itterate over.
    geno_list = whole.genotype.unique().tolist()
    
    # Green towers border is our buffer group and will not be included in analysis
    if 'Green_Towers_BORDER' in geno_list:
        geno_list.remove('Green_Towers_BORDER')

    # Run clustering algorithm and add matching column: plant_name 
    model = sklearn.cluster.AgglomerativeClustering(n_clusters=None, affinity='euclidean', memory=None, connectivity=None, compute_full_tree='auto', linkage='average', distance_threshold= .0000006)
    matched_df = pd.DataFrame(columns=['date',
                                        'treatment',
                                        'plot',
                                        'genotype',
                                        'lon',
                                        'lat',
                                        'min_x',
                                        'max_x',
                                        'min_y',
                                        'max_y',
                                        'nw_lat',
                                        'nw_lon',
                                        'se_lat',
                                        'se_lon',
                                        'bounding_area_m2'])

    # Doing the prediction by genotype so it doesn't get overwhelmed
    for geno in geno_list:
        sub_df = whole.set_index('genotype').loc[geno]
        
        # An agglomerative clustering model is fitted for each genotype
        try:
            cords = list(zip(sub_df['lon'], sub_df['lat']))
            clustering = model.fit_predict(cords)
            geno_clustered = sub_df.assign(plant_name = clustering)
            matched_df = pd.concat([matched_df,geno_clustered])
             
        except:
            pass

    # Assigning the match names to the plants and exporting
    matched_df = matched_df.reset_index()
    matched_df['genotype'] = matched_df['index']
    del matched_df['index']
  
    names = list(zip(matched_df['genotype'], matched_df['plant_name']))
    names_format = [i[0] + '_' + str(int(i[1])) for i in names]
    
    matched_df = matched_df.assign(plant_name = names_format)

    out_path = os.path.join(args.outdir, args.filename + '.csv')
    matched_df.to_csv(out_path)
    
# --------------------------------------------------
if __name__ == '__main__':
    main()
