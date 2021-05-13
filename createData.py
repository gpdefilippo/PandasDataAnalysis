import pandas as pd
import numpy as np

def randomPercentage(length):
    rng = np.random.default_rng()
    percentage = rng.random(length)
    
    return(percentage)

def percentageWithRandom(mu, sigma, nums, numFalse):
    percentageArr = abs(np.random.normal(mu, sigma, nums))
    
    falsePercentage = np.random.normal((40-mu), sigma, numFalse)
    for falseCount in range(numFalse):
        index = np.random.randint(0, len(percentageArr))
        percentageArr[index] = falsePercentage[falseCount]
        
    return(percentageArr)

def generateFalseRate():
    falseRate = np.int64(np.ceil(np.random.normal(2, 1)))
    
    return(falseRate)

def negativeConcentration(quality):
    concentrations = np.array([None] * len(quality))
    concentrations[np.where(quality >= 0.88)] = percentageWithRandom(1, 4, np.count_nonzero(quality>0.88), generateFalseRate())
    
    concentrations[np.where((quality < 0.88) & (quality >= 0.44))] = percentageWithRandom(15, 5, 
                                                                    np.count_nonzero((quality < 0.88) & (quality >= 0.44)), 0)
    
    concentrations[np.where(quality < 0.44)] = percentageWithRandom(50, 10, np.count_nonzero(quality < 0.44),  0)
    
    return(concentrations)

def createDataFrame(numSamples):
    #falsePositive = generateFalseRate()
    #falseNegative = generateFalseRate()
    
    trials = np.linspace(1,numSamples, numSamples)
    quality_pct = randomPercentage(len(trials))
    negativeControl = negativeConcentration(quality_pct)
    
    rand_data = pd.DataFrame({"Trials":trials, "Quality": quality_pct,
                              "Negative_Control_Concentration":negativeControl})
    
    return(rand_data)
