"""
Custom extensions to Wonambi spindle detection
"""

from numpy import mean, arange
from wonambi.detect import DetectSpindle as OriginalDetectSpindle

class ImprovedDetectSpindle(OriginalDetectSpindle):
    def __init__(self, method='Moelle2011', frequency=None, duration=None, merge=False):
        super().__init__(method, frequency, duration, merge)
        
        # Fix the frequency issue by updating all relevant parameters
        if frequency is not None:
            # Update frequency in all relevant method parameters
            if hasattr(self, 'det_remez'):
                self.det_remez['freq'] = self.frequency
            if hasattr(self, 'det_butter'):
                self.det_butter['freq'] = self.frequency
            if hasattr(self, 'det_low_butter') and hasattr(self, 'cdemod'):
                self.cdemod['freq'] = mean(self.frequency)
            if hasattr(self, 'det_wavelet'):
                if 'f0' in self.det_wavelet:
                    self.det_wavelet['f0'] = mean(self.frequency)
                if 'freqs' in self.det_wavelet:
                    self.det_wavelet['freqs'] = arange(self.frequency[0],
                                                    self.frequency[1] + .5, .5)
            if hasattr(self, 'sel_wavelet'):
                if 'freqs' in self.sel_wavelet:
                    self.sel_wavelet['freqs'] = arange(self.frequency[0],
                                                    self.frequency[1] + .5, .5)
            if hasattr(self, 'moving_power_ratio'):
                self.moving_power_ratio['freq_narrow'] = self.frequency
        if duration is not None:
            # Update duration in all relevant method parameters
            if hasattr(self, 'det_wavelet'):
                if 'duration' in self.det_wavelet:
                    self.det_wavelet['duration'] = duration
                if 'duration' in self.sel_wavelet:
                    self.sel_wavelet['duration'] = duration
            if hasattr(self, 'moving_power_ratio'):
                self.moving_power_ratio['duration'] = duration
