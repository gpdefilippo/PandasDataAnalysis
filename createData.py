import pandas as pd
import numpy as np

def randomPercentage(length):
    rng = np.random.default_rng()
    percentage = rng.random(length)
    
    return(percentage)

def createDataFrame(numSamples):
    trials = np.linspace(1,numSamples, numSamples)
    quality_pct = randomPercentage(len(trials))
    
    rand_data = pd.DataFrame()