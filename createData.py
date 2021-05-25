import pandas as pd
import numpy as np

def randomPercentage(length):
    rng = np.random.default_rng()
    percentage = rng.random(length)
    
    return(percentage)

def percentageWithRandom(mu, sigma, nums, numPct):
    percentageArr = abs(np.random.normal(mu, sigma, nums))
    
    totalFalse = np.ceil(nums * numPct).astype(int)
    falsePercentage = abs(np.random.normal((40-mu), sigma, totalFalse))
    for falseCount in range(totalFalse):
        index = np.random.randint(0, len(percentageArr))
        percentageArr[index] = falsePercentage[falseCount]
        
    return(percentageArr)

def generateFalseRate():
    falseRate = np.int64(np.ceil(np.random.normal(2, 1)))/100
    
    return(falseRate)

def generateCondition(quality):
    conditionsArr = np.array([None] * len(quality))
    conditions = [1,2,3]
    
    iterations = np.floor(len(quality)/3).astype(int)
    for condition in conditions:
        NoneIndex = np.where(conditionsArr == None)[0]
        replacement = np.random.choice(NoneIndex, iterations, replace = False)
        
        conditionsArr[replacement] = condition
    
    #get leftovers when len(quality)%3 != 0
    conditionsArr[np.where(conditionsArr == None)[0]] = 1
    
    return(conditionsArr)

def generateIntensity(quality, ntc):
    quality_ntc = np.array([quality, ntc]).T
    
    intensity = np.array([None]*len(quality_ntc))
    
    intensity[np.where((quality_ntc[:,0] >= 0.88) & (quality_ntc[:,1] < 5))] = percentageWithRandom(100, 4, 
                                                                                                     np.count_nonzero((quality_ntc[:,0] >= 0.88) & (quality_ntc[:,1] < 5)), generateFalseRate())
    intensity[np.where((quality_ntc[:,0] >= 0.88) & (quality_ntc[:,1] >= 5))] = percentageWithRandom(130, 10, 
                                                                                                     np.count_nonzero((quality_ntc[:,0] >= 0.88) & (quality_ntc[:,1] >= 5)), 0)
    intensity[np.where((quality_ntc[:,0] < 0.88) & (quality_ntc[:,0] >= 0.44))] = percentageWithRandom(50, 20, 
                                                                                                       np.count_nonzero((quality_ntc[:,0] < 0.88) & (quality_ntc[:,0] >= 0.44)), 0)
    intensity[np.where((quality_ntc[:,0] < 0.44))] = percentageWithRandom(10, 40,
                                                                          np.count_nonzero(quality_ntc[:,0] < 0.44), generateFalseRate())
  
    return(intensity)

def negativeConcentration(quality):
    concentrations = np.array([None] * len(quality))
    concentrations[np.where(quality >= 0.88)] = percentageWithRandom(1, 4, np.count_nonzero(quality>0.88), generateFalseRate())
    
    concentrations[np.where((quality < 0.88) & (quality >= 0.44))] = percentageWithRandom(15, 5, 
                                                                    np.count_nonzero((quality < 0.88) & (quality >= 0.44)), 0)
    
    concentrations[np.where(quality < 0.44)] = percentageWithRandom(50, 10, np.count_nonzero(quality < 0.44),  generateFalseRate())
    
    return(concentrations)

def createSampleNames(quality):
    countSamples = int(len(quality)/3)
    
    
    sigDigits = 0
    for value in str(countSamples):
        sigDigits += 1
    
    formatType = "{:0>" + str(sigDigits) + "}"
    
    sampleNums = np.array(range(int(countSamples)), dtype = object) + 1
    for sampleInd in range(countSamples):
        sampleName = "ND" + formatType.format(sampleNums[sampleInd])
        sampleNums[sampleInd] = sampleName
    
    return(sampleNums)

def assignSampleNames(df, Names):
    
    for condition in pd.unique(df['Condition']):
        df.loc[df['Condition'] == condition, "Sample_ID"] = Names

    return(df)

def createDataFrame(numSamples):
    numSamples = numSamples-(numSamples%3)
    
    trials = np.linspace(1,numSamples, numSamples)
    quality_pct = randomPercentage(len(trials))
    negativeControl = negativeConcentration(quality_pct)
    intensity = generateIntensity(quality_pct, negativeControl)
    conditions = generateCondition(quality_pct)
    sampleNames = createSampleNames(quality_pct)
    
    rand_data = pd.DataFrame({"Trials":trials, "Quality": quality_pct,
                              "Negative_Control_Concentration":negativeControl,
                              "Intensity":intensity,
                              "Condition":conditions})
    
    rand_data = assignSampleNames(rand_data, sampleNames)
    
    return(rand_data)
