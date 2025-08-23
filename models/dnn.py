import joblib
import numpy as np
import pandas as pd
import keras
import tensorflow as tf
from keras.optimizers import *
from sklearn.preprocessing import LabelEncoder, normalize
from sklearn import preprocessing

def dnn(csv_file):
    # Load pre-trained DNN model
    new_model = keras.models.load_model('models/redneuronal4.h5')
    
    # Read CSV dataset
    df = pd.read_csv(csv_file)
    
    # Reorder dataset columns to match training order
    df = df.reindex(columns=[
        'dst_port','flow_duration','tot_fwd_pkts','tot_bwd_pkts','totlen_fwd_pkts','totlen_bwd_pkts',
        'fwd_pkt_len_max','fwd_pkt_len_min','fwd_pkt_len_mean','fwd_pkt_len_std','bwd_pkt_len_max',
        'bwd_pkt_len_min','bwd_pkt_len_mean','bwd_pkt_len_std','flow_byts_s','flow_pkts_s','flow_iat_mean',
        'flow_iat_std','flow_iat_max','flow_iat_min','fwd_iat_tot','fwd_iat_mean','fwd_iat_std','fwd_iat_max',
        'fwd_iat_min','bwd_iat_tot','bwd_iat_mean','bwd_iat_std','bwd_iat_max','bwd_iat_min','fwd_psh_flags',
        'bwd_psh_flags','fwd_urg_flags','bwd_urg_flags','fwd_header_len','bwd_header_len','fwd_pkts_s',
        'bwd_pkts_s','pkt_len_min','pkt_len_max','pkt_len_mean','pkt_len_std','pkt_len_var','fin_flag_cnt',
        'syn_flag_cnt','rst_flag_cnt','psh_flag_cnt','ack_flag_cnt','urg_flag_cnt','cwe_flag_count',
        'ece_flag_cnt','down_up_ratio','pkt_size_avg','fwd_seg_size_avg','bwd_seg_size_avg','fwd_byts_b_avg',
        'fwd_pkts_b_avg','fwd_blk_rate_avg','bwd_byts_b_avg','bwd_pkts_b_avg','bwd_blk_rate_avg',
        'subflow_fwd_pkts','subflow_fwd_byts','subflow_bwd_pkts','subflow_bwd_byts','init_fwd_win_byts',
        'init_bwd_win_byts','fwd_act_data_pkts','fwd_seg_size_min','active_mean','active_std','active_max',
        'active_min','idle_mean','idle_std','idle_max','idle_min'
    ])
    
    # Replace infinite values with 0
    df = df.replace([np.inf, -np.inf], 0)
    
    # Normalize values
    values = df.values
    normalized = pd.DataFrame(normalize(values))
    
    # Make predictions
    predictions = np.argmax(new_model.predict(normalized), axis=1)
    
    # Decode predictions to original labels
    label_encoder = preprocessing.LabelEncoder()
    label_encoder.fit(["BENIGN","DDoS","DoS GoldenEye","DoS Hulk","DoS Slowhttptest","DoS slowloris"])
    decoded = label_encoder.inverse_transform(predictions)
    
    # Convert to DataFrame
    results_df = pd.DataFrame(decoded, columns=['Label'])
    
    # Count predictions
    benign = int(results_df[results_df['Label'] == 'BENIGN'].count())
    ddos = int(results_df[results_df['Label'] == 'DDoS'].count())
    goldeneye = int(results_df[results_df['Label'] == 'DoS GoldenEye'].count())
    hulk = int(results_df[results_df['Label'] == 'DoS Hulk'].count())
    slowhttptest = int(results_df[results_df['Label'] == 'DoS Slowhttptest'].count())
    slowloris = int(results_df[results_df['Label'] == 'DoS slowloris'].count())
    
    return benign, ddos, goldeneye, hulk, slowhttptest, slowloris
