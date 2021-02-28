from dataclasses import dataclass
import h5py
import numpy as np
import pandas as pd
from typing import List, Type, TypeVar

LS = TypeVar('LibrarySpectrum', bound='C')

@dataclass
class LibrarySpectrum:
    """Data class for creating specral objects within the spectral library database,
    managed in an HDF5 file.
    
    Any individual library spectra should only need to be added once. It will then be
    available for all future spectral library calls."""
    
    ### HDF5 attrubutes ###
    name: str # name of species
    chemical_formula: str #chemical formula
    temp: float # temperature of sample (K)
    grain_size: np.array # grain size [min, max] (microns)
    spec_type: str # lab, shkuratov (from optical constants), etc.
    hydration: int # hydration state 0=anhydrous, 2 = (H2O)2, etc.
    spec_features: np.array # major spectral features (microns)
    source: str # where was data accessed? link if available
    citation: str # paper/citation
        
    ### HDF5 data ###
    wavelength: np.array # microns
    albedo: np.array #reflectance albedo
        
    def to_dict(self, incl_data = False):
        """Add any new attributes here."""
        
        d = {
            'name': self.name,
            'chemical_formula': self.chemical_formula,
            'temp': self.temp,
            'grain_size': self.grain_size,
            'spec_type': self.spec_type,
            'hydration': self.hydration,
            'spec_features': self.spec_features,
            'source': self.source,
            'citation': self.citation,
            }
        
        if incl_data:
            d['wavelength'] = self.wavelength
            d['albedo'] = self.albedo
            
        return d
        
    def save(self, filenm):
        """ Add LibrarySpectrum to the spectral library (HDF5 file)."""
        
        with h5py.File(filenm, 'a') as f:
            # create data set
            dset = f.create_dataset(self.name, data=np.stack((self.wavelength, self.albedo), axis=1))
            
            # add attributes
            attr = self.to_dict(self)
            for key in attr.keys():
                dset.attrs[key] = attr[key]
       
    @classmethod
    def load(cls, filenm, name) -> LS:
        """ Load an individual spectrum, name, from HDF5 library."""
        
        with h5py.File(filenm, 'r') as f:
            dset = f[name]
            attrs = {**dset.attrs}
            if 'albedo' not in attrs:
                attrs['albedo'] = dset[:,1]
            if 'wavelength' not in attrs:
                attrs['wavelength'] = dset[:,0]
            
            return cls(**attrs)
    

##### Useful functions for loading spectral library from HDF5 file using the LibrarySpectrum dataclass #####

def batch_load(filenm) -> List[LibrarySpectrum]:
    """Load full HDF5 spectral library as a list of LibrarySpectrum"""
        
    with h5py.File(filenm, 'r') as f:
        spectral_library = [LibrarySpectrum.load(filenm, name) for name in f]
        
    return spectral_library
        

def load_dataframe(filenm) -> pd.DataFrame:
    """Load full HDF5 spectral library as a (queryable) pandas dataframe."""
    
    return pd.DataFrame.from_records([s.to_dict(incl_data=True) for s in batch_load(filenm)]) #Dataframe of attributes
    

    
### Sample Code to Add a new laboratory spectrum to the library ###

# filenm = 'spectral_library.hdf5' #spectral library file
# data = np.loadtxt('lib_spec/MgCl2.2H2O_80K.txt', skiprows=4)
# spec = lib.LibrarySpectrum(name = 'magnesium chloride dihydrate'
#                            ,chemical_formula = 'MgCl2_(H2O)2'
#                            ,temp = 80. #K
#                            ,grain_size = np.array(['flash frozen']).astype('S1') #only need .astype if np.array of strings
#                            ,spec_type = 'lab'
#                            ,hydration = 2
#                            ,spec_features = np.array([1.45, 1.97])
#                            ,source = 'https://agupubs.onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2F2013JE004565&file=jgre20327-sup-0005-dataSetS4.txt'
#                            ,citation = 'Hanley et al (2014)'
#                            ,wavelength = data[:,0] #um
#                            ,albedo = data[:,1]
#                            )

# spec.save(filenm)