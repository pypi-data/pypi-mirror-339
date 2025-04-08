# Experanto
Python package to interpolate recordings and stimuli of neuroscience experiments 

## Use specification
- Instantiation
```python
dat = Experiment('dataset-folder', discretization=30) # 30Hz
```

- Single frame or sequence access
```python
item = dat[10]
sequence = dat[10:100]
```


## Data Folder Structure
Do we want 0001 blocks in eye_tracker/running_wheel/responses?
```
dataset-folder/

  screen/
    0001/ # this could be a block of images
      meta.yaml #what type of interpolator should be used for which block / which data type each block is
      timestamps.npz
      meta/
        condition_hash.npy
        trial_idx.npy
      data/
        img01.png
        img02.png
        ...
    0002/ # this could be a block of videos
      ...
    0003/ # this could be a abother block of images 
      ...
  eye_tracker/
    meta.yaml
    timestamps.npz
  running_wheel/
    meta.yaml
    timestamps.npz
  multiunit/
    meta.yaml
    timestamps.npz
  poses/
    meta.yaml
    timestamps.npz
```

## Example for meta.yaml

```
modality: images
```

