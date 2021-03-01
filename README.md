# LinearSpectralModelling

Framework for building a spectral library and performing linear spectral modelling on planetary surface spectra

## Add a new laboratory spectra to the library

To add a new spectrum to the spectral library, first create a LibrarySpectrum class object with the information about the spectra. Then use the save method to add your spectrum to the library.


```python
import numpy as np
import pandas as pd
from SpectralLibrary import spectral_library_utils as lib

filenm = 'example_library.hdf5' #spectral library file

data = np.loadtxt('Examples/NaCl_80K.txt', skiprows=4)
spec = lib.LibrarySpectrum(name = 'sodium chloride'
                           ,chemical_formula = 'NaCl'
                           ,temp = 80. #K
                           ,grain_size = np.array([20,50])
                           ,spec_type = 'lab'
                           ,hydration = 0 #anhydrous
                           ,spec_features = np.array([]) #empty if no features of note
                           ,source = 'https://agupubs.onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2F2013JE004565&file=jgre20327-sup-0014-dataSetS13.txt'
                           ,citation = 'Hanley et al (2014)'
                           ,wavelength = data[:,0] #um
                           ,albedo = data[:,1]
                           )
spec.save('Examples/'+filenm) #overwrite=True only if you want to replace an existing object with the same name
```

## Read in spectral library to pandas dataframe


```python
df = lib.load_dataframe(filenm)
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>chemical_formula</th>
      <th>temp</th>
      <th>grain_size</th>
      <th>spec_type</th>
      <th>hydration</th>
      <th>spec_features</th>
      <th>source</th>
      <th>citation</th>
      <th>wavelength</th>
      <th>albedo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>sodium chloride</td>
      <td>NaCl</td>
      <td>80.0</td>
      <td>[20, 50]</td>
      <td>lab</td>
      <td>0</td>
      <td>[]</td>
      <td>https://agupubs.onlinelibrary.wiley.com/action...</td>
      <td>Hanley et al (2014)</td>
      <td>[0.35, 0.351, 0.352, 0.353, 0.354, 0.355, 0.35...</td>
      <td>[0.256260774, 0.258040028, 0.260486898, 0.2613...</td>
    </tr>
  </tbody>
</table>
</div>


