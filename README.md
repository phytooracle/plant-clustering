# RGB Identification Agglomerative Clustering

This repository contains the agglomerative clustering script used in the PhytoOracle pipeline to track plants over time for season 10. 

## Inputs
It takes in a csv with at least the columns of 'genotype', 'lat', 'lon'.

Optional Input: An additional csv containing 'genotype', 'lat', 'lon' using the flag '-r'. Whatever clusters contain these points will get a 1 in their 'double_lettuce' column.

## Outputs
It will return a csv with an added columns 'plant_name' that is in the format (f'genotype',f'match number'), where match number is the order in which the plant was matched in that genotype. eg: The first plant that is clustered in the Franklin genotype will be named (Franklin, 1). There will also be a 'double_lettuce' columns that indicates if the lettuce was clustered with any of the points provided in your 'remove_points' csv. 

The outputted csv is easy to use with pandas, but can be difficult to read, so in the repository containing this readme there is also a csv to json conversion script that creates a more human readable document.

## Arguments and Flags

* **Positional Arguments:** 
    * **Directory containing CSV files to cluster:** 'csv_list'
    
* **Optional Arguments:**
    * **Remove Points:** '-r', '--remove_points'
    * **Output directory:** '-o', '--outdir', default='pointmatching_out'
    * **Output filename:** '-f', '--filename', default='agglomerative_plant_clustering'



