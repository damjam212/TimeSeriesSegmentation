import pandas as pd
import numpy as np
import stumpy
import matplotlib.pyplot as plt
from stumpy.floss import _cac
from scipy.signal import argrelextrema


def get_indices_matricies(data,m):
    mp = stumpy.stump(data, m)
    return mp[:, 1] 
        
def get_cac_curves(mpi,L,exclusion_factor):
    cac = _cac(mpi, L=L, excl_factor=exclusion_factor)
    return cac

class Fluss:
    def __init__(self,L,exclusion_factor):
        self.L=L
        self.exclusion_factor = exclusion_factor
        self.custom_extraction_zone = 5*L 
        self.last_regimes = None
        self.last_cac = None
        self.last_data = None
        
    def set_custom_regime_extraction(self, extraction_zone ):
        self.custom_extraction_zone = extraction_zone 
        
    def predict_regimes(self,data):
        self.last_data = data
        mp = stumpy.stump(data, m=self.L)
        cac = _cac(mp[:, 1], L=self.L, excl_factor=self.exclusion_factor)
        self.last_cac = cac

        local_minima_indices = argrelextrema(cac, np.less, order=self.custom_extraction_zone)[0]
        self.last_regimes = local_minima_indices
        return cac, local_minima_indices

    
    def m_predict_regimes(self,data):
        self.last_data = data
        m_mp = np.apply_along_axis(get_indices_matricies, 0, data,self.L)
        m_cac = np.apply_along_axis(get_cac_curves, 0, m_mp,self.L,self.exclusion_factor)
        mean_cac = np.mean(m_cac, axis=1)

        self.last_cac = mean_cac
        
        local_minima_indices = argrelextrema(mean_cac, np.less, order=self.custom_extraction_zone)[0]
        self.last_regimes = local_minima_indices
        return mean_cac, local_minima_indices

            
    def print_latest_output(self, original_points = None):
        fig, axs = plt.subplots(2, sharex=True, gridspec_kw={'hspace': 0})
        axs[0].plot(range(self.last_data.shape[0]), self.last_data)
        axs[1].plot(range(self.last_cac.shape[0]), self.last_cac, color='C1')
        
        for i in self.last_regimes:
            axs[0].axvline(x=i, linestyle="dashed")
            axs[1].axvline(x=i, linestyle="dashed")

        if original_points is not None:            
            for i in original_points:
                axs[0].axvline(x=i, linestyle="dashed", color='g')
                axs[1].axvline(x=i, linestyle="dashed", color='g')
            
        plt.show()


#eval
            

# FlussRegimeSegmentator = Fluss(1000,3,5)
# FlussRegimeSegmentator.turn_custom_regime_extraction()
# # cac , regimes = FlussRegimeSegmentator.predict_regimes(data)
# # FlussRegimeSegmentator.print_latest_output()

# m_data = cricet_stacked_ndarray.astype(np.float64)
# cac , m_cac ,regimes = FlussRegimeSegmentator.m_predict_regimes(m_data)
# FlussRegimeSegmentator.print_latest_output()
