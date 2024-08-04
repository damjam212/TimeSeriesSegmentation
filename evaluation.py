import numpy as np
import pandas as pd 
# https://ceur-ws.org/Vol-1226/paper31.pdf

def points_labels_vector(n,change_points):
    """This function creates vector of predicated labels [0,0, ...,1,...0] 
    where 1 means time series at this index is change point, and 0 that there is no change point

    Args:
        n: count of time series
        change_points: 1-D numpy array with change point indexes
    Returns:
        A 1-D numpy array with lenght of n, containing ones and zeros
    """
    predicted_labels = np.zeros(n)
    predicted_labels[change_points] = 1
    return predicted_labels


def calculate_TP_TN_FP_FN(n, predicted_points, original_points, treshold):
    """This function calculates TP, TN, FP, FN , the change point is correct if its distance from original
    change point is closer then treshold, when there is more than one change point within the threshold the additional
    ones are considered FP

    Args:
        n: count of time series
        predicted_points: 1-D numpy array with predicted change point indexes
        original_points: 1-D numpy array with original change point indexes
        treshold: arbitray distance from orignal point
    Returns:
        A scalar values of TP, TN, FP, FN
    """
    predicted_labels = points_labels_vector(n, predicted_points)
    original_labels = points_labels_vector(n, original_points)

    TP = 0
    TN = 0
    FP = 0
    FN = 0
    zone_counter = np.zeros(len(original_points), dtype=bool)
    for index, value in enumerate(predicted_labels):
        if(np.min(np.abs(original_points - index)) < treshold):
            if value == 1:
                which_point = np.argmin(np.abs(original_points - index))
                #print(original_points)
                #print(which_point)
                if zone_counter[which_point] == True :
                    FP+=1
                else:
                    TP+=1     
                    zone_counter[which_point] = True
        else:
            if value == 0:
                TN+=1
            else:
                FP+=1

    for index , val in enumerate(zone_counter):
         if val == False:
             FN+=1

    return TP, TN, FP, FN
            


def calculate_ACC_PRE_REC_F1(TP,TN,FP,FN):
    A = (TP+TN)/(TP+TN+FP+FN)
    P = TP/(TP+FP)
    R = TP/(TP+FN)
    F1 = (2*TP)/(2*TP+FN+FP)
    return A,P,R,F1


def calculateASC(n, predicted_points, original_points, treshold):
    """This function calculates average count of predicted change points in segmentation zone

    Args:
        n: count of time series
        predicted_points: 1-D numpy array with predicted change point indexes
        original_points: 1-D numpy array with original change point indexes
        treshold: arbitray distance from orignal point
    Returns:
        average change point count for segmentation zone 
    """
    predicted_labels = points_labels_vector(n, predicted_points)
    original_labels = points_labels_vector(n, original_points)

    sum = 0
    zone_counter = np.zeros(len(predicted_points), dtype=bool)
    for index, value in enumerate(predicted_labels):
        if(np.min(np.abs(original_points - index)) < treshold):
            if value == 1:
                sum+=1
 
    return sum/len(original_points)

def calculateASD(n, predicted_points, original_points, treshold):
    """This function calculates average distance of predicted change points from the center of segmentation zone

    Args:
        n: count of time series
        predicted_points: 1-D numpy array with predicted change point indexes
        original_points: 1-D numpy array with original change point indexes
        treshold: arbitray distance from orignal point
    Returns:
        average distance 
    """
    predicted_labels = points_labels_vector(n, predicted_points)
    original_labels = points_labels_vector(n, original_points)

    ASD = 0
    div = 0
    zone_counter = np.zeros(len(predicted_points), dtype=bool)
    for index, value in enumerate(predicted_labels):
        if(np.min(np.abs(original_points - index)) < treshold):
            if value == 1:
                ASD += np.min(np.abs(original_points - index))
                div += 1
 
    return (ASD/div) if div > 0 else -1


def calculateADT(n, predicted_points, original_points, treshold):
    """This function calculates average direction tendency, above 0.5 means that algorithm tends to place change points after
        segmentation zone center. Value below 0.5 means the tendency is to put change points before segmentation zone center
    Args:
        n: count of time series
        predicted_points: 1-D numpy array with predicted change point indexes
        original_points: 1-D numpy array with original change point indexes
        treshold: arbitray distance from orignal point
    Returns:
        average direction tendency
    """
    predicted_labels = points_labels_vector(n, predicted_points)
    original_labels = points_labels_vector(n, original_points)

    PostSeg = 0
    PreSeg = 0
    zone_counter = np.zeros(len(predicted_points), dtype=bool)
    for index, value in enumerate(predicted_labels):
        if(np.min(np.abs(original_points - index)) < treshold):
            if value == 1:
                arg = np.argmin(np.abs(original_points - index))
                if index > original_points[arg]:
                    PostSeg += 1
                else:
                    PreSeg += 1
 
    return (PostSeg/(PostSeg+PreSeg)) if (PostSeg+PreSeg) > 0 else -1

        
def get_evaluation(result, original_points, n):
    prediction_margin =( n/len(original_points)/8)
    print(prediction_margin)
    TP,TN,FP,FN = calculate_TP_TN_FP_FN(n,result,original_points,prediction_margin)
    ASC = calculateASC(n,result,original_points,prediction_margin)
    ASD = calculateASD(n,result,original_points,prediction_margin)
    ADT = calculateADT(n,result,original_points,prediction_margin)
        
    Acc, Prec, Recall, F1 = calculate_ACC_PRE_REC_F1(TP,TN,FP,FN)
    #score = ScoreRegimes(result,original_points,n)
        
        # Dane
    etykiety = ["Acc", "Prec", "Recall", "F1","ASC","ASD","ADT"]
    wartosci = [Acc, Prec, Recall, F1 , ASC , ASD, ADT]
        
        # Tworzenie DataFrame
    evaluation = pd.DataFrame({
            "Metryka": etykiety,
            "Wartość": wartosci
        })
    return evaluation
#eval = get_evaluation(regimes,ch,129276)

def ScoreRegimes(locRegimes, gtRegimes, ts_length):
    """
    Function to score the difference between extracted regimes and ground truth regimes.

    Parameters:
    locRegimes (list or np.array): extracted regimes
    gtRegimes (list or np.array): ground truth regimes
    ts_length (int): length of the time series

    Returns:
    float: score in the range [0, 1], with 0 being the best score
    """
    sumDiff = 0
    numRegimes = len(gtRegimes)

    for i in range(numRegimes):
        # Find the gtRegimes[j] closest to locRegimes[i]
        closest_diff = min(abs(locRegime - gtRegimes[j]) for j, locRegime in enumerate(locRegimes))
        sumDiff += closest_diff

    score = sumDiff / ts_length
    return score
