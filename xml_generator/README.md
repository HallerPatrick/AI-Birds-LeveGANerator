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


## Notes 18.17.2019

Having a hard time building the NN right with the right image dimension. In the end this should be a huge problem,
as it is only scaled for image processing and later rescaled to put it backed in to the xml. 

From the 4 different generators it should be possible to generate valid xmls. The next step is to sanity check those levels for gravity and later for playability. The should be done in continuous intgeration process. 

For this, every generated xml level should be annotated with the generated images from which it comes from. We can then 
retain the models with the positive levels.

