# Python libraries needed to run the TDA based method package ##
import numpy as np
import pandas as pd
from scipy.io import loadmat
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import time
import warnings
warnings.filterwarnings("ignore")
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score
import os
import joblib
import cloudpickle




#This funcion loads the separate .npy files that contains ML features for various landslide types
def load_data(path):
    #INPUT- path to .npy file
    #recognizes various landslide types in the data from the names of .npy file
    npy_files = [file for file in os.listdir(path) if file.endswith(".npy")]
    dictionary = {}
    #ML features numpy arrays are stored in dictionary as values and keys are landslide types
    for npy_file in npy_files:
        file_path = os.path.join(path, npy_file)
        loaded_array = np.load(file_path)

        key_name = os.path.splitext(npy_file)[0]
        dictionary[key_name] = loaded_array

    return dictionary
#OUTPU- gives a dictionary with keys as different landslide types and ML features numpy arrays as values


#This function recognizes various labels, aka, different landslide types
def labelgeneration(dictionary):
    #INPUT- the dictionary produced in previous function
    arrays = {}
    columns = ['Landslide Type', 'Values']
    df = pd.DataFrame(columns = columns)
    #Creating a dataframe to store information about which landslide type corresponds to which number
    
    for i, key in enumerate(dictionary.keys()):
        names = f'label_{key}'
        #Assigning each landslide type with a number to be used as labels
        arrays[names] = np.ones((np.shape(dictionary[key])[0],1))*i
        new_row= pd.Series({'Landslide Type': key, 'Values': i})
        df = pd.concat([df, new_row.to_frame().T], ignore_index = True, axis= 0)
        print(f'Landslide type {key} corresponds to:: {i}')
        print('##################################################')
        print(new_row)
    return arrays, df
#OUTPUT- A dictionary called arrays that contains keys as various landslide types and values as the index assigned to the landslide type




#This function vertically stacks the ML features from different landslide types and their labels
def verticalstacking(dictionary, arrays):
    #INPUT- both the dictionaries from above functions
    features = [dictionary[i] for i in dictionary.keys()]
    data = np.vstack(features)
    #ML Features are stacked
    
    ##ASK KAMAL ABOUT THIS PART (IMPORTANT)
    false_data_ind=np.unique(np.argwhere(data>10000)[:,0])
    real_data_ind=np.setdiff1d(np.arange(len(data)),false_data_ind)
    
    labels = [arrays[j] for j in arrays.keys()]
    label = np.vstack(labels)
    # Labels corresponding to the ML features are stacked
    ## THIS TOO
    data=data[real_data_ind,:]
    label=label[real_data_ind,:]
    data_df = pd.DataFrame(data)
    labels_df = pd.DataFrame(label, columns=['Labels'])
    return data_df, labels_df
#OUTPUT- two dataframes, one contains ML features from all the landslide types, other contains labels corresponding to those ML features



#We can skip this function for now, ignore it-
def ACC(dictionary, confusion_matrix):
    
    ACC = {}
    for key in dictionary.keys():
        names = f'ACC_{key}'
        ACC[names] = []
    
        
    for i, keyacc in enumerate(ACC.keys()):
        # aa_values = (confusion_matrix[i,i]/np.sum(confusion_matrix[i,:]))*100
        # ACC[keyacc].append(aa_values)
        ACC[keyacc].append(((confusion_matrix[i,i] / np.sum(confusion_matrix[i,:]))*100))
    return ACC
        
        
        

        
##THIS IS THE CODE THAT KAMAL WROTE FOR SPLITTING THE DATA INTO TRAINING AND TESTING SET
## AND TRAIN THE RF MODEL        
# def MovementClassifier(path):
    



#     dictionary = load_data(path)
#     arrays, df = labelgeneration(dictionary= dictionary)
#     data_df, labels_df = verticalstacking(dictionary= dictionary, arrays= arrays)
    
    
    # #################################################################################
    # #TRAINING PHASE FOR MODEL ROBUSTNESS
    # feature=[]
    # f1scores = []
    # for count in range(10):
    #     print(f'counter is :: {count+1}')
    #     start_time = time.time()
    #     Train,Test=[],[]
    #     Trainlabel,Testlabel=[],[]
    #     feato=[]
    #     kf = StratifiedKFold(n_splits=10,shuffle=True)  
    #     for train_index, test_index in kf.split(data, label):
    #         Train.append(data[train_index,:])
    #         Test.append(data[test_index,:])
    #         Trainlabel.append(label[train_index])
    #         Testlabel.append(label[test_index])

    #     for k in range(10):
    #         Classifier = RandomForestClassifier(n_estimators=100) 
    #         scaler = StandardScaler()
    #         train_data = scaler.fit_transform( Train[k])
    #         test_data = scaler.transform(Test[k])
    #         Classifier.fit(train_data,np.ravel(Trainlabel[k] ))      
    #         y_pred = Classifier.predict(test_data)
    #         f1scores.append(f1_score(Testlabel[k],y_pred,average='micro'))
    #         Featur_importance=Classifier.feature_importances_
    #         feato.append(Featur_importance)
    #     feature.append(np.average(np.asarray(feato),axis=0))
        
    # print(f'Mean F1 Score for the model is :: {np.mean(f1scores)}')
    # print(f'Standard Deviation of F1 Score for the model is :: {np.std(f1scores)}') 
    # print("--- %s seconds ---" % (time.time() - start_time))
    # print('##################################################')
    
    
    
    
    
    # #################################################################################
    # #PRODUCING OPTIMIAL FEATURE SPACE 
    # FEATURE_IMP=np.asarray(feature)
    # FEATURE_IMP=np.average(FEATURE_IMP,axis=0)
    
    
    # ##THINKING OF PROVIDING A SWITCH FOR CHOOSING FEATURE SPACE
    
    
    # imp_features=np.argsort(-FEATURE_IMP)[0:8]
    # data=data[:,imp_features]
    
    
    
    
    
    # ##################################################################################
    # #FINAL TERAINING WITH OPTIMAL FEATURE SPACE
    # f1scoresupdate = []
    # for count in range(10):
    #     print(f'counter is :: {count+1}')
    #     Trainupdate,Testupdate=[],[]
    #     Trainlabelupdate,Testlabelupdate=[],[]
    #     kfupdate = StratifiedKFold(n_splits=10,shuffle=True)  
    #     for train_index, test_index in kfupdate.split(data, label):
    #         Trainupdate.append(data[train_index,:])
    #         Testupdate.append(data[test_index,:])
    #         Trainlabelupdate.append(label[train_index])
    #         Testlabelupdate.append(label[test_index])

    #     for k in range(10):
    #         Classifierupdate = RandomForestClassifier(n_estimators=100) 
    #         scalerupdate = StandardScaler()
    #         train_dataupdate = scalerupdate.fit_transform( Trainupdate[k])
    #         test_dataupdate = scalerupdate.transform(Testupdate[k])
    #         Classifierupdate.fit(train_dataupdate,np.ravel(Trainlabelupdate[k] ))
    #         y_predupdate = Classifierupdate.predict(test_dataupdate)
    #         f1scoresupdate.append(f1_score(Testlabelupdate[k],y_predupdate,average='micro'))
                    
        
            
    # print(f'Mean F1 Score for the model is :: {np.mean(f1scoresupdate)}')
    # print(f'Standard Deviation of F1 Score for the model is :: {np.std(f1scoresupdate)}') 
    # print("--- %s seconds ---" % (time.time() - start_time))
    
    # print('##################################################')
    
    
    # joblib.dump(Classifier, './Model_All_Features.joblib')
    # # joblib.dump(Classifierupdate, './Model_Optimized_Features.joblib')
    # df.to_csv(f'{path}/Landslide_Types.csv')


##THIS IS THE NEW FUNCTION THAT USES train_test_split FROM sklearn TO SPLIT THE DATA
## AND JUST FOR NOW, WE ARE GENERATING ONLY ONE TRAINED MODEL
def MovementClassifier(path):
    #INPUT- path to the .npy files that contains ML features for each landslide type
    
    #Calling the above functions
    dictionary = load_data(path)
    arrays, df = labelgeneration(dictionary= dictionary)
    data_df, labels_df = verticalstacking(dictionary= dictionary, arrays= arrays)
    
    #################################################################################
    #TRAINING PHASE FOR MODEL ROBUSTNESS
    feature=[]
    f1scores = []
    feato = []

    for count in range(10):
        print(f"outer iteration {count+1}:")
        for innercount in range(10):
            print(f"Iteration {innercount+1}:")
            start_time = time.time()
            X_train, X_test, y_train, y_test = train_test_split(data_df, labels_df, test_size = 0.35, random_state= count)
            rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            rf_classifier.fit(X_train, y_train)
            y_pred = rf_classifier.predict(X_test)
            prob = rf_classifier.predict_proba(X_test)
            f1scores.append(f1_score(y_test, y_pred, average = 'micro'))
            feato.append(rf_classifier.feature_importances_)
        feature.append(np.average(np.asarray(feato),axis=0))    
    
    print(f'Mean F1 Score for the model is :: {np.mean(f1scores)}')
    print(f'Standard Deviation of F1 Score for the model is :: {np.std(f1scores)}') 
    print("--- %s seconds ---" % (time.time() - start_time))
    print('##################################################')
    print('###############')
    print(f'Data type of X_Train is:: {type(X_train)}')
    print(f'Data type of y_train is:: {type(y_train)}')




    # # print(f'counter is :: {count+1}')
    # start_time = time.time()
    # #Training the RF Classifier model-
    # rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    # rf_classifier.fit(X_train, y_train)
    # y_pred = rf_classifier.predict(X_test)
    # prob = rf_classifier.predict_proba(X_test)
    # f1scores.append(f1_score(y_test,y_pred,average='micro'))
    # Featur_importance=rf_classifier.feature_importances_
    # feato.append(Featur_importance)
    # feature.append(np.average(np.asarray(feato),axis=0))
    





    #FOR NOW WE CAN SKIP THIS-
    #HERE, WE FIND THE FEATURE SPACE AND PERFORM FEATURE IMPORTANCE AND THEN USES JUST THOSE
    #FEATURES FOR TRAINING AN OPTIMIZED MODEL


    #################################################################################
    #PRODUCING OPTIMIAL FEATURE SPACE 
    FEATURE_IMP=np.asarray(feature)
    FEATURE_IMP=np.average(FEATURE_IMP,axis=0)


    ##THINKING OF PROVIDING A SWITCH FOR CHOOSING FEATURE SPACE


    imp_features=np.argsort(-FEATURE_IMP)[0:8]
    imp_features_df = pd.DataFrame(imp_features)
    imp_features_df.to_csv(f"{path}/Optimized_Features.csv")
    print(f"Shape of data_df: {data_df.shape}")
    print(f"Selected feature indices: {imp_features}")
    data_df_update=data_df.iloc[:,imp_features]
    f1scores_update = []


    # ##################################################################################
    # #FINAL TERAINING WITH OPTIMAL FEATURE SPACE
    
    
    for count in range(10):
        print(f"outer iteration {count+1}:")
        for innercount in range(10):
            print(f"Iteration {innercount+1}:")
            start_time = time.time()
            X_train_update, X_test_update, y_train_update, y_test_update = train_test_split(data_df_update, labels_df, test_size = 0.35, random_state= count)
            rf_classifier_update = RandomForestClassifier(n_estimators=100, random_state=42)
            rf_classifier_update.fit(X_train_update, y_train_update)
            y_pred_update = rf_classifier_update.predict(X_test_update)
            prob_update = rf_classifier_update.predict_proba(X_test_update)
            f1scores_update.append(f1_score(y_test_update, y_pred_update, average = 'micro'))
    
    print(f'Mean F1 Score for the model is :: {np.mean(f1scores_update)}')
    print(f'Standard Deviation of F1 Score for the model is :: {np.std(f1scores_update)}') 
    print("--- %s seconds ---" % (time.time() - start_time))
    print('##################################################')
    print('###############')
    print(f'Data type of X_Train is:: {type(X_train_update)}')
    print(f'Data type of y_train is:: {type(y_train_update)}')

    
    
    
    # X_train_update, X_test_update, y_train_update, y_test_update = split(data_df_update, labels_df)
    # # print(f'counter is :: {count+1}')
    # start_time = time.time()
    # #Training the RF Classifier model-
    # rf_classifier_update = RandomForestClassifier(n_estimators=100, random_state=42)
    # rf_classifier_update.fit(X_train_update, y_train_update)
    # y_pred_update = rf_classifier_update.predict(X_test_update)
    # prob_update = rf_classifier_update.predict_proba(X_test_update)
    # f1scores_update.append(f1_score(y_test_update,y_pred_update,average='micro'))

    
    # print(f'Mean F1 Score for the model is :: {np.mean(f1scores_update)}')
    # print(f'Standard Deviation of F1 Score for the model is :: {np.std(f1scores_update)}') 
    # print("--- %s seconds ---" % (time.time() - start_time))
    # print('##################################################')
    # print('###############')
    # print(f'Data type of X_Train is:: {type(X_train_update)}')
    # print(f'Data type of y_train is:: {type(y_train_update)}')
    
    
    
    
    
    
    
    

    # ##################################################################################
    # #FINAL TERAINING WITH OPTIMAL FEATURE SPACE
    # f1scoresupdate = []
    # for count in range(10):
    #     print(f'counter is :: {count+1}')
    #     Trainupdate,Testupdate=[],[]
    #     Trainlabelupdate,Testlabelupdate=[],[]
    #     kfupdate = StratifiedKFold(n_splits=10,shuffle=True)  
    #     for train_index, test_index in kfupdate.split(data, label):
    #         Trainupdate.append(data[train_index,:])
    #         Testupdate.append(data[test_index,:])
    #         Trainlabelupdate.append(label[train_index])
    #         Testlabelupdate.append(label[test_index])

    #     for k in range(10):
    #         Classifierupdate = RandomForestClassifier(n_estimators=100) 
    #         scalerupdate = StandardScaler()
    #         train_dataupdate = scalerupdate.fit_transform( Trainupdate[k])
    #         test_dataupdate = scalerupdate.transform(Testupdate[k])
    #         Classifierupdate.fit(train_dataupdate,np.ravel(Trainlabelupdate[k] ))
    #         y_predupdate = Classifierupdate.predict(test_dataupdate)
    #         f1scoresupdate.append(f1_score(Testlabelupdate[k],y_predupdate,average='micro'))
                    
        

    #HERE WE SAVE THE MODEL USING JOBLIB.DUMP
    # joblib.dump(rf_classifier, f'{path}/Model_All_Features.joblib')
    model_all_path = f'{path}/Model_All_Features.pkl'
    with open(model_all_path, 'wb') as f:
        cloudpickle.dump(rf_classifier, f)
    model_optimized_path = f'{path}/Model_Optimized_Features.pkl'
    with open(model_optimized_path, 'wb') as f:
        cloudpickle.dump(rf_classifier_update, f)
    # joblib.dump(Classifierupdate, './Model_Optimized_Features.joblib')
    df.to_csv(f'{path}/Landslide_Types.csv')
    return prob, prob_update    