import os
import librosa
import numpy as np
import glob as glob

FRAME_SIZE = 1024
HOP_LENGTH = 512

def evalMfcc(fileName, n_mfcc = 13):
    raw, rate = librosa.load(fileName)
    mfcc = np.mean(librosa.feature.mfcc(y = raw, sr = rate, n_mfcc = n_mfcc).T, axis=0)
    return mfcc

def amplitudeEnvelope(fileName, frame_size, hop_length):
    amplitude_envelope = []
    signal, rate = librosa.load(fileName)
    
    for i in range(0, len(signal), hop_length):
        current_frame_amplitude_envelope = max(signal[i:i + frame_size])
        amplitude_envelope.append(current_frame_amplitude_envelope)
    
    return sum(amplitude_envelope) / len(amplitude_envelope)

def rms(fileName):
    signal, rate = librosa.load(fileName)
    rms = librosa.feature.rms(y = signal, frame_length = FRAME_SIZE, hop_length = HOP_LENGTH)[0]
    return sum(rms) / (rms.shape)[0]

def parseAudio(parentDirectory, genres, fileExtension = "*.wav", mfcc_coeff = 13):
    features, labels = np.empty((0, mfcc_coeff + 2)), np.empty(0)
    for subDir in genres:
        print("Processing directory:", subDir)
        for fn in glob.glob(os.path.join(parentDirectory, subDir, fileExtension)):
            mfcc = evalMfcc(fn, mfcc_coeff)
            ae = amplitudeEnvelope(fn, FRAME_SIZE, HOP_LENGTH)
            rms_val = rms(fn)
            mfcc = np.append(mfcc, ae)
            mfcc = np.append(mfcc, rms_val)
            tempFeatures = np.hstack(mfcc)
            features = np.vstack([features, tempFeatures])
            labels = np.append(labels, genres[subDir])
        print("Directory \"" + subDir + "\" completely Processed")

    return np.array(features), np.array(labels, dtype = int)