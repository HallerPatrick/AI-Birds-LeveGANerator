# XML Generator

This submodule builds valid xmls (and json) files for the angry birds levels


Workflow steps
1. For this the generator reads the `parameters.txt` 
2. generated images with the help of the GAN network.
3. It generated images in batches for every gameobject (platforms, blocks, tnt and pigs).
4. From those images detect all contures and forward them to a validator, that
   selects those centroids (from the contures), that fit the parameters
   constraints.
5. Generated some birds and look how to choose the platform types
