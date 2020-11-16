# Agglomerative Plant Clustering Script

This is the agglomerative clustering script used in the PhytoOracle pipline to track plants over days. 

It takes in a csv with at least the columns of 'genotype', 'lat', 'lon'.

It will return a csv with an added column 'plant_name' that is in the format (f'genotype',f'match number'), where match number is the order in which the plant was matched in that genotype. eg: The first plant that is clustered in the Franklin genotype will be named (Franklin, 1).



The outputted csv is easy to use with pandas, but can be difficult to read, so in the repository containing this readme there is also a csv to json conversion script that creates a more human readable document.

## Arguments and Flags

Positional: 'csv_list' - Directory containing CSV files to match

Flags:&nbsp; '-o' - Output Directory - Default is pointmatching_out.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'-f' - Filename of the output csv. - Default is agglomerative_plant_clustering.csv
        

## Adapting the Script

The script is searching by genotype as it will not cluster the whole csv at one time, so you have to sub sect it. This can be replaced in the script with any catagorical
variable from your experiment as long as your csv has that header and you replace 'genotype' everywhere in the script with your catagorical name.

You will also need to change the lines below in the script to match your original csv that you are feeding in.

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
                                        
### Example
For instance if you were running an experiment with two plant types and two treatment groups you may change the lines above to:

    matched_df = pd.DataFrame(columns=['date',
                                        'plant_type',
                                        'treatment',
                                        'lon',
                                        'lat'])
                                        
 And then you would change all occurences of 'genotype' to plant type. This would return a csv with headers = ['date', 'plant_type', 'treatment', 'lon', 'lat', 'plant_name'].
 
 Then your clusters would be named something like (plant_type_1, 23).
 
 Please feel free to reach out if you have any questions, and I will do my best to help. 

