
#from wonambi.detect.spindle import DetectSpindle
from wonambi.trans import select, fetch, math
from wonambi.attr import Annotations
from wonambi.trans.frequency import frequency, timefrequency
from wonambi.trans.filter import filter_
from concurrent.futures import ProcessPoolExecutor, as_completed
from wonambi.trans import select, fetch, get_times
import numpy as np
import time
import os
import multiprocessing
import csv
from turtlewave_hdEEG.extensions import ImprovedDetectSpindle as DetectSpindle
import json
import datetime

class ParalEvents:
    """
    A class for parallel detection and analysis of EEG events such as spindles,
    slow waves, and other neural events across multiple channels.
    """
    
    def __init__(self, dataset, annotations=None):
        """
        Initialize the ParalEvents object.
        
        Parameters
        ----------
        dataset : Dataset or similar
            Dataset object containing EEG data
        annotations : XLAnnotations or similar
            Annotations object for storing and retrieving events
        """
        self.dataset = dataset
        self.annotations = annotations
    
    def process_events_parallel(self, events, data_source=None, window_size=5, n_workers=None, func=None):
        """
        Process EEG events in parallel
        
        Parameters
        ----------
        events : list of dict
            List of events with at least 'start_time' key
        data_source : Dataset or str or None
            Dataset object or path to data file. If None, uses self.dataset.
        window_size : float
            Window size around event in seconds
        n_workers : int or None
            Number of parallel workers. If None, uses CPU count - 1.
        func : callable or None
            Function to apply to each event data, if None just return the data
            
        Returns
        -------
        results : list
            List of processed event data
        """
        # If n_workers not specified, use CPU count - 1 (leave one for system)
        if n_workers is None:
            n_workers = max(1, multiprocessing.cpu_count() - 1)
        
        # Use self.dataset if data_source is None
        if data_source is None:
            data_source = self.dataset
        
        # Initialize data source if needed
        if isinstance(data_source, str):
            from wonambi.dataset import Dataset
            data = Dataset(data_source)
        else:
            data = data_source
        
        def process_single_event(event):
            try:
                # Load data around event
                # Use peak_time if available, otherwise use start_time
                center_time = event.get('peak_time', event['start_time'])
                start = max(0, center_time - window_size/2)
                end = start + window_size
                
                # Get channel for this event, if specified
                channel = event.get('channel', None)
                channels = [channel] if channel else None
                
                # Read data
                event_data = data.read_data(start=start, end=end, chan=channels)
                
                # Apply custom function if provided
                result = {
                    'event_id': event.get('id', None),
                    'start_time': event['start_time'],
                    'end_time': event.get('end_time', None),
                    'channel': event.get('channel', None),
                    'data': event_data,
                }
                
                if func is not None:
                    result['analysis'] = func(event_data, event)
                    
                return result
            except Exception as e:
                print(f"Error processing event {event.get('id', 'unknown')}: {e}")
                return {
                    'event_id': event.get('id', None),
                    'start_time': event['start_time'],
                    'error': str(e)
                }
        
        # Process events in parallel
        results = []
        
        # Use single process for debugging if needed
        debug_mode = False
        if debug_mode:
            results = [process_single_event(event) for event in events]
        else:
            # Process events in parallel with progress reporting
            print(f"Processing {len(events)} events with {n_workers} workers")
            
            # Calculate chunk size for feedback
            chunk_size = max(10, len(events) // 20)  # Report after every 5% or 10 events, whichever is larger
            
            with ProcessPoolExecutor(max_workers=n_workers) as executor:
                future_to_idx = {executor.submit(process_single_event, event): i for i, event in enumerate(events)}
                
                completed = 0
                for future in as_completed(future_to_idx):
                    result = future.result()
                    results.append(result)
                    
                    completed += 1
                    if completed % chunk_size == 0 or completed == len(events):
                        print(f"Processed {completed}/{len(events)} events ({completed/len(events)*100:.1f}%)")
        
        return results
    
    def detect_spindles(self, method='Ferrarelli2007', chan=None, ref_chan=[], grp_name='eeg',
                       frequency=(11, 16), duration=(0.5, 3), polar='normal', 
                       reject_artifacts=True, reject_arousals=True,stage=None, cat=None,
                       save_to_annotations=False, json_dir=None):
        """
        Detect spindles in the dataset while considering artifacts and arousals.
        
        Parameters
        ----------
        method : str or list
            Detection method(s) to use ('Ferrarelli2007', 'Wamsley2012', etc.)
        chan : list or str
            Channels to analyze
        ref_chan : list or str
            Reference channel(s) for re-referencing, or None to use original reference
        grp_name : str
            Group name for channel selection
        frequency : tuple
            Frequency range for spindle detection (min, max)
        duration : tuple
            Duration range for spindle detection in seconds (min, max)
        polar : str
            'normal' or 'opposite' for handling signal polarity
        reject_artifacts : bool
            Whether to exclude segments marked with artifact annotations
        reject_arousals : bool
            Whether to exclude segments marked with arousal annotations
        json_dir : str or None
            Directory to save individual channel JSON files (one per channel)
        
        Returns
        -------
        list
            List of all detected spindles
        """

        
        print(r"""Whaling it... (searching for spindles)
                              .
                           ":"
                         ___:____     |"\/"|
                       ,'        `.    \  /
                       |  O        \___/  |
                     ~^~^~^~^~^~^~^~^~^~^~^~^~
                     """)
                     
        
        # Configure what to reject
        reject_types = []
        if reject_artifacts:
            reject_types.append('Artefact')
        if reject_arousals:
            reject_types.extend(['Arousal'])

        # Make sure method is a list
        if isinstance(method, str):
            method = [method]
        
        # Make sure chan is a list
        if isinstance(chan, str):
            chan = [chan]
        
        # Make sure stage is a list
        if isinstance(stage, str):
            stage = [stage]
           # Create json_dir if specified
        if json_dir:
            os.makedirs(json_dir, exist_ok=True)
            print(f"Channel JSONs will be saved to: {json_dir}")
        
        # Verify that we have all required components
        if self.dataset is None:
            print("Error: No dataset provided for spindle detection")
            return []
        
        if self.annotations is None and save_to_annotations:
            print("Warning: No annotations provided but annotation saving requested.")
            print("Spindles will not be saved to annotations.")
            save_to_annotations = False

        # Convert method to string
        method_str = "_".join(method) if isinstance(method, list) else str(method)
        
        # Convert frequency to string
        freq_str = f"{frequency[0]}-{frequency[1]}Hz"

        # Create a custom annotation file name if saving to annotations
        if save_to_annotations:
            # Convert channel list to string
            chan_str = "_".join(chan) if len(chan) <= 3 else f"{chan[0]}_plus_{len(chan)-1}_chans"
            
            
            # Create custom filename
            annotation_filename = f"spindles_{method_str}_{chan_str}_{freq_str}.xml"
             # Create full path if json_dir is specified
            if json_dir:
                annotation_file_path = os.path.join(json_dir, annotation_filename)
            else:
                # Use current directory
                annotation_file_path = annotation_filename
                
            # Create new annotation object if we're saving to a new file
            if self.annotations is not None:
                try:
                    # Create a copy of the original annota
                    import shutil
                    if hasattr(self.annotations, 'xml_file') and os.path.exists(self.annotations.xml_file):
                        shutil.copy(self.annotations.xml_file, annotation_file_path)
                        new_annotations = Annotations(annotation_file_path)
                        try:
                            spindle_events = new_annotations.get_events('spindle')
                            if spindle_events:
                                print(f"Removing {len(spindle_events)} existing spindle events")
                                new_annotations.remove_event_type('spindle')
                        except Exception as e:
                            print(f"Note: No existing spindle events to remove: {e}")
                    else:
                        # If we can't copy, create a new annotations file from scratch
                        # Create minimal XML structure
                        with open(annotation_file_path, 'w') as f:
                            f.write('<?xml version="1.0" ?>\n<annotations><dataset><filename>')
                            if hasattr(self.dataset, 'filename'):
                                f.write(self.dataset.filename)
                            f.write('</filename></dataset><rater><name>Wonambi</name></rater></annotations>')
                        new_annotations = Annotations(annotation_file_path)
                    print(f"Will save spindles to new annotation file: {annotation_file_path}")    

                except Exception as e:
                    print(f"Error creating new annotation file: {e}")
                    save_to_annotations = False
                    new_annotations = None
            else:
                print("Warning: No annotations provided but annotation saving requested.")
                print("Spindles will not be saved to annotations.")
                save_to_annotations = False
                new_annotations = None

        # Store all detected spindles
        all_spindles = []

        for ch in chan:
                try:
                    print(f'Reading data for channel {ch}')
                    
                    # Fetch segments, filtering based on stage and artifacts
                    segments = fetch(self.dataset, self.annotations, cat=cat, stage=stage, cycle=None, 
                                    reject_epoch=True, reject_artf=reject_types)
                    segments.read_data(ch, ref_chan, grp_name=grp_name)

                    
                    # Process each detection method
                    channel_spindles = []
                    channel_json_spindles = []
                    ## Loop through methods (i.e. WHALE IT!)
                    for m, meth in enumerate(method):
                        print(f"Applying method: {meth}")
                        ### define detection
                        detection = DetectSpindle(meth, frequency=frequency, duration=duration)
                            
                        for i, seg in enumerate(segments):
                            print(f'Detecting events, segment {i + 1} of {len(segments)}')

                            # Apply polarity adjustment if needed
                            if polar == 'normal':
                                pass # No change needed
                            elif polar == 'opposite':
                                seg['data'].data[0][0] = seg['data'].data[0][0]*-1
                            # Run detection
                            spindles = detection(seg['data'])

                            if spindles and save_to_annotations and new_annotations is not None:
                                spindles.to_annot(new_annotations, 'spindle')
                            
                            # Add to our results
                            # Convert to dictionary format for consistency
                            for sp in spindles:
                                # Add channel information
                                sp['chan'] = ch
                                channel_spindles.append(sp)
                                
                                # Add to JSON 
                                if json_dir:
                                    # Extract key properties in a serializable format
                                    sp_data = {
                                        'chan': ch,
                                        'start time': float(sp.get('start', 0)),
                                        'end time': float(sp.get('end', 0)),
                                        'peak_time': float(sp.get('peak_time', 0)),
                                        'duration': float(sp.get('dur', 0)),
                                        'ptp_det': float(sp.get('ptp_det', 0)),
                                        'method': meth
                                    }
                                    
                                    sp_data['stage'] = stage
                                    sp_data['freq_range'] = frequency
                                    # Add frequency/power/amplitude if available
                                    if 'peak_freq' in sp:
                                        sp_data['peak_freq'] = float(sp['peak_freq'])
                                    if 'peak_val' in sp:
                                        sp_data['peak_val'] = float(sp['peak_val'])
                                    if 'power' in sp:
                                        sp_data['power'] = float(sp['power'])
                                        
                                    channel_json_spindles.append(sp_data)
                    all_spindles.extend(channel_spindles)
                    print(f"Found {len(channel_spindles)} spindles in channel {ch}")

                    if json_dir and channel_json_spindles:
                        try:
                            ch_json_file = os.path.join(json_dir, f"spindles_{method_str}_{freq_str}_{ch}.json")

                            with open(ch_json_file, 'w') as f:
                                json.dump(channel_json_spindles, f, indent=2)
                            print(f"Saved spindle data for channel {ch} to {ch_json_file}")
                        except Exception as e:
                            print(f"Error saving channel JSON: {e}")
                except Exception as e:        
                        print(f'WARNING: No spin channel {ch}: {e}')
        
        # Save the new annotation file if needed
        if save_to_annotations and new_annotations is not None and all_spindles:
            try:
                new_annotations.save(annotation_file_path)
                print(f"Saved {len(all_spindles)} spindles to new annotation file: {annotation_file_path}")
            except Exception as e:
                print(f"Error saving annotation file: {e}")



        # Return all detected spindles
        print(f"Total spindles detected across all channels: {len(all_spindles)}")
        return all_spindles
 
   
    def detect_spindles_multichannel(self, method='Ferrarelli2007', channels=None,
                               frequency=(11, 16), duration=(0.5, 3), polar='normal',
                               reject_artifacts=True, reject_arousals=True,
                               n_workers=None, chunk_size=10, stage=['NREM2'], cat=(1, 1, 1, 0)):
        """
        Detect spindles across multiple channels using parallel processing.
        
        Parameters
        ----------
        method : str or list
            Detection method(s) to use ('Ferrarelli2007', 'Wamsley2012', etc.)
        channels : list or None
            Channels to analyze. If None, uses all available channels.
        frequency : tuple
            Frequency range for spindle detection (min, max)
        duration : tuple
            Duration range for spindle detection in seconds (min, max)
        polar : str
            'normal' or 'opposite' for handling signal polarity
        reject_artifacts : bool
            Whether to exclude segments marked with artifact annotations
        reject_arousals : bool
            Whether to exclude segments marked with arousal annotations
        n_workers : int or None
            Number of workers for parallel processing. If None, uses CPU count - 1.
        chunk_size : int
            Number of channels to process in each parallel batch
        stage : list
            Sleep stages to include in analysis (default: ['NREM2'])
        cat : tuple
            Concatenation settings (cycle, stage, discontinuous, event) where:
            0 means no concatenation, 1 means concatenation
        
        Returns
        -------
        dict
            Results organized by channel with all detected spindles
        """
        # If n_workers not specified, use CPU count - 1 (leave one for system)
        if n_workers is None:
            n_workers = max(1, multiprocessing.cpu_count() - 1)
        
        # Get all available channels if not specified
        if channels is None:
            if hasattr(self.dataset, 'header') and 'chan_name' in self.dataset.header:
                channels = self.dataset.header['chan_name']
            else:
                raise ValueError("No channels specified and couldn't extract channel names from dataset")
        
        # Ensure channels is a list
        if isinstance(channels, str):
            channels = [channels]
        
        print(f"Processing {len(channels)} channels with {n_workers} workers")
        start_time = time.time()
        
        # Split channels into chunks for parallel processing
        channel_chunks = [channels[i:i+chunk_size] for i in range(0, len(channels), chunk_size)]
        
        # Process channel chunks in parallel
        all_results = {}
        
        with ProcessPoolExecutor(max_workers=n_workers) as executor:
        # Pass all the parameters explicitly when submitting the function
            futures = [executor.submit(
                self.process_channel_chunk, 
                chunk, 
                method, 
                frequency, 
                duration, 
                polar, 
                reject_artifacts, 
                reject_arousals,
                stage,
                cat
            ) for chunk in channel_chunks]
        
        # Collect results as they complete
        for i, future in enumerate(futures):
            try:
                chunk_results = future.result()
                all_results.update(chunk_results)
                print(f"Completed chunk {i+1}/{len(channel_chunks)}")
            except Exception as e:
                print(f"Error in chunk {i+1}: {e}")
                import traceback
                traceback.print_exc()

        # Calculate summary statistics
        total_spindles = sum(len(spindles) for spindles in all_results.values())
        spindles_by_channel = {chan: len(spindles) for chan, spindles in all_results.items()}
        
        # Sort channels by number of spindles (descending)
        sorted_channels = sorted(spindles_by_channel.items(), key=lambda x: x[1], reverse=True)
        
        # Print summary
        print(f"\nSpindle detection complete in {time.time() - start_time:.2f} seconds")
        print(f"Total spindles detected: {total_spindles}")
        print("\nTop 10 channels by spindle count:")
        for chan, count in sorted_channels[:10]:
            print(f"  {chan}: {count}")
        
        return {
            'spindles': all_results,
            'total': total_spindles,
            'by_channel': spindles_by_channel
        }
    
    def process_channel_chunk(self, channel_chunk, method, frequency, duration, polar, reject_artifacts, 
                              reject_arousals,stage=['NREM2'], cat=(1, 1, 1, 0)):
        """
        Process a chunk of channels for spindle detection.
        
        Parameters
        ----------
        channel_chunk : list
            List of channel names to process
        method : str or list
            Detection method(s) to use
        frequency : tuple
            Frequency range for spindle detection
        duration : tuple
            Duration range for spindle detection
        polar : str
            Signal polarity setting
        reject_artifacts : bool
            Whether to exclude segments marked with artifact annotations
        reject_arousals : bool
            Whether to exclude segments marked with arousal annotations
        stage : list
            Sleep stages to include in analysis (default: ['NREM2'])
        cat : tuple
            Concatenation settings (cycle, stage, discontinuous, event)
            
        Returns
        -------
        dict
            Results for each channel
        """
        results = {}
        for channel in channel_chunk:
            try:
                # Use detect_spindles to detect spindles for this channel
                spindles = self.detect_spindles(
                    method=method,
                    chan=[channel],
                    frequency=frequency,
                    duration=duration,
                    polar=polar,
                    reject_artifacts=reject_artifacts,
                    reject_arousals=reject_arousals,
                    stage=stage,
                    cat=cat
                )
                
                results[channel] = spindles
            except Exception as e:
                print(f"Error processing channel {channel}: {e}")
                results[channel] = []
        
        return results
    
    def analyze_spindles(self, spindle_results, window_size=5, n_workers=None, 
                        analysis_func=None, max_spindles=None):
        """
        Perform advanced analysis on detected spindles across multiple channels.
        
        Parameters
        ----------
        spindle_results : dict
            Results from detect_spindles_multichannel
        window_size : float
            Window size around each spindle for analysis (seconds)
        n_workers : int or None
            Number of workers for parallel processing. If None, uses CPU count - 1.
        analysis_func : callable or None
            Function to apply to each spindle's data
        max_spindles : int or None
            Maximum number of spindles to analyze (for very large datasets)
        
        Returns
        -------
        dict
            Advanced analysis results
        """
        # If n_workers not specified, use CPU count - 1 (leave one for system)
        if n_workers is None:
            n_workers = max(1, multiprocessing.cpu_count() - 1)
        
        start_time = time.time()
        
        # Create a flat list of all spindles with channel information
        all_spindles = []
        for channel, spindles in spindle_results['spindles'].items():
            for i, spindle in enumerate(spindles):
                # Create event dictionary
                event = {
                    'id': f"{channel}_{i}",
                    'start_time': spindle.get('start', 0),
                    'end_time': spindle.get('end', 0),
                    'channel': channel,
                    'peak_time': (spindle.get('start', 0) + spindle.get('end', 0)) / 2,
                    'spindle_data': spindle  # Store original spindle info
                }
                all_spindles.append(event)
        
        # Limit number of spindles if specified
        if max_spindles and len(all_spindles) > max_spindles:
            print(f"Limiting analysis to {max_spindles} spindles out of {len(all_spindles)}")
            # Randomly sample spindles to ensure representation across channels
            import random
            random.shuffle(all_spindles)
            all_spindles = all_spindles[:max_spindles]
        
        print(f"Analyzing {len(all_spindles)} spindles with {n_workers} workers")
        
        # Define a default analysis function if none provided
        if analysis_func is None:
            def default_analysis(data, event):
                """
                Default analysis computes basic spindle metrics.
                """
                try:
                    # Calculate spindle power
                    from scipy import signal
                    from scipy.fft import fft
                    
                    # Get data array (assuming data object has a .data attribute)
                    if hasattr(data, 'data'):
                        signal_data = data.data
                    else:
                        signal_data = data
                    
                    # Extract channel data based on the spindle's channel
                    channel_idx = None
                    if hasattr(data, 'chan'):
                        try:
                            channel_idx = data.chan.index(event['channel'])
                        except:
                            pass
                    
                    if channel_idx is not None:
                        signal_data = signal_data[channel_idx]
                    
                    # Calculate metrics
                    # 1. Signal amplitude
                    amplitude = np.max(np.abs(signal_data)) if len(signal_data) > 0 else 0
                    
                    # 2. Spindle duration
                    duration = event['end_time'] - event['start_time']
                    
                    # 3. Estimate spindle frequency using FFT
                    frequency = np.nan
                    if len(signal_data) > 0 and hasattr(data, 's_freq'):
                        try:
                            # Apply bandpass filter to isolate spindle frequencies
                            from scipy.signal import butter, filtfilt, periodogram
                            def butter_bandpass(lowcut, highcut, fs, order=5):
                                nyq = 0.5 * fs
                                low = lowcut / nyq
                                high = highcut / nyq
                                b, a = butter(order, [low, high], btype='band')
                                return b, a
                            
                            # Get sampling rate
                            fs = data.s_freq
                            
                            # Get spindle-specific data
                            s_start = event['start_time'] - data.start
                            s_end = event['end_time'] - data.start
                            if s_start < 0: s_start = 0
                            if s_end > len(signal_data) / fs: s_end = len(signal_data) / fs
                            
                            # Calculate indices
                            idx_start = int(s_start * fs)
                            idx_end = int(s_end * fs)
                            
                            # Extract spindle segment
                            if idx_end > idx_start:
                                spindle_segment = signal_data[idx_start:idx_end]
                                
                                # Calculate periodogram
                                f, psd = periodogram(spindle_segment, fs)
                                
                                # Find frequency with maximum power in spindle range
                                spindle_range = (9, 16)  # broader range to catch various spindle types
                                spindle_indices = np.where((f >= spindle_range[0]) & (f <= spindle_range[1]))[0]
                                
                                if len(spindle_indices) > 0:
                                    # Find peak frequency within spindle range
                                    max_idx = spindle_indices[np.argmax(psd[spindle_indices])]
                                    frequency = f[max_idx]
                                    
                                    # Also calculate power
                                    power = np.sum(psd[spindle_indices])
                                else:
                                    frequency = np.nan
                                    power = 0
                            else:
                                frequency = np.nan
                                power = 0
                            
                            return {
                                'amplitude': float(amplitude),
                                'duration': float(duration),
                                'frequency': float(frequency) if not np.isnan(frequency) else None,
                                'power': float(power),
                            }
                        except Exception as e:
                            print(f"Error in frequency analysis: {e}")
                    
                    return {
                        'amplitude': float(amplitude),
                        'duration': float(duration),
                        'frequency': None,
                        'power': None,
                    }
                except Exception as e:
                    print(f"Error in default analysis: {e}")
                    return {'error': str(e)}
            
            analysis_func = default_analysis
        
        # Process spindles in parallel
        analyzed_spindles = self.process_events_parallel(
            events=all_spindles,
            data_source=self.dataset,
            window_size=window_size,
            n_workers=n_workers,
            func=analysis_func
        )
        
        # Organize results by channel
        results_by_channel = {}
        analysis_by_channel = {}
        
        for result in analyzed_spindles:
            channel = result.get('channel', 'unknown')
            
            if channel not in results_by_channel:
                results_by_channel[channel] = []
                analysis_by_channel[channel] = {
                    'count': 0,
                    'amplitude': [],
                    'duration': [],
                    'frequency': [],
                    'power': []
                }
            
            results_by_channel[channel].append(result)
            
            # Extract analysis results
            if 'analysis' in result:
                analysis = result['analysis']
                analysis_by_channel[channel]['count'] += 1
                
                if 'amplitude' in analysis and analysis['amplitude'] is not None:
                    analysis_by_channel[channel]['amplitude'].append(analysis['amplitude'])
                if 'duration' in analysis and analysis['duration'] is not None:
                    analysis_by_channel[channel]['duration'].append(analysis['duration'])
                if 'frequency' in analysis and analysis['frequency'] is not None:
                    analysis_by_channel[channel]['frequency'].append(analysis['frequency'])
                if 'power' in analysis and analysis['power'] is not None:
                    analysis_by_channel[channel]['power'].append(analysis['power'])
        
        # Calculate channel statistics
        for channel in analysis_by_channel:
            stats = analysis_by_channel[channel]
            
            # For each metric, calculate mean, median, std
            for metric in ['amplitude', 'duration', 'frequency', 'power']:
                values = stats[metric]
                if values:
                    stats[f'{metric}_mean'] = float(np.mean(values))
                    stats[f'{metric}_median'] = float(np.median(values))
                    stats[f'{metric}_std'] = float(np.std(values))
                    stats[f'{metric}_min'] = float(np.min(values))
                    stats[f'{metric}_max'] = float(np.max(values))
                else:
                    stats[f'{metric}_mean'] = None
                    stats[f'{metric}_median'] = None
                    stats[f'{metric}_std'] = None
                    stats[f'{metric}_min'] = None
                    stats[f'{metric}_max'] = None
        
        # Calculate overall statistics
        all_amplitude = []
        all_duration = []
        all_frequency = []
        all_power = []
        
        for channel in analysis_by_channel:
            stats = analysis_by_channel[channel]
            all_amplitude.extend(stats['amplitude'])
            all_duration.extend(stats['duration'])
            all_frequency.extend(stats['frequency'])
            all_power.extend(stats['power'])
        
        overall_stats = {
            'total_spindles': len(all_spindles),
            'analyzed_spindles': len(analyzed_spindles),
            'runtime_seconds': time.time() - start_time
        }
        
        # Calculate overall metrics
        if all_amplitude:
            overall_stats['amplitude_mean'] = float(np.mean(all_amplitude))
            overall_stats['amplitude_std'] = float(np.std(all_amplitude))
        if all_duration:
            overall_stats['duration_mean'] = float(np.mean(all_duration))
            overall_stats['duration_std'] = float(np.std(all_duration))
        if all_frequency:
            overall_stats['frequency_mean'] = float(np.mean(all_frequency))
            overall_stats['frequency_std'] = float(np.std(all_frequency))
        if all_power:
            overall_stats['power_mean'] = float(np.mean(all_power))
            overall_stats['power_std'] = float(np.std(all_power))
        
        print(f"\nAnalysis complete in {overall_stats['runtime_seconds']:.2f} seconds")
        if all_frequency:
            print(f"Overall spindle frequency: {overall_stats['frequency_mean']:.2f} ± {overall_stats['frequency_std']:.2f} Hz")
        if all_duration:
            print(f"Overall spindle duration: {overall_stats['duration_mean']*1000:.0f} ± {overall_stats['duration_std']*1000:.0f} ms")
        
        return {
            'results': results_by_channel,
            'analysis': analysis_by_channel,
            'overall': overall_stats
        }
    
    def export_spindle_parameters_to_csv(self, json_input, csv_file, export_params='all', 
                              frequency=None, ref_chan=None, grp_name='eeg', n_fft_sec=4):
        """
        Calculate spindle parameters from JSON files and export to CSV.
        
        Parameters
        ----------
        json_input : str or list
            Path to JSON file, directory of JSON files, or list of JSON files
        csv_file : str
            Path to output CSV file
        export_params : dict or str
            Parameters to export. If 'all', exports all available parameters
        frequency : tuple or None
            Frequency range for power calculations (default: None, uses original range from JSON)
        ref_chan : list or None
            Reference channel(s) to use for parameter calculation
        grp_name : str
            Group name for channel selection
            
        Returns
        -------
        dict
            Dictionary of calculated parameters
        """
        from wonambi.trans.analyze import event_params, export_event_params
        import glob
        
        print("Calculating spindle parameters for CSV export...")
        
        # Determine input files
        json_files = []
        if isinstance(json_input, str):
            if os.path.isdir(json_input):
                json_files = glob.glob(os.path.join(json_input, "*.json"))
            elif os.path.isfile(json_input):
                json_files = [json_input]
        elif isinstance(json_input, list):
            json_files = json_input
        
        if not json_files:
            print(f"No JSON files found at {json_input}")
            return None
        
        print(f"Found {len(json_files)} JSON files to process")
        
        # Load spindles from JSON files
        all_spindles = []
        for file in json_files:
            try:
                with open(file, 'r') as f:
                    spindles = json.load(f)
                    
                if isinstance(spindles, list):
                    all_spindles.extend(spindles)
                else:
                    print(f"Warning: Unexpected format in {file}")
                    
                print(f"Loaded {len(spindles) if isinstance(spindles, list) else 0} spindles from {file}")
            except Exception as e:
                print(f"Error loading {file}: {e}")
        
        if not all_spindles:
            print("No spindles found in the input files")
            return None
        
        print(f"Total of {len(all_spindles)} spindles loaded")
        
        # Get frequency band from spindles if not provided
        if frequency is None:
            try:
                # Try to extract from the first spindle
                if 'freq_range' in all_spindles[0]:
                    freq_str = all_spindles[0]['freq_range']
                    if '-' in freq_str:
                        freq_parts = freq_str.split('-')
                        frequency = (float(freq_parts[0]), float(freq_parts[1]))
                        print(f"Using frequency range from JSON: {frequency}")
            except:
                # Default if we can't extract
                frequency = (11, 16)
                print(f"Using default frequency range: {frequency}")
        

            # Get sampling frequency from dataset
        try:
            s_freq = self.dataset.header['s_freq']
            #print(f"Dataset sampling frequency: {s_freq} Hz")
        except:
            print("Could not determine dataset sampling frequency")
        
        # Try to get recording start time if not provided
        recording_start_time = None
        try:
            # Get it from dataset header
            if hasattr(self.dataset, 'header'):
                header = self.dataset.header
                if hasattr(header, 'start_time'):
                    recording_start_time = header.start_time
                elif hasattr(header, 'recordings') and header.recordings:
                    if hasattr(header.recordings[0], 'start_time'):
                        recording_start_time = header.recordings[0].start_time
                    elif isinstance(header.recordings[0], dict) and 'start_time' in header.recordings[0]:
                        recording_start_time = header.recordings[0]['start_time']
                elif isinstance(header, dict) and 'start_time' in header:
                    recording_start_time = header['start_time']
                    
            if recording_start_time:
                print(f"Found recording start time: {recording_start_time}")
            else:
                print("Warning: Could not find recording start time in dataset header. Using relative time only.")
        except Exception as e:
            print(f"Error getting recording start time: {e}")
            print("Using relative time only.")




        # Create segments for parameter calculation
        spindle_segments = []
        
        # Group spindles by channel
        spindles_by_chan = {}
        for sp in all_spindles:
            chan = sp.get('chan')
            if chan not in spindles_by_chan:
                spindles_by_chan[chan] = []
            spindles_by_chan[chan].append(sp)
        
        # Load data for each channel and create segments
        for chan, spindles in spindles_by_chan.items():
            try:
                print(f"Processing {len(spindles)} spindles for channel {chan}")
                
                # For each spindle, create a segment with the data
                for sp in spindles:
                    try:
                        # Get timing information
                        start_time = sp['start time']
                        end_time = sp['end time']
                        
                        # def sec_to_time(seconds):
                        #     hours = int(seconds // 3600)
                        #     minutes = int((seconds % 3600) // 60)
                        #     seconds = seconds % 60
                        #     return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"
                    
                        # start_time_hms = sec_to_time(start_time)
                    

                        # Fetch the data from the dataset
                        #beg_sample = int(start_time * s_freq)
                        #end_sample = int(end_time * s_freq)
                        data = self.dataset.read_data(chan=[chan], 
                                                      begtime=start_time, 
                                                      endtime=end_time)

                        seg = {
                            'data': data,
                            'name': 'spindle',
                            'start': start_time,
                            'end': end_time,
                            'n_stitch': 1,
                            'stage': sp.get('stage'),
                            'cycle': None
                        }
                        spindle_segments.append(seg)
               
                            
                    except Exception as e:
                        print(f"Error creating segment for spindle {start_time}-{end_time}: {e}")
            except Exception as e:
                print(f"Error processing channel {chan}: {e}")
        
        if not spindle_segments:
            print("No valid segments created for parameter calculation")
            return None
        
        print(f"Created {len(spindle_segments)} segments for parameter calculation")
        
        # Calculate parameters
        n_fft = None
        if spindle_segments and n_fft_sec is not None:
            n_fft = int(n_fft_sec * s_freq)                
        try:
            params = event_params(spindle_segments, export_params, band=frequency, n_fft=n_fft)
            
            
            # Export parameters to temporary CSV file
            print(f"Exporting parameters to temporary file")
            temp_csv = csv_file + '.temp'
            export_event_params(temp_csv, params, count=None, density=None)
            # Now read the temporary CSV and add the HH:MM:SS column
            print(f"Adding HH:MM:SS format to CSV")
            with open(temp_csv, 'r', newline='') as infile, open(csv_file, 'w', newline='') as outfile:
                reader = csv.reader(infile)
                writer = csv.writer(outfile)
                # Process the header rows
                header_processed = False
                data_rows_started = False
                start_time_index = None
                
                # Read all rows into memory to process them
                all_rows = list(reader)
                # First pass: Find the header row with 'Start time' and determine column index
                for i, row in enumerate(all_rows):
                    if row and any(x == 'Start time' for x in row):
                        header_found = True
                        # Find the index of 'Start time'
                        for j, col in enumerate(row):
                            if col == 'Start time':
                                start_time_index = j
                                break
                        break

                if not header_found or start_time_index is None:
                    print("Error: Could not find 'Start time' column in CSV")
                    # Copy the original file as fallback
                    with open(temp_csv, 'r') as src, open(csv_file, 'w') as dst:
                        dst.write(src.read())
                    return params
                # Second pass: Process and write rows
                for i, row in enumerate(all_rows):
                    if i == 0 and header_found:
                        # This is the header row with column names
                        # Insert HH:MM:SS column after Start time
                        row.insert(start_time_index + 1, 'Start time (HH:MM:SS)')
                        writer.writerow(row)
                    elif header_found and not data_rows_started:
                        # These are the summary statistics rows (Mean, SD, etc.)
                        # Check if this is a row with a numeric Start time (actual data row)
                        if row and len(row) > start_time_index:
                            try:
                                # Try to convert the Start time to a float
                                float(row[start_time_index])
                                # If successful, this is the first data row
                                data_rows_started = True 
                                try:
                                    start_time_sec = float(row[start_time_index])
                                    def sec_to_time(seconds):
                                        hours = int(seconds // 3600)
                                        minutes = int((seconds % 3600) // 60)
                                        seconds = seconds % 60
                                        return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"
                                
                                    if recording_start_time is not None:
                                        try:
                                            # Calculate seconds into delta
                                            delta = datetime.timedelta(seconds=start_time_sec)
                                            # Add to recording start time
                                            event_time = recording_start_time + delta
                                            # Format as HH:MM:SS.mmm (just time, no date)
                                            start_time_hms = event_time.strftime('%H:%M:%S.%f')[:-3]
                                        except:
                                            # Fall back to relative time if calculation fails
                                            start_time_hms = sec_to_time(start_time_sec)
                                    else:
                                        # Use relative time format
                                        start_time_hms = sec_to_time(start_time_sec)
                                    
                                    # Insert the HH:MM:SS time after the original Start time
                                    row.insert(start_time_index + 1, start_time_hms)
                                except (ValueError, IndexError):
                                    # If we can't convert the start time, insert empty string
                                    row.insert(start_time_index + 1, '')

                                writer.writerow(row)    
                            except (ValueError, IndexError):
                                    # If we can't convert the start time, insert empty string
                                row.insert(start_time_index + 1, '')
                                writer.writerow(row)
                        else:
                            # This is a summary row with empty/non-numeric Start time
                            row.insert(start_time_index + 1, '')
                            writer.writerow(row)
                    elif data_rows_started:
                        # This is a standard data row
                        try:
                            start_time_sec = float(row[start_time_index])

                            # Convert to HH:MM:SS
                            def sec_to_time(seconds):
                                hours = int(seconds // 3600)
                                minutes = int((seconds % 3600) // 60)
                                sec = seconds % 60
                                return f"{hours:02d}:{minutes:02d}:{sec:06.3f}"
                            # Calculate clock time if recording start time is available
                            if recording_start_time is not None:
                                try:
                                    delta = datetime.timedelta(seconds=start_time_sec)
                                    event_time = recording_start_time + delta
                                    start_time_hms = event_time.strftime('%H:%M:%S.%f')[:-3]
                                except:
                                    start_time_hms = sec_to_time(start_time_sec)
                            else:
                                start_time_hms = sec_to_time(start_time_sec)
                            
                            # Insert the HH:MM:SS time
                            row.insert(start_time_index + 1, start_time_hms)
                        except (ValueError, IndexError):
                            row.insert(start_time_index + 1, '')
                        
                        writer.writerow(row)
                    else:
                        # These are rows before the header row - skip them
                        pass

            # Close the files
            # Remove the temporary file
            try:
                os.remove(temp_csv)
            except:
                print(f"Note: Could not remove temporary file {temp_csv}")

            print(f"Successfully exported to {csv_file} with HH:MM:SS time format")          
            return params
        except Exception as e:
            print(f"Error calculating parameters: {e}")
            import traceback
            traceback.print_exc()
            return None

    
    def export_spindle_density_to_csv(self, json_input, csv_file, stage=None):
        """
        Export spindle statistics to CSV with both whole night and stage-specific densities.
        
        Parameters
        ----------
        json_input : str or list
            Path to JSON file, directory of JSON files, or list of JSON files
        csv_file : str
            Path to output CSV file
        stage : str or list
            Sleep stage(s) to include (e.g., 'NREM2', ['NREM2', 'NREM3'])
        time_window : int
            Window size in seconds for density calculation
            
        Returns
        -------
        dict
            Dictionary with spindle statistics by channel
        """
        import os
        import json
        import glob
        import csv
        import numpy as np
        from collections import defaultdict
        
        # Load spindles from JSON file(s)
        json_files = []
        if isinstance(json_input, str):
            if os.path.isdir(json_input):
                json_files = glob.glob(os.path.join(json_input, "*.json"))
            elif os.path.isfile(json_input):
                json_files = [json_input]
        elif isinstance(json_input, list):
            json_files = json_input
        

        #Prepare the stages as a list
        if stage is None:
            stage_list = None
        elif isinstance(stage, str):
            stage_list = [stage]
        else:
            stage_list = stage

        if stage_list:
            print(f"Calculating spindle density for stages: {', '.join(stage_list)}")
        else:
            print("Calculating spindle density for all stages")


        all_spindles = []
        for file in json_files:
            try:
                with open(file, 'r') as f:
                    spindles = json.load(f)
                    all_spindles.extend(spindles if isinstance(spindles, list) else [])
            except Exception as e:
                print(f"Error loading {file}: {e}")
        
        # Get stage durations from annotations (assuming annotations are available)
        epoch_duration_sec = 30  # Standard epoch duration
        
        # Count epochs for each stage
        stage_counts = defaultdict(int)
        for s in self.annotations.get_stages():
            if s in ['Wake', 'NREM1', 'NREM2', 'NREM3', 'REM']:
                stage_counts[s] += 1
        
        # Calculate durations in minutes
        stage_durations = {stg: count * epoch_duration_sec / 60 for stg, count in stage_counts.items()}
        total_duration_min = sum(stage_durations.values())
        

        # Extract stages from spindles if stage is None
        spindle_stages = set()
        for sp in all_spindles:
            if isinstance(sp, dict) and 'stage' in sp:
                sp_stage = sp['stage']
                if isinstance(sp_stage, list) and len(sp_stage) > 0:
                    for s in sp_stage:
                        spindle_stages.add(s)
                else:
                    spindle_stages.add(str(sp_stage))
        
        # If stage is None, process all stages found in spindles
        # If stage is None, process all stages found in spindles
        if stage is None:
            stages_to_process = sorted(spindle_stages)
        elif isinstance(stage, list):
            stages_to_process = stage
        else:
            stages_to_process = [stage]

        # Group spindles by channel and stage
        spindles_by_chan_stage = defaultdict(lambda: defaultdict(list))

        for sp in all_spindles:
            # Get channel information
            chan = None
            if isinstance(sp, dict):
                if 'chan' in sp:
                    chan = sp['chan']
                elif 'channel' in sp:
                    chan = sp['channel']
                
            # Get stage information
            sp_stage = None
            if isinstance(sp, dict) and 'stage' in sp:
                if isinstance(sp['stage'], list):
                    if len(sp['stage']) > 0:
                        sp_stage = sp['stage'][0]
                else:
                    sp_stage = sp['stage']

            
            if chan and sp_stage:
               spindles_by_chan_stage[chan][sp_stage].append(sp)
        
        # Calculate statistics by channel for each stage
        stage_channel_stats = defaultdict(dict)
        
        for process_stage in stages_to_process:
            for chan in spindles_by_chan_stage:
                # Get spindles for this channel and stage
                stage_spindles = spindles_by_chan_stage[chan].get(process_stage, [])
                
                # Get all spindles for this channel (for whole night density)
                all_chan_spindles = []
                for stg in spindles_by_chan_stage[chan]:
                    all_chan_spindles.extend(spindles_by_chan_stage[chan][stg])
                
                # Count spindles
                stage_count = len(stage_spindles)
                
                # Skip if no spindles for this stage and channel
                if stage_count == 0:
                    continue
                    
                # Calculate density (spindles per minute)
                if isinstance(process_stage, list):
                    # For combined stages, sum up the durations
                    combined_duration_min = sum(stage_durations.get(s, 0) for s in process_stage)
                    stage_duration_min = combined_duration_min
                    stage_name_display = "+".join(process_stage)  # For display purposes
                else:
                    stage_duration_min = stage_durations.get(process_stage, 0)
                    stage_name_display = process_stage

                stage_density = stage_count / stage_duration_min if stage_duration_min > 0 else 0
                whole_night_density = len(all_chan_spindles) / total_duration_min if total_duration_min > 0 else 0
                
                # Calculate mean duration
                durations = []
                for sp in stage_spindles:
                    durations.append(sp['end time'] - sp['start time'])
                        
                mean_duration = np.mean(durations) if durations else 0
                
                # Store the statistics
                stage_channel_stats[process_stage][chan] = {
                    'count': stage_count,
                    'stage_density': stage_density,
                    'whole_night_density': whole_night_density,
                    'mean_duration': mean_duration
                }
        
        # Export to CSV - each stage gets its own section
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Process each stage
            for process_stage in stages_to_process:
                # Skip if no data for this stage
                if not stage_channel_stats[process_stage]:
                    continue
                    
                # Add stage header
                stage_name_display = process_stage if isinstance(process_stage, str) else "+".join(process_stage)
                writer.writerow([f"Sleep Stage: {stage_name_display}"])
                writer.writerow(['Channel', 'Count', f'Density in {stage_name_display} (events/min)', 'Whole Night Density (events/min)', 'Mean Duration (s)'])
                
                # Write channel-specific statistics, sorted by channel name
                for chan in sorted(stage_channel_stats[process_stage].keys()):
                    stats = stage_channel_stats[process_stage][chan]
                    writer.writerow([
                        chan, 
                        stats['count'], 
                        f"{stats['stage_density']:.4f}",
                        f"{stats['whole_night_density']:.4f}", 
                        f"{stats['mean_duration']:.4f}"
                    ])
                
                # Add empty row between stages
                if len(stages_to_process) > 1:
                    writer.writerow([])
        
        print(f"Exported spindle statistics to {csv_file}")
        return dict(stage_channel_stats)