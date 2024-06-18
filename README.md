# RGB Identification Agglomerative Clustering

This repository contains the agglomerative clustering script used in the PhytoOracle pipeline to track plants over time for season 11. 

## Running the container
singularity build s11_clustering.simg docker://phytooracle/s11_clustering:latest
singularity run s11_clustering.simg <directory containing CSVs>

This container is typically used initially to create an RGB clustering file with the RGB detections as input. When this is done, the resulting CSV can be used for clustering FLIR images by including it in a directory of FLIR detections, and running the container again.

This container should be run on Puma with 94 cores and 5 GB of memory per core to provide the maximum amount of memory to the container. If requested memory is higher than what is available, the HPC job scheduler will kill the job.

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



