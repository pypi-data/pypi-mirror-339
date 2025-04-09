"""FunctionSM

This module contains all of the required functionality in regards to Summary Measure functions (their calculations)


Authors: Brandon Carrasco
Created on: 07-11-2024
Modified on: 08-04-2025
"""

# Imports
import numpy as np
from . import FieldSM as fsm
from . FieldSM import GetLocaleFromIndex, GetIndexFromLocale

# Constants

FRAMES_PER_SECOND = 29.97

## Ref ids for Data & SMs -> Easier way to call the summary measure functions

SM_MAPPING = {
    "calc_homebases" : "CalculateHomeBases",
    "calc_HB1_cumulativeReturn" : "CalculateFreqHomeBaseStops",
    "calc_HB1_meanDurationStops" : "CalculateMeanDurationHomeBaseStops",
    "calc_HB1_meanReturn" : "CalculateMeanReturnHomeBase",
    "calc_HB1_meanExcursionStops" : "CalculateMeanStopsExcursions",
    "calc_HB1_stopDuration" :  "Calculate_Main_Homebase_Stop_Duration",
    "calc_HB2_stopDuration" : "Calculate_Secondary_Homebase_Stop_Duration",
    "calc_HB2_cumulativeReturn" : "Calculate_Frequency_Stops_Secondary_Homebase",
    "calc_HB1_expectedReturn" : "Calculated_Expected_Return_Frequency_Main_Homebase",
    "calc_sessionReturnTimeMean" : "Calculate_Mean_Return_Time_All_Locales",
    "calc_sessionTotalLocalesVisited" : "Calculate_Total_Locales_Visited",
    "calc_sessionTotalStops" : "Calculate_Total_Stops",
    "calc_expectedMainHomeBaseReturn" : "Expected_Return_Time_Main_Homebase",
    "calc_distanceTravelled" : "Calculate_Distance_Travelled",
    "calc_boutsOfChecking" : "Calculate_Bouts"
}

DATA_MAPPING = {
    "locale_stops_calc" : "CalculateStops",
    "distances_calc" : "CalcuateDistances",
}


## Storing Dependencies for Summary Measures and Common Calcs
## SM Dependencies
### All SMs that are dependent on other SMs to be calculated appear here in this dict.
### Their values is a list of summary measures that must be calculated before the key SM is calculated.
SM_DEPENDENCIES = {
    "calc_HB1_cumulativeReturn" : ["calc_homebases"],
    "calc_HB1_meanDurationStops" : ["calc_homebases"],
    "calc_HB1_meanReturn" : ["calc_homebases"],
    "calc_HB1_meanExcursionStops" : ["calc_homebases"],
    "calc_HB1_stopDuration" : ["calc_homebases"],
    "calc_HB2_stopDuration" : ["calc_homebases"],
    "calc_HB2_cumulativeReturn" : ["calc_homebases"],
    "calc_HB1_expectedReturn" : ["calc_homebases"],
    "calc_sessionReturnTimeMean" : ["calc_homebases"],
    "calc_expectedMainHomeBaseReturn" : ["calc_homebases", "calc_HB1_meanReturn", "calc_sessionReturnTimeMean"],
    "calc_boutsOfChecking" : ["calc_homebases", "calc_HB1_meanReturn"],
}

## Data Dependencies
### Dictionary of summary measure names (strings) matched to the functions that calculate the metrics that the summary measure needs.
DATA_DEPENDENCIES = {
    "calc_homebases" : ["locale_stops_calc"],
    "calc_HB1_cumulativeReturn" : ["locale_stops_calc"],
    "calc_HB1_meanDurationStops" : ["locale_stops_calc"],
    "calc_HB1_meanReturn" : ["locale_stops_calc"],
    "calc_HB1_meanExcursionStops" : ["locale_stops_calc"],
    "calc_HB1_stopDuration" : ["locale_stops_calc"],
    "calc_HB2_stopDuration" : ["locale_stops_calc"],
    "calc_HB2_cumulativeReturn" : ["locale_stops_calc"],
    "calc_HB1_expectedReturn" : ["locale_stops_calc"],
    "calc_sessionReturnTimeMean" : ["locale_stops_calc"],
    "calc_sessionTotalLocalesVisited" : ["locale_stops_calc"],
    "calc_sessionTotalStops" : ["locale_stops_calc"],
    "calc_distanceTravelled" : ["distances_calc"]
}


### Commander-Specific Helper Functions (calculation of data mainly) ###

def CalculateLocale(movementMat, env: fsm.Environment):

    """
        Calculates and returns a vector of locales that the specimen is in at a specific x, y coordinate.
    """
    locales = []
    for i in range(len(movementMat)):
        frame = movementMat[i]
        locales.append(env.SpecimenLocation(frame[0], frame[1]))
    return np.array(locales)

def CheckForMissingDependencies(calc, preExistingSMs):
    """
        Confirms that the selected calc has all of its summary measure dependencies calculated. Throws error otherwise.
    """
    if calc not in SM_DEPENDENCIES.keys(): # If desired SM requires no summary measures to be calculated, then everything's fine
        return
    dependencies = SM_DEPENDENCIES[calc]
    notCalculated = set(dependencies) - set(preExistingSMs)
    if len(notCalculated) != 0: # If some dependencies still haven't been calculated
        print(f"Attempting to calculate {calc}, but missing the following necessary summary measures:")
        for sm in notCalculated:
            print(f"     - {sm}")
        raise Exception("Error: Missing one or more summary measures necessary to calculate another summary measure!")

def HandleMissingInputs(refId: str, data, env: fsm.Environment, calculatedSummaryMeasures, preExistingCalcs):
    """
        Calculates al
    """
    # Check if required summary measures have been calculated already
    CheckForMissingDependencies(refId, calculatedSummaryMeasures.keys())
    # Perform any necessary pre-calcs
    requiredCalcs = DATA_DEPENDENCIES["calc_HB2_stopDuration"]
    desiredCalcs = CalculateMissingCalcs(data, env, preExistingCalcs, requiredCalcs)
    return desiredCalcs

def CalculateMissingCalcs(data, env: fsm.Environment, preExistingCalcs, calcs):
    """
        Given a list calcuations, determin
    """
    # Find missing calcs
    desiredCalcs = {}
    if preExistingCalcs != None: # If passed pre-existing data, find any pre-calculated data that's missing (that will be calculated)
        missingCalcs = list(set(calcs) - set(preExistingCalcs.keys()))
        for calc in list(set(calcs) - set(missingCalcs)): # Add all already existing calcs to the desired calcs dictionary
            desiredCalcs[calc] = preExistingCalcs[calc]
    else:
        missingCalcs = calcs # If no pre-existing data passed, then calculated all required data.

    # Calculate Missing Calcs
    for missingCalc in missingCalcs: # Calculate all missing calculations and add them to the desired calcs dictionary
        calcFunc = globals()[DATA_MAPPING[missingCalc]]
        desiredCalcs[missingCalc] = calcFunc(data, env)

    # Return as dict for use in the summary measure function
    
    return desiredCalcs

### Calculating metrics ###

## Metrics/Data Calculation Schema ##
#   All calculations of common data that's used across one or more summary measures share the following input schema:
#       data : numpy.ndarray
#           Preprocessed data array, of the format: 0 = frame, 1 = x-coord, 2 = y-coord, 3 = velocity, 4 = movement type (lingering or progression)
#       env : Environment
#           Testing environment for the given specimen (and data array)
#   This schema is ensures that these functions can be called generically. Data Pre-calc functions shouldn't need anything but these two inputs.
## End of Data Calculation Schema ##


def CalculateStops(data: np.ndarray, env: fsm.Environment) -> tuple[list[int], list[int]]:
    """
        Given the raw time-series data and environment of the experiment, calculates the stops in each locale, as well as the total duration of the stops (in frames) for each locale.
    """
    stopLocales = [0 for x in range(25)]
    stopFrames = [0 for x in range(25)]
    stopped = False
    relevantLocale = False
    locDur = [0 for x in range(25)]
    
    for i in range(len(data)):
        frame = data[i]
        if frame[4] == 0: # Part of a lingering episode
            specimenLocale =  env.SpecimenLocation(frame[1], frame[2], index=True) # Get current locale of specimen
            # if GetLocaleFromIndex(specimenLocale) in [50, 4] and not relevantLocale:
            #     print(f"Currently in locale: {GetLocaleFromIndex(specimenLocale)}")
            #     relevantLocale = True
            stopped = True # Lingering episode begins (if it hasn't already begun)
            # Count the stop
            # if not stopped: # If it was previously moving and just now stopped
            #     stopped = True
                # locDur = [0 for x in range(25)]
            locDur[specimenLocale] += 1
        elif frame[4] == 1 and stopped: # lingering episode ends
            # if relevantLocale:
            #     relevantLocale = False
            #     print("End of lingering containing relevant locales")
            #     print(locDur)
            #     print(np.argmax(locDur))
            #     print(GetLocaleFromIndex(np.argmax(locDur)))
            #     print(f"Frame of ending: {frame[0]}")
            stopped = False
            # Get the maximum duration for each locale and add a stop to the max locale
            maxLocale = np.argmax(locDur)
            stopLocales[maxLocale] += 1
            # Add stop frames to total stop durations
            # stopFrames = [sum(comb) for comb in zip(stopFrames, locDur)]
            stopFrames[maxLocale] += sum(locDur) 
            # Reset local locale stop durations (for a stop episode)
            locDur = [0 for x in range(25)]

    if stopped: # if the search for stops ends on a stop, then sum it up and calculate the necessary stuff
        maxLocale = np.argmax(locDur)
        stopLocales[maxLocale] += 1
        # Add stop frames to total stop durations
        # stopFrames = [sum(comb) for comb in zip(stopFrames, locDur)]
        stopFrames[maxLocale] += sum(locDur) 
    return stopLocales, stopFrames


def CalcuateDistances(data: np.ndarray, env: fsm.Environment) -> list[int]:
    """
        Given the raw time-series data and environment, calculates the distance travelled from one frame to the next.

        Frame 0 will always be 0.
    """
    distanceFrames = [0]
    prevFrameX = data[0][1]
    prevFrameY = data[0][2]
    for i in range(1, len(data)):
        curFrameX = data[i][1]
        curFrameY = data[i][2]
        dist = np.sqrt(np.square(curFrameX - prevFrameX) + np.square(curFrameY - prevFrameY))
        distanceFrames.append(dist)
        prevFrameX = curFrameX
        prevFrameY = curFrameY
    return distanceFrames
        
        
### Functions to Calculate Summary Measures ###

### On Summary Measures format ###
#   All summary measures follow the same parameters format:
#       data : numpy.ndarray
#           Preprocessed data array, of the format: 0 = frame, 1 = x-coord, 2 = y-coord, 3 = velocity, 4 = movement type (lingering or progression)
#       env : Environment
#           Testing environment for the given specimen (and data array)
#       requiredSummaryMeasures : dict
#           Dict containing all summary measures (matching name to outputs) previously calculated by the interface (or by some other method). Must contain the summary measures that the current summary measure being calculated depends on.
#       preExisitingCalcs : dict | None
#           Dict containing all the data calculations (locale stops, etc.) that the summary measure requires. Optional, but saves time if pre-calculated and shared with all dependent summary measures.
#   The above schema ensures that summary measures can be run by the interface generically (or be handled by a bespoke solution generically).
### End of Summary Measures format explanation ###

## Minor Notes ##
#   SM descriptions contain the following two ids:
#   1. 'Also referred to as...', which describes what official name for the summary measures are when downloaded. Defined by Dr. Anna Dvorkin & Dr. Henry Szetchman. 
#   2. 'Reference ID for Commander:...', which describes the shorthand we use to call those summary measures (from the Commander class).
## End of Minor Notes ##

def CalculateHomeBases(data: np.ndarray, env: fsm.Environment, requiredSummaryMeasures: dict, preExistingCalcs: dict = None) -> tuple[int, int | None]:
    """
        Given an environment and matrix containing columns specifying the x-coords, y-coords, and movement type (lingering or progression) of the specimen per frame (every sample is one frame),
        return the two locales (main home base & secondary home base) of the specimen.

        If the main home base is visited only once, then return None for secondary home base. 

        Also referred to as KPname01 & KPname02.

        Reference ID for Commander: calc_homebases
    """
    ### Perform necessary calculations on the data!
    # TEMPORARY -> any required calc names should be stored in Data Dependences, which will be moved over to this file soon.
    requiredCalcs = DATA_DEPENDENCIES["calc_homebases"]
    desiredCalcs = CalculateMissingCalcs(data, env, preExistingCalcs, requiredCalcs)

    ### Summary Measure Logic
    localeVisits = desiredCalcs['locale_stops_calc'][0]
    localeDuration = desiredCalcs['locale_stops_calc'][1]
    for i in range(len(localeVisits)):
        print(f"Locale {GetLocaleFromIndex(i)} was visited {localeVisits[i]} times, for a duration of {localeDuration[i]}")

    # Calculate home bases
    topTwoMostVisited = np.argpartition(np.array(localeVisits), len(localeVisits) - 2)[-2:]
    localeA = topTwoMostVisited[0]
    localeB = topTwoMostVisited[1]
    # Check & handle tiebreaker
    if localeVisits[localeA] == localeVisits[localeB]:
        mainHomeBase = localeA if localeDuration[localeA] >= localeDuration[localeB] else localeB
    else:
        mainHomeBase = localeA if localeVisits[localeA] >= localeVisits[localeB] else localeB
    secondaryHomeBase = localeA if mainHomeBase == localeB else localeB
    if localeA < 2 and localeB < 2: # In case that there's less than two stops for main home base. In this case, the home base would essentially be a random locale that has one stop in it.
        return GetLocaleFromIndex(mainHomeBase), None
    else:
        return GetLocaleFromIndex(mainHomeBase), GetLocaleFromIndex(secondaryHomeBase)


def CalculateFreqHomeBaseStops(data: np.ndarray, env: fsm.Environment, requiredSummaryMeasures: dict, preExistingCalcs: dict = None) -> int:
    """
        Calculates the cumulative number of stops within the first home base. Requires the First Home Base to have been calculated (ref. id. calc_homebases)

        Also referred to as KPcumReturnfreq01

        Reference ID is: calc_HB1_cumulativeReturn
    """
    # Check if required summary measures have been calculated already
    CheckForMissingDependencies('calc_HB1_cumulativeReturn', requiredSummaryMeasures.keys())
    # Perform any necessary pre-calcs
    requiredCalcs = DATA_DEPENDENCIES["calc_HB1_cumulativeReturn"]
    desiredCalcs = CalculateMissingCalcs(data, env, preExistingCalcs, requiredCalcs)

    ### Summary Measure Logic
    localeVisits = desiredCalcs['locale_stops_calc'][0]
    mainHomeBase = requiredSummaryMeasures['calc_homebases'][0]

    # Constraint: cannot calculate the summary measure if 2nd home base isn't present
    # if requiredSummaryMeasures["calc_homebases"][1] == None:
    #     print("WARNING: Cannot calculate mean return time to main home base, as second home base does not exist!")
    #     return None
    
    ind = GetIndexFromLocale(mainHomeBase)
    return localeVisits[ind]

def CalculateMeanDurationHomeBaseStops(data: np.ndarray, env: fsm.Environment, requiredSummaryMeasures: dict, preExistingCalcs: dict = None) -> tuple[float, float]:
    """
        Calculates the mean duration (in seconds) of the specimen remaining in the main home base. Additionally returns the log (base 10) of this duration as well.

        Also referred to as KPmeanStayTime01_s & KPmeanStayTime01_s_log.

        Reference ID is: calc_HB1_meanDurationStops
    """
    # Check if required summary measures have been calculated already
    CheckForMissingDependencies('calc_HB1_meanDurationStops', requiredSummaryMeasures.keys())
    # Perform any necessary pre-calcs
    requiredCalcs = DATA_DEPENDENCIES["calc_HB1_meanDurationStops"]
    desiredCalcs = CalculateMissingCalcs(data, env, preExistingCalcs, requiredCalcs)

    ### Summary Measure Logic
    localeVisits = desiredCalcs['locale_stops_calc'][0]
    localeDuration = desiredCalcs['locale_stops_calc'][1]
    mainHomeBase = requiredSummaryMeasures['calc_homebases'][0]

    ind = GetIndexFromLocale(mainHomeBase)
    totalDuration = localeDuration[ind]
    numStops = localeVisits[ind]

    duration_in_seconds = (totalDuration / numStops) / FRAMES_PER_SECOND
    return duration_in_seconds, np.log10(duration_in_seconds)

def CalculateMeanReturnHomeBase(data: np.ndarray, env: fsm.Environment, requiredSummaryMeasures: dict, preExistingCalcs: dict = None) -> float:
    """
        Calculates the mean return time to the main home base (in seconds). Also can be thought of as the mean duration of execursions.

        Also referred to as KPcumReturnfreq01

        Reference ID is: calc_HB1_meanReturn
    """
    # Check if required summary measures have been calculated already
    CheckForMissingDependencies('calc_HB1_meanReturn', requiredSummaryMeasures.keys())
    # Perform any necessary pre-calcs
    requiredCalcs = DATA_DEPENDENCIES["calc_HB1_meanReturn"]
    desiredCalcs = CalculateMissingCalcs(data, env, preExistingCalcs, requiredCalcs)

    ### Summary Measure Logic
    localeVisits = desiredCalcs['locale_stops_calc'][0]
    localeDuration = desiredCalcs['locale_stops_calc'][1]
    mainHomeBase = requiredSummaryMeasures['calc_homebases'][0]

    # Constraint: cannot calculate the summary measure if 2nd home base isn't present
    if requiredSummaryMeasures["calc_homebases"][1] == None:
        print("WARNING: Cannot calculate mean return time to main home base, as second home base does not exist!")
        return None
    
    ind = GetIndexFromLocale(mainHomeBase)
    # Sum of all durations and stops minus the ones that are in the main home base
    totalDuration = sum(localeDuration) - localeDuration[ind]
    totalExcursions = sum(localeVisits) - localeVisits[ind]
    return (totalDuration / totalExcursions) / FRAMES_PER_SECOND

def CalculateMeanStopsExcursions(data: np.ndarray, env: fsm.Environment, requiredSummaryMeasures: dict, preExistingCalcs: dict = None) -> float:
    """
        Calculates the mean number of stops during excursions (away from the Main Home Base).

        Also referred to as KPstopsToReturn01

        Reference ID is: calc_HB1_meanExcursionStops
    """
    # Check if required summary measures have been calculated already
    CheckForMissingDependencies('calc_HB1_meanExcursionStops', requiredSummaryMeasures.keys())
    # Perform any necessary pre-calcs
    requiredCalcs = DATA_DEPENDENCIES["calc_HB1_meanExcursionStops"]
    desiredCalcs = CalculateMissingCalcs(data, env, preExistingCalcs, requiredCalcs)

    ### Summary Measure Logic
    # localeVisits = desiredCalcs['locale_stops_calc'][0]
    # localeDuration = desiredCalcs['locale_stops_calc'][1]
    mainHomeBase = requiredSummaryMeasures['calc_homebases'][0]

    totalExcursions = 0
    totalStops = 0
    excursion = False
    stopped = False
    # Count number of excursions (and their total stops) for each locale
    for i in range(len(data)):
        frame = data[i]
        specimenLocale = env.SpecimenLocation(frame[1], frame[2])
        if specimenLocale != mainHomeBase: # If the specimen is not in the main home base
            if frame[4] == 1 and not excursion: # If the specimen is no longer in its main home base, it's on an excursion. Has to be moving in a progressive episode to be counted as an excursion (lingering between main home base and elsewhere doesn't count).
                totalExcursions += 1
                excursion = True
            if frame[4] == 0 and excursion and not stopped: # If the specimen is lingering while on an excursion
                totalStops += 1
                stopped = True
            elif frame[4] == 1:
                stopped = False 
        else:
            excursion = False
    return totalStops / totalExcursions

def Calculate_Main_Homebase_Stop_Duration(data: np.ndarray, env: fsm.Environment, requiredSummaryMeasures: dict, preExistingCalcs: dict = None) -> float:
    """
        Calculates the cumulative duration of stops within the first home base, measured in seconds.

        Also referred to as: KPtotalStayTime01_s

        Reference ID is: calc_HB1_stopDuration
    """
    # Check if required summary measures have been calculated already
    CheckForMissingDependencies('calc_HB1_stopDuration', requiredSummaryMeasures.keys())
    # Perform any necessary pre-calcs
    requiredCalcs = DATA_DEPENDENCIES["calc_HB1_stopDuration"]
    desiredCalcs = CalculateMissingCalcs(data, env, preExistingCalcs, requiredCalcs)

    ### Summary Measure Logic
    # localeVisits = desiredCalcs['locale_stops_calc'][0]
    localeDuration = desiredCalcs['locale_stops_calc'][1]
    mainHomeBase = requiredSummaryMeasures['calc_homebases'][0]

    ind = GetIndexFromLocale(mainHomeBase)
    return localeDuration[ind] / FRAMES_PER_SECOND

def Calculate_Secondary_Homebase_Stop_Duration(data: np.ndarray, env: fsm.Environment, requiredSummaryMeasures: dict, preExistingCalcs: dict = None) -> float:
    """
        Calculates the cumulative duration of stops within the second home base, measured in seconds.

        Warning: There must be at least two stop within the first home base (for the second home base to exist).

        Also referred to as: KPtotalStayTime02_s

        Reference ID is: calc_HB2_stopDuration
    """
    # Check if required summary measures have been calculated already
    CheckForMissingDependencies('calc_HB2_stopDuration', requiredSummaryMeasures.keys())
    # Perform any necessary pre-calcs
    requiredCalcs = DATA_DEPENDENCIES["calc_HB2_stopDuration"]
    desiredCalcs = CalculateMissingCalcs(data, env, preExistingCalcs, requiredCalcs)

    ### Summary Measure Logic
    # Constraint: cannot calculate the summary measure if 2nd home base isn't present
    if requiredSummaryMeasures["calc_homebases"][1] == None:
        print("WARNING: Cannot calculate mean return time to main home base, as second home base does not exist!")
        return None

    # localeVisits = desiredCalcs['locale_stops_calc'][0]
    localeDuration = desiredCalcs['locale_stops_calc'][1]
    secondaryHomeBase = requiredSummaryMeasures['calc_homebases'][1]

    ind = GetIndexFromLocale(secondaryHomeBase)
    return localeDuration[ind] / FRAMES_PER_SECOND


def Calculate_Frequency_Stops_Secondary_Homebase(data: np.ndarray, env: fsm.Environment, requiredSummaryMeasures: dict, preExistingCalcs: dict = None) -> int:
    """
        Calculates the cumulative number of stops within the second home base.

        Warning: There must be at least two stop within the first home base (for the second home base to exist).

        Also referred to as: KPcumReturnfreq02

        Reference ID is: calc_HB2_cumulativeReturn
    """
    # Check if required summary measures have been calculated already
    CheckForMissingDependencies('calc_HB2_cumulativeReturn', requiredSummaryMeasures.keys())
    # Perform any necessary pre-calcs
    requiredCalcs = DATA_DEPENDENCIES["calc_HB2_cumulativeReturn"]
    desiredCalcs = CalculateMissingCalcs(data, env, preExistingCalcs, requiredCalcs)

    ### Summary Measure Logic
    # Constraint: cannot calculate the summary measure if 2nd home base isn't present
    if requiredSummaryMeasures["calc_homebases"][1] == None:
        print("WARNING: Cannot calculate mean return time to main home base, as second home base does not exist!")
        return None

    localeVisits = desiredCalcs['locale_stops_calc'][0]
    # localeDuration = desiredCalcs['locale_stops_calc'][1]
    secondaryHomeBase = requiredSummaryMeasures['calc_homebases'][1]

    ind = GetIndexFromLocale(secondaryHomeBase)
    return localeVisits[ind]

def Calculated_Expected_Return_Frequency_Main_Homebase(data: np.ndarray, env: fsm.Environment, requiredSummaryMeasures: dict, preExistingCalcs: dict = None) -> float:
    """
        Calculates the expected return frequency to the first home base.

        TO DO: Confirm that this function is meant to calculate expected return!

        Also referred to as: KPexpReturnfreq01

        Reference ID is: calc_HB1_expectedReturn
    """
    # Check if required summary measures have been calculated already
    CheckForMissingDependencies('calc_HB1_expectedReturn', requiredSummaryMeasures.keys())
    # Perform any necessary pre-calcs
    requiredCalcs = DATA_DEPENDENCIES["calc_HB1_expectedReturn"]
    desiredCalcs = CalculateMissingCalcs(data, env, preExistingCalcs, requiredCalcs)

    ### Summary Measure Logic
    localeVisits = desiredCalcs['locale_stops_calc'][0]
    # localeDuration = desiredCalcs['locale_stops_calc'][1]
    mainHomeBase = requiredSummaryMeasures['calc_homebases'][0]

    # The total number of locales visited during the session
    totalLocalesVisited = sum([1 if visits > 0 else 0 for visits in localeVisits])

    # All stops in the main home base
    ind = GetIndexFromLocale(mainHomeBase)
    mainVisits = localeVisits[ind]
    
    return (mainVisits * totalLocalesVisited) / sum(localeVisits)

def Calculate_Mean_Return_Time_All_Locales(data: np.ndarray, env: fsm.Environment, requiredSummaryMeasures: dict, preExistingCalcs: dict = None) -> float:
    """
        Calculates the mean return time to all locales,

        Warning: There must be at least two stop within the first home base (for there to be a main home base). I think.

        Also referred to as: KP_session_ReturnTime_mean

        Reference ID is: calc_sessionReturnTimeMean
    """
    # Check if required summary measures have been calculated already
    CheckForMissingDependencies('calc_sessionReturnTimeMean', requiredSummaryMeasures.keys())
    # Perform any necessary pre-calcs
    requiredCalcs = DATA_DEPENDENCIES["calc_sessionReturnTimeMean"]
    desiredCalcs = CalculateMissingCalcs(data, env, preExistingCalcs, requiredCalcs)

    ### Summary Measure Logic
    if requiredSummaryMeasures["calc_homebases"][1] == None:
        print("WARNING: Cannot calculate mean return time to all locales, as the first home base is only stopped in once!")
        return None

    localeVisits = desiredCalcs['locale_stops_calc'][0]
    mainHomeBase = requiredSummaryMeasures['calc_homebases'][0]

    totalExcursionDuration = 0
    excursion = False
    # Count number of excursions (and their total stops) for each locale
    for i in range(len(data)):
        frame = data[i]
        specimenLocale = env.SpecimenLocation(frame[1], frame[2])
        specimenLocaleIndex = GetIndexFromLocale(specimenLocale)
        if specimenLocale != mainHomeBase: # If the specimen is not in the main home base
            if frame[4] == 1 and not excursion: # If the specimen is no longer in its main home base, it's on an excursion. Has to be moving in a progressive episode to be counted as an excursion (lingering between main home base and elsewhere doesn't count).
                excursion = True
            elif excursion and localeVisits[specimenLocaleIndex] > 1: # If the specimen is on an excursion in a locale that it will/has stopped in more than once
                totalExcursionDuration += 1
        else:
            excursion = False
    return (totalExcursionDuration / sum(localeVisits)) / FRAMES_PER_SECOND


def Expected_Return_Time_Main_Homebase(data: np.ndarray, env: fsm.Environment, requiredSummaryMeasures: dict, preExistingCalcs: dict = None) -> float:
    """
        Calculates the expected return time to the main homebase.

        Warning: There must be at least two stop within the first home base (for there to be a main home base). I think.

        Also referred to as: KPexpReturntime01

        Reference ID is: calc_expectedMainHomeBaseReturn
    """
    # Check if required summary measures have been calculated already
    CheckForMissingDependencies('calc_expectedMainHomeBaseReturn', requiredSummaryMeasures.keys())
    # Perform any necessary pre-calcs
    requiredCalcs = DATA_DEPENDENCIES["calc_expectedMainHomeBaseReturn"]
    desiredCalcs = CalculateMissingCalcs(data, env, preExistingCalcs, requiredCalcs)

    ### Summary Measure Logic
    if requiredSummaryMeasures["calc_homebases"][1] == None:
        print("WARNING: Cannot calculate mean return time to all locales, as the first home base is only stopped in once!")
        return None
    
    mainHomeBaseMeanReturn = requiredSummaryMeasures['calc_HB1_meanReturn']
    sessionMeanReturn = requiredSummaryMeasures['calc_sessionReturnTimeMean']
    
    return mainHomeBaseMeanReturn / sessionMeanReturn
    

def Calculate_Total_Locales_Visited(data: np.ndarray, env: fsm.Environment, requiredSummaryMeasures: dict, preExistingCalcs: dict = None) -> int:
    """
        Calculates the total number of locales visited (1 to 25) throughout a session.

        Also referred to as: KP_session_differentlocalesVisited_#

        Reference ID is: calc_sessionTotalLocalesVisited
    """
    # Check if required summary measures have been calculated already
    CheckForMissingDependencies('calc_sessionTotalLocalesVisited', requiredSummaryMeasures.keys())
    # Perform any necessary pre-calcs
    requiredCalcs = DATA_DEPENDENCIES["calc_sessionTotalLocalesVisited"]
    desiredCalcs = CalculateMissingCalcs(data, env, preExistingCalcs, requiredCalcs)

    ### Summary Measure Logic
    localeVisits = desiredCalcs['locale_stops_calc'][0]
    
    visitedLocales = [1 if visits > 0 else 0 for visits in localeVisits]
    return sum(visitedLocales)

def Calculate_Total_Stops(data: np.ndarray, env: fsm.Environment, requiredSummaryMeasures: dict, preExistingCalcs: dict = None) -> int:
    """
        Calculates total number of stops in a session.

        Also referred to as: KP_session_Stops_total#

        Reference ID is: calc_sessionTotalStops
    """
    # Check if required summary measures have been calculated already
    CheckForMissingDependencies('calc_sessionTotalStops', requiredSummaryMeasures.keys())
    # Perform any necessary pre-calcs
    requiredCalcs = DATA_DEPENDENCIES["calc_sessionTotalStops"]
    desiredCalcs = CalculateMissingCalcs(data, env, preExistingCalcs, requiredCalcs)

    ### Summary Measure Logic
    localeVisits = desiredCalcs['locale_stops_calc'][0]

    return sum(localeVisits)

###  Distance & Locomotion Summary Measures ###

def Calculate_Distance_Travelled(data: np.ndarray, env: fsm.Environment, requiredSummaryMeasures: dict, preExistingCalcs: dict = None):
    """
        Calculates all distances travelled metrics. Returns a tuple of (total distance for progression segments only, total distance for all segments),
        total distance travelled, speed of progression, 
        and a tuple of two lists of travelled distances in five minute intervals from start to finish,
        with the first list corresponding to the use of only the progression statements, and
        the second corresponding to the use of all segements.

        See Checking_parameters_Definitions_Oct30_2024 for full list of variables.

        Reference ID is: calc_distanceTravelled
    """
    # Check if required summary measures have been calculated already
    CheckForMissingDependencies('calc_distanceTravelled', requiredSummaryMeasures.keys())
    # Perform any necessary pre-calcs
    requiredCalcs = DATA_DEPENDENCIES["calc_distanceTravelled"]
    desiredCalcs = CalculateMissingCalcs(data, env, preExistingCalcs, requiredCalcs)

    ### Summary Measure Logic
    distanceData = desiredCalcs['distances_calc']
    # Get chunk length (in terms of frames) for five minutes worth of time
    chunkLength = 5 * 60 * FRAMES_PER_SECOND
    chunk = 0
    distancesProgression = [0 for i in range(11)]
    distancesAll = [0 for i in range(11)]
    totalDurationOfProgression = 0

    for i in range(len(data)):
        # Update chunks if necessary
        if i == (chunk + 1) * chunkLength:
            chunk += 1
        frame = data[i]
        # Add distance to all distances list
        distancesAll[chunk] += distanceData[i]
        if frame[4] == 1: # If it's a progression segment, add it to the progression distances list
            distancesProgression[chunk] += distanceData[i]
            totalDurationOfProgression += 1 # Add 1 frame to the total duration of progressions
    totalDurationSeconds = totalDurationOfProgression / FRAMES_PER_SECOND
    # Divide all distances by 100 to get distance in metres
    distancesAll = [distance / 100 for distance in distancesAll]
    distancesProgression = [distance / 100 for distance in distancesProgression]
    # Calculate total distance travelled for all & progression
    totalDistanceAll = sum(distancesAll)
    totalDistanceProgression = sum(distancesProgression)
    return (totalDistanceProgression, totalDistanceAll), totalDurationSeconds, totalDistanceProgression / (totalDurationSeconds), (distancesProgression, distancesAll)

# Below summary isn't finished yet! Do not call it. Ever. For now.
def Calculate_Bouts(data: np.ndarray, env: fsm.Environment, requiredSummaryMeasures: dict, preExistingCalcs: dict = None):
    """
        Calculates the bouts of checking. Not sure of what to return yet

        TO BE IMPLEMENTED

        Reference ID is: calc_boutsOfChecking
    """
    # Check if required summary measures have been calculated already
    CheckForMissingDependencies('calc_boutsOfChecking', requiredSummaryMeasures.keys())
    # Perform any necessary pre-calcs
    requiredCalcs = DATA_DEPENDENCIES["calc_boutsOfChecking"]
    desiredCalcs = CalculateMissingCalcs(data, env, preExistingCalcs, requiredCalcs)

    ### Summary Measure Logic
    mainHomeBase = requiredSummaryMeasures["calc_homebases"][0]
    mainHomeBaseReturn = requiredSummaryMeasures["calc_HB1_meanReturn"]

    ## Need to find all long lingering episodes and filter them out to get bouts of activity
    # Find mean time + IQR of lingering episodes
    allLing = []
    ling = False
    currentLing = []

    # Get the start and end points of all lingering episodes
    for i in range(len(data)):
        frame = data[i]
        if frame[4] == 0:
            ling = True
            currentLing.append(i)
        elif frame[4] == 1 and ling == True:
            ling = False
            currentLing.append(i)
            allLing.append(currentLing)
            currentLing = []
    if len(currentLing) != 0: # In case the loop ends on a lingering episode
        allLing.append(len(data))

    # Calculate means for lingering episode duration
    timeForEpi = [start - end for epi in allLing for start, end in epi] # Calculate the total duration
    meanTimeLing = sum(timeForEpi) / len(allLing)
    q75Mean, q25Mean = np.percentile(timeForEpi, [75, 25])
    iqrMean = q75Mean - q25Mean

    # Get outlier lingering episodes (time of epi is >= mean + 1.5 * iqr)
    outlierIndices = np.array(timeForEpi)
    outlierIndices = [outlierIndices >= (meanTimeLing + 1.5 * iqrMean)]
    outliers = []
    for x in range(len(timeForEpi)): # Get indices of all outlier episodes in the actual data
        outliers = outliers + [frame for frame in range(timeForEpi[x][0], timeForEpi[x][1])] # generate indicies between the start and end of lingering episodes

    # Calculate bouts of activity
    boutOfActivity = np.delete(data, outliers, axis=0) # Delete all frames that belong to outlier lingering episodes

    # # Filter out all bouts that have too long excursion times
    
    # Find all possible intervals
    ## Find the start and end points of all homebase visitations (their frames).
    right_points = [] # start of hb visitation (think of it as the ')', or end, of an interval)
    left_points = [] # end of hb visitation (think of it as the '(', or start, of an interval)
    hb = False if env.SpecimenLocation(data[0][1], data[0][2]) != mainHomeBase else True
    for i in range(len(data)):
        frame = data[i]
        if not hb and env.SpecimenLocation(frame[1], frame[2]) == mainHomeBase:
            hb = True
            right_points.append(i)
        elif hb and env.SpecimenLocation(frame[1], frame[2]) != mainHomeBase:
            hb = False
            left_points.append(i - 1)

    ## Create the intervals from the above 


    ## Check if their excursion stuff meets the criteria

    # Filter out lingering episodes that don't start and end in homebase
    outliers = list(filter(lambda x : env.SpecimenLocation(x[0][1], x[0][2]) == mainHomeBase and env.SpecimenLocation(x[-1][1], x[-1][2]) == mainHomeBase, outliers))

    # Dunno :)



### TESTING ###
# x = np.array([1, 5, 21, 1, 2, 5, 9, 21])
# print(x[np.argpartition(x, len(x) - 2)][-2:])

# x = 10
# print(np.log10(x))

# x = np.array([[1, 2, 3, 10], [4, 5, 6, 11], [7, 8, 9, 12]])
# print(x[:, [0, 2, 3]])