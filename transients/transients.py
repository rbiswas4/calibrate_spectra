#!/usr/bin/env python
"""
Constructing objects representing a single astrophysical source with spectra
taken on a certain number of days with photometry on at least the same ?24? hour
span. The raw spectroscopic data, and a set of the spectroscopic data multipled by splines to best match the photometry at the same time, and the photometry 
have been by N. Karpenka, and form the basis for this study
"""
 

class TransientObject(object):
    def __init__(self,
                 spectral_data,
                 matched_spectra,
                 days,
                 data_fnames=None,
                 mangled_fnames=None):
        """
        Constructor
        
        Parameters
        ----------
        spectral_data: list of 2-D `np.ndarray` of floats
            list of all the spectral data available corresponding to the object.
            Each `np.ndarray` has columns of wavelength and specific flux in
            units of Ang and arbitrary units respectively
        matched_spectra: list of 2-D `np.ndarray` of floats 
            list of all of the 'mangled' spectral data matched to the
            photometry of the transient object, in the form of 2-D `np.ndarray`.
            The list of arrays is indexed identically to the `spectral data`.
            Each `np.ndarray` has columns wavelength in units of Ang, and
            specific flux ($f_\lambda$) in units of ergs/cm^2/s/Ang. It is
            assumed that the wavelengths are indexed in ascending order.
        days: `np.ndarray` of floats
            days on which the spectral_data were taken in the same.  
        
        Returns
        -------
        instance of TransientObject class
        
        .. note :: 1. the wavelength gridding of the `mangled` matched spectra
        should be identical, and may differ from the wavelength gridding of the
        spectral_data of the object from which it was constructed. 2. The
        wavelengths in the matched spectra are assumed to be in increasing
        order.
        """
        
        self.sortOrder = np.argsort(days)
        self.data_fnames = data_fnames[self.sortOrder]
        self.mangled_fnames = mangled_fnames[self.sortOrder]
        self.spectral_data = np.array(spectral_data)[self.sortOrder]
        self.mangled_spectra = np.array(matched_spectra)[self.sortOrder]
        self.mjds = np.array(days)[self.sortOrder]
        
        self.validateWavelengths()
        
        
    @classmethod
    def fromDataDir(cls, spectralDataDir):
        """
        """
        import glob

        
        spectralDataFname = np.array(glob.glob(spectralDataDir + '/*.dat'))
        mangledDataFname = np.array(glob.glob(spectralDataDir + '/*mangled.txt'))
            
        spectral_data = map(lambda x: np.loadtxt(x, skiprows=2),
                            spectralDataFname) 
        matched_spectra = map(lambda x: np.loadtxt(x, skiprows=2),
                              mangledDataFname)
        days = map(cls.parse_mjds, mangledDataFname)
        
        
            
        return cls(spectral_data=spectral_data, matched_spectra=matched_spectra, days=days,
                   data_fnames=spectralDataFname, mangled_fnames=mangledDataFname) 
            
    @staticmethod    
    def parse_mjds(mangledSpectraFileName):
        """
        
        """
        s = mangledSpectraFileName.split('_mangled')[0]
        day = s.split('_')[-1]
        return float(day)
    
    def validateWavelengths(self, verbose=False):
        """
        Check that the wavelength grid of the `self.matched_spectra
        are identical to each other and that the wavelengths are
        in increasing order
        """
        firstwave = self.mangled_spectra[0][:, 0]
        
        for i, mangledSpectra in enumerate(self.mangled_spectra):    
            wave = mangledSpectra[:, 0]
            if len(wave) != len(firstwave):
                print "Different lengths for ", 0, i
            elif not np.allclose(wave, firstwave):
                print 'Different values for ', 0, i
            else:
                if verbose:
                    print '0 ', i , ' match!'
