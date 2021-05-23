#!/usr/bin/env python3
"""
Author : Travis Simmons, Emmanuel Gonzalez
Date   : 2020-10-30
Purpose: Plant clustering for a full growing season using agglomerative clustering
Sample Deployment: ./clustering_points_v2.py /home/travis_s/data/season10_plant_detection/season10_plant_detection 
                    -r /home/travis_s/data/plant_prediction_data/intermediate/stereoTop/high_number_marked_doubles.csv 
                    -f final_clustering_out_with_high_number_doubles
"""

import argparse
import os
import sys
import numpy as np
import pandas as pd
import sklearn
import glob
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import FeatureAgglomeration

# ./clustering_points_v3_naming.py /home/travis_s/data/season10_plant_detection/season10_plant_detection -r /home/travis_s/data/plant_prediction_data/intermediate/stereoTop/high_number_marked_doubles.csv -f naming_update_clustering_full

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

    parser.add_argument('-r',
                        '--remove_points',
                        help='A csv of points, that if they are included in a cluster, they get a 1 in the double_lettuce column',
                        metavar='remove_points',
                        type=str)


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
    print(identifications)
    
    for csv in identifications:
        df = pd.read_csv(csv, engine='python')
        df_list.append(df)
    # ----------------------------------------------------------------
    whole = pd.concat(df_list)
    
    # Creates a list of all unique genotypes in day 2 that we can itterate over.
    geno_list = whole.genotype.unique().tolist()
    geno_list = [x for x in geno_list if str(x) != 'nan']

    whole['double_lettuce'] = 0
    print(len(whole))
    if args.remove_points:
        double_df = pd.read_csv(args.remove_points)
        double_df['double_lettuce'] = 1
        whole = pd.concat([whole, double_df])

    print(len(whole))

 
    # print(geno_list)


    
    # Green towers border is our buffer group and will not be included in analysis
    #if 'Green_Towers_BORDER' in geno_list:
    #    geno_list.remove('Green_Towers_BORDER')

    # Run clustering algorithm and add matching column: plant_name 
    model = sklearn.cluster.AgglomerativeClustering(n_clusters=None, affinity='euclidean', memory=None, connectivity=None, compute_full_tree='auto', linkage='average', distance_threshold= .0000006)
    # model = FeatureAgglomeration(n_clusters=None, compute_full_tree = True, distance_threshold = 0.0000012, linkage='ward')
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
                                        'bounding_area_m2',
                                        'plant_name',
                                        'double_lettuce'])
    # # Reverse date matching
    # rgb_dates = matched_df.date.unique()
    # rgb_dates.sort(reverse = True)

    # for date in rgb_dates:
        

    # Doing the prediction by genotype so it doesn't get overwhelmed
    geno_list = geno_list[:4]
    for geno in geno_list:
        print(geno)
        sub_df = whole.set_index('genotype').loc[geno]
        
        # An agglomerative clustering model is fit for each genotype
        try:
            cords = list(zip(sub_df['lon'], sub_df['lat']))

            clustering = model.fit_predict(cords)

            # at this point plant name is a clustering number generated by the fit_predict (no genotype)
            # We need to separate plants at this stage whose clustering numbers match, and give them a name
            geno_clustered = sub_df.assign(plant_name = clustering)

            for i in geno_clustered.plant_name.unique():

                single_plant_df = geno_clustered[geno_clustered['plant_name'] == i]
                
                for index, row in single_plant_df.iterrows():
                    lat_main = row['lat']
                    plot_main = row['plot']
                    break
                # lat_main = single_plant_df.loc[[geno], ['lat']]
                lat_format = str(lat_main).replace('.', '')[:12]


                # plot_main = single_plant_df[[geno], ['plot']]

                names_format = geno + '_' + str(plot_main) + '_' + lat_format

                

                # single_plant_df = single_plant_df.assign(plant_name = names_format)

                single_plant_df['plant_name'] = names_format
                single_plant_df['genotype'] = geno
                # print('good')

                matched_df = pd.concat([matched_df,single_plant_df])


            
             
        except:
            pass

    # # Assigning the match names to the plants and exporting
    # matched_df = matched_df.reset_index()
    # matched_df['genotype'] = matched_df['index']
    # del matched_df['index']
  
    # names = list(zip(matched_df['genotype'], matched_df['plant_name']))
    # names_format = [i[0] + '_' + str(int(i[1])) for i in names]
    


    # matched_df = matched_df.assign(plant_name = names_format)
    
    # changing the double_lettuce column for the ones that were matched with doubles
    if args.remove_points:
    
        doubles_matches = matched_df[matched_df['double_lettuce'] == 1]

        double_plants = doubles_matches.plant_name.unique()

        matched_df = matched_df.set_index('plant_name')
        for i in double_plants:
            matched_df.loc[i, 'double_lettuce'] = 1
        matched_df = matched_df.reset_index()

    # Dropping the rows from the double lettuce template
    nan_value = float("NaN")
    matched_df.replace("", nan_value, inplace = True)
    matched_df.dropna(subset = ['bounding_area_m2'], inplace = True)

    # Getting rid of double identifications
    plant_names = matched_df.plant_name.unique()

    for i in plant_names:

        # Creating an rgb df for one plant 
        one_plant_rgb_df1 = matched_df.loc[matched_df['plant_name'] == i, ['date', 'bounding_area_m2']]

        # There is an error here where sometimes a plant was seen twice on the same day.
        # I am implementing a decision rule that we have used before for double identifications
        # If it was identified twice, the biggest identification is the real one. 
        # The second identification was most likely it bleeding into another plot or a weed.\]
        # I am only doing this for rgb because the way the clustering is done for flir we shouldn't have double identifications
        # I may go back and change how rgb is clustered to include this condidtional
        
        # Checking for double dates
        if not one_plant_rgb_df1["date"].is_unique:

            # pull out the rows that have the same date
            drop_df = one_plant_rgb_df1[one_plant_rgb_df1.duplicated('date', keep=False) == True]

            # Implement decision rule described above
            for x in drop_df.date.unique():
                one_day_drop_df = drop_df[drop_df['date'] == x]

                # drop the ones that are not the max,
                # this makes this solution handle if the plant was seen more than twice
                dont_drop_df = one_day_drop_df[one_day_drop_df['bounding_area_m2'] == max(one_day_drop_df['bounding_area_m2'])]
                
                # drop the one we want to keep
                one_day_drop_df.drop(labels = dont_drop_df.index[0], axis = 0, inplace = True)

                # Drop the rest from the main df
                matched_df.drop(labels = one_day_drop_df.index[:], axis = 0, inplace = True)
    
    matched_df.drop( labels = ['Unnamed: 0', 'id', 'geometry','index_right', 'ID'], axis = 1, inplace = True)
    # Outputting finished file
    out_path = os.path.join(args.outdir, args.filename + '.csv')
    matched_df.to_csv(out_path)
# --------------------------------------------------
if __name__ == '__main__':
    main()
