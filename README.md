# Agglomerative Plant Clustering Script

This is the agglomerative clustering script used in the PhytoOracle pipline to track plants over days. 

It takes in a csv with at least the columns of 'genotype', 'lat', 'lon'.

It will return a csv with an added column 'plant_name' that is in the format (f'genotype',f'match number'), where match number is the order in which the plant was matched in that genotype. eg: The first plant that is clustered in the Franklin genotype will be named (Franklin, 1).

The script is searching by genotype as it will not cluster the whole csv at one time, so you have to sub sect it. This can be replaced in the script with any catagorical variable from your experiment as long as your csv has that header and you replace 'genotype' everywhere in the script with your catagorical name.

The outputted csv is easy to use with pandas, but can be difficult to read, so in the file containing this readme there is also a csv to json conversion script that creates a more human readable document.

## Arguments and Flags

Positional: 'csv_list' - Directory containing CSV files to match

Flags:  '-o' - Output Directory - Default is pointmatching_out.
        '-f' - Filename of the output csv. - Default is agglomerative_plant_clustering.csv
        
        
