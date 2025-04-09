# Extract classical features from time series
#
# apr 2018, set 2019, dec 2023, Diego Cabrera, sbaltaz@ualg.pt, hdaniel@ualg.pt
# ago 2024 Parallelization, David Solís, dsolis@us.es
import logging
import time
import pywt
import numpy as np
import scipy.stats
import multiprocessing
import pandas as pd

logging.basicConfig(level=logging.INFO)

def signal2wpt_energy(signal, wavelet, max_level):
    """
        Computes the normalized energy coefficients of a signal at each node of a specified decomposition level
        in its Wavelet Packet Transform (WPT).

        Parameters:
        -----------
        signal : array-like
            The input signal to be analyzed, a 1D array.
        wavelet : str or pywt.Wavelet
            The wavelet to use for the wavelet packet decomposition. Can be a string name of a wavelet
            (e.g., 'db1' for Daubechies 1) or a `pywt.Wavelet` object.
        max_level : int
            The maximum level of decomposition in the wavelet packet transform. Higher levels give finer frequency
            resolution.

        Returns:
        --------
        energy_coef : ndarray
            A 1D array of normalized energy coefficients, where each element represents the energy at a specific
            node at `max_level` in the wavelet packet tree. The energy is calculated as the root mean square
            (RMS) of the coefficients in each node at the `max_level`.

        Example:
        --------
        To compute the energy coefficients of a signal `sig` using the 'db1' wavelet at level 3:
        ```python
        energy = signal2wp_energy(sig, 'db1', 3)
        ```

        Notes:
        ------
        - The energy of each node is normalized by the number of samples in the node to provide a consistent
          metric across nodes.
        - This function requires the PyWavelets (`pywt`) library to perform the wavelet packet transform.

    """
    wp_tree = pywt.WaveletPacket(data=signal, wavelet=wavelet, maxlevel=max_level)
    level = wp_tree.get_level(max_level, order='freq')
    energy_coef = np.zeros((len(level),))

    for i, node in enumerate(level):
        energy_coef[i] = np.sqrt(np.sum(node.data ** 2)) / node.data.shape[0]

    return energy_coef


def statistic_features(signal):
    """
       Computes a set of statistical features for a given signal, including measures of central tendency,
       spread, shape, and peaks.

       Parameters:
       -----------
       signal : array-like
           The input signal, typically a 1D array, for which statistical features are to be calculated.

       Returns:
       --------
       tuple
           A tuple containing the following statistical features of the signal:

           - `mean` (float): The mean (average) value of the signal.
           - `rms` (float): The root-mean-square (RMS) of the signal, a measure of the signal's power.
           - `std_dev` (float): The standard deviation of the signal, representing its spread.
           - `kurtosis` (float): The kurtosis of the signal, which measures the "tailedness" of the distribution.
             If the standard deviation is too low (≤ 0.01), this value is set to 0.
           - `peak` (float): The maximum value in the signal.
           - `crest` (float): The crest factor, calculated as `peak / rms`. If `rms` is 0, a small denominator is used.
           - `r_mean` (float): The rectified mean (mean of absolute values) of the signal.
           - `form` (float): The form factor, calculated as `rms / r_mean`. If `r_mean` is 0, a small denominator is used.
           - `impulse` (float): The impulse factor, calculated as `peak / r_mean`. If `r_mean` is 0, a small denominator is used.
           - `variance` (float): The variance of the signal, calculated as `std_dev ** 2`.
           - `minimum` (float): The minimum value in the signal.

       Example:
       --------
       To compute the statistical features of a signal `sig`:
       ```python
       features = statistic_features(sig)
       ```

       Notes:
       ------
       - The function handles cases where `rms` or `r_mean` are zero by using a very small denominator to avoid
         division by zero.
       - The `scipy.stats` library is required to calculate kurtosis.

    """
    mean = np.mean(signal)
    rms = np.sqrt(np.mean(np.square(signal)))
    std_dev = np.std(signal)
    if std_dev > 0.01:
        kurtosis = scipy.stats.kurtosis(signal)
    else:
        kurtosis = 0
    # kurtosis = scipy.stats.kurtosis(signal)[0]
    peak = np.max(signal)
    crest = peak / 1e-12 if rms == 0 else peak / rms
    r_mean = np.mean(np.abs(signal))
    form = rms / 1e-12 if r_mean == 0 else rms / r_mean
    impulse = peak / 1e-12 if r_mean == 0 else peak / r_mean
    variance = std_dev ** 2
    minimum = np.min(signal)

    return mean, rms, std_dev, kurtosis, peak, crest, r_mean, form, impulse, variance, minimum

def band_features(spectrum):
    """
        Computes a set of features for a given frequency spectrum, including measures of central tendency, power,
        and energy.

        Parameters:
        -----------
        spectrum : array-like
            The input frequency spectrum, typically a 1D array, for which features are to be calculated.

        Returns:
        --------
        tuple
            A tuple containing the following features of the frequency spectrum:

            - `mean` (float): The mean (average) value of the spectrum.
            - `rms` (float): The root-mean-square (RMS) of the spectrum, providing a measure of signal strength.
            - `peak` (float): The maximum value in the spectrum.
            - `power` (float): The average power of the spectrum, calculated as the mean of the squared spectrum.
            - `energy` (float): The total energy of the spectrum, calculated as the sum of the squared spectrum.

        Example:
        --------
        To compute the features of a spectrum `spec`:
        ```python
        features = band_features(spec)
        ```

        Notes:
        ------
        - The `spectrum` is expected to be a single-dimensional array representing the frequency components.
        - This function is suitable for analyzing the characteristics of signals in the frequency domain.

    """
    spectrumSQ = np.square(spectrum)
    mean = np.mean(spectrum)
    rms = np.sqrt(np.mean(spectrumSQ))
    peak = np.max(spectrum)
    power = np.mean(spectrumSQ)
    energy = np.sum(spectrumSQ)
    return mean, rms, peak, power, energy


def extractFeatures(signal, time=True, wavelets=True, frequency=True):
    """
        Extracts a comprehensive set of features from a given signal across different domains: time, frequency,
        and time-frequency (using wavelets). This feature set is useful for signal processing and pattern
        recognition tasks.

        Parameters:
        -----------
        signal : array-like
            The input signal, typically a 1D array, from which features will be extracted.
        time : bool, optional
            If `True`, extracts time-domain features using statistical descriptors (default is `True`).
        wavelets : bool, optional
            If `True`, extracts time-frequency features using wavelet packet transform energies (default is `True`).
        frequency : bool, optional
            If `True`, extracts frequency-domain features including power, peak, and band statistics (default is `True`).

        Returns:
        --------
        list
            A list of extracted features from the signal. The feature set will vary depending on which domains
            (`time`, `wavelets`, `frequency`) are enabled, and includes:

            - Time-domain features: Calculated using `statistic_features`, including metrics like mean, RMS,
              kurtosis, and more.
            - Frequency-domain features: Calculated using Fourier transform and band division, including metrics
              like mean, RMS, peak, power, and energy for each band.
            - Time-frequency features: Calculated using wavelet packet transform energies, with multiple wavelets
              (`'db7'`, `'sym3'`, `'coif4'`, `'bior6.8'`, `'rbio6.8'`) at a `max_level` of 6.

        Example:
        --------
        To extract features from a signal `sig` in all three domains:
        ```python
        features = extractFeatures(sig, time=True, wavelets=True, frequency=True)
        ```

        Notes:
        ------
        - The frequency-domain features include band-wise statistics, where the signal is divided into `n_band`
          bands of equal size.
        - Wavelet packet decomposition is performed using a list of wavelets, and features are extracted at
          each level up to `max_level`.

    """
    features = []

    # Time Features
    if time:
        time_features = statistic_features(signal)
        features.extend(time_features)

    # Frequency Features
    if frequency:
        freq_signal = np.abs(np.fft.rfft(signal))
        freq_features = statistic_features(freq_signal)
        features.extend(freq_features)

        # Frequency bands
        size_band = int(freq_signal.shape[0] / 89)
        if size_band > 0:
            i = 0
            while i + size_band <= freq_signal.shape[0]:
                band_freq_features = band_features(freq_signal[i:i + size_band])
                features.extend(band_freq_features)
                i += size_band

    # Time-frequency
    if wavelets:
        for i, wavelet in enumerate(['db7', 'sym3', 'coif4', 'bior6.8', 'rbio6.8']):
            wavelet_features = signal2wpt_energy(signal, wavelet, 6)
            features.extend(wavelet_features)

    return features


def __only_time_features(*data):
    return extractFeatures(data, wavelets=False, frequency=False)

def __all_features(*data):
    return extractFeatures(data)


def extract_features(X, feature_cols, jobs=4, prefix="F", frec_features=True):
    """
        Extracts features from specified columns in a dataset using multiprocessing, with options for
        time-domain or frequency-domain features. Adds the extracted features back to the dataset.

        Parameters:
        -----------
        X : pd.DataFrame
            Input DataFrame containing the data to process and extract features from.
        feature_cols : list of str
            List of column names in `X` containing the data for which features are to be extracted.
        jobs : int, optional
            Number of processes to use for multiprocessing (default is 4).
        prefix : str, optional
            Prefix for naming the extracted feature columns (default is "F").
        frec_features : bool, optional
            If `True`, extracts both frequency and time-domain features using `__all_features`.
            If `False`, extracts only time-domain features using `__only_time_features` (default is `True`).

        Returns:
        --------
        pd.DataFrame
            A new DataFrame containing the extracted features and the original non-feature columns.
            The extracted feature columns are prefixed with `prefix` and numbered sequentially.

        Example:
        --------
        To extract features from columns `['col1', 'col2']` in a DataFrame `df` using 4 jobs:
        ```python
        extracted_features_df = extract_features(df, feature_cols=['col1', 'col2'], jobs=4, prefix="F")
        ```

        Notes:
        ------
        - The function uses multiprocessing to parallelize feature extraction, which can significantly
          speed up the process for large datasets.
        - The selected function for feature extraction depends on `frec_features`, where `__all_features`
          includes both frequency and time features, while `__only_time_features` includes only time features.
        - The function logs the time taken for feature extraction.

    """
    start_time = time.time()

    with multiprocessing.Pool(processes=jobs) as pool:
        results = pool.starmap(__all_features if frec_features else __only_time_features,
                               X[feature_cols].values)

    Xf = np.array(list(results))

    Xf = pd.DataFrame(Xf)
    Xf.columns = [f"{prefix}{i}" for i in range(Xf.shape[1])]

    rest_cols = [c for c in X.columns if c not in feature_cols]
    for c in rest_cols:
        Xf[c] = X[c].values

    end_time = time.time()
    logging.info(f"Features extracted in {end_time - start_time} seconds")

    return Xf
