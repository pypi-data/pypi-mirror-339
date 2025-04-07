"""
turtlewave_hdEEG - Extended Wonambi for large EEG datasets
"""

__version__ = '0.1.0'

# Import important classes to expose at the package level
from .dataset import LargeDataset
from .visualization import EventViewer
from .annotation import XLAnnotations, CustomAnnotations
from .eventprocessor import ParalEvents
from .extensions import ImprovedDetectSpindle
