#!/usr/bin/env python3

import subprocess
import warnings
import argparse

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


    parser.add_argument('-tl',
                        '--threshold_low',
                        help= 'clustering threshold low side',
                        metavar = 'threshold_low', 
                        type= float,
                        default = .0000006)

    parser.add_argument('-th',
                    '--threshold_high',
                    help= 'clustering threshold high side',
                    metavar = 'threshold_high', 
                    type= float,
                    default = .00000012)
    
    parser.add_argument('-s',
                '--steps',
                help= 'number of steps to take in iterration',
                metavar = 'steps', 
                type= int,
                default = 5)

    

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
    warnings.filterwarnings('ignore')
    args = get_args()


    # Define steps
    x = args.threshold_low
    y = args.threshold_high
    n = args.steps
    step = (y - x) / (n - 1)

    frames = [x + step * i for i in range(n)]

    for i in frames:
        
        file_name = 'detection_out_' + str(i)
        
        command = ['./clustering_points_v3.py', args.csv_list, '-t', i, '-f', file_name]

        subprocess.call(command)
        # ./clustering_points_v3_naming.py /home/travis_s/data/season10_plant_detection/season10_plant_detection -r /home/travis_s/data/plant_prediction_data/intermediate/stereoTop/high_number_marked_doubles.csv -f naming_update_clustering_full








# --------------------------------------------------
if __name__ == '__main__':
    main()