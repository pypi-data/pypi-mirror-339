from Landsifier_DataPreparation import *
from Landsifier_DataPreparation import read_shapefiles
from Landsifier_ML_Training import *
# from joblib import dump, load
import cloudpickle
import pandas as pd



def LoadModel(path, optimized_features):
    if optimized_features:
        print("Optimized Model is being loaded")
        model_path = path+'/Model_Optimized_Features.pkl'
        with open(model_path, 'rb') as f:
            models = cloudpickle.load(f)
    else:
        print("Model with all features is being loaded")
        model_path = path+'/Model_All_Features.pkl'
        with open(model_path, 'rb') as f:
            models = cloudpickle.load(f)
        return models
    

def prediction(path, shp_path, dem_location, inventory_name, kk, switch, optimized_features):
    shapefile = read_shapefiles(shp_path)
    features = Feature_Engineering(shp_path = shp_path, column_name= None, dem_location = dem_location, inventory_name = inventory_name, kk = kk, switch = switch)
    df_features = pd.DataFrame(features)
    model = LoadModel(path, optimized_features)
    
    if optimized_features:   
        imp_features_df = pd.read_csv(f"{path}/Optimized_Features.csv")
        print(f"{imp_features_df}")
        features_df = df_features
        imp_features = imp_features_df['0'].tolist()
        features_df =features_df.iloc[:,imp_features]
        prediction = model.predict(features_df)
        prediction_df = pd.Series(prediction, name = 'Landslide Types')
        prediction_gpd = gpd.GeoDataFrame(prediction_df, geometry= shapefile.geometry)
        prediction_gpd.head()
        # To export the final predicted shapefile
        # prediction_gpd.to_file(path+'/predictions.shp', driver = 'ESRI Shapefile')
        return prediction_gpd
        
        # prediction_proba = model.predict_proba(features)
        # prediction_proba_df = pd.Series(prediction_proba)
        
        ############################################
        # Take a look later
        ############################################
        # csv_df = pd.read_csv(csv_path)
        # old_values_column = 'Values'
        # new_values_column = 'Landslide Type'
        # replacement_dict = csv_df.set_index(old_values_column)[new_values_column].to_dict()
        # prediction_df = prediction_df.replace(replacement_dict)
        ############################################
        
    else:
        # csv_path = path+'/Landslide_Types.csv'
        features_df = df_features
        prediction = model.predict(features_df)
        prediction_df = pd.Series(prediction, name = 'Landslide Types')
        
        prediction_gpd = gpd.GeoDataFrame(prediction_df, geometry= shapefile.geometry)
        prediction_gpd.head()
        
        # To export the final predicted shapefile
        # prediction_gpd.to_file(path+'/predictions.shp', driver = 'ESRI Shapefile')
        return prediction_gpd
        
        