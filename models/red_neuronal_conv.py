import joblib
import numpy as np
import pandas as pd
import keras
import sklearn
import tensorflow as tf
import tensorflow
from keras.optimizers import *
from tensorflow.python import tf2
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler
from sklearn.preprocessing import normalize
from joblib import dump, load

def redNeuronalconvolucional(prueba):
  new_model = keras.models.load_model("/home/kali/Escritorio/rest_API/models/redneuronalconvolucional.h5")
  prueba=pd.read_csv(prueba)
  prueba=prueba.reindex(columns=['dst_port','flow_duration','tot_fwd_pkts','tot_bwd_pkts','totlen_fwd_pkts','totlen_bwd_pkts', 'fwd_pkt_len_max', 'fwd_pkt_len_min','fwd_pkt_len_mean', 'fwd_pkt_len_std', 'bwd_pkt_len_max','bwd_pkt_len_min', 'bwd_pkt_len_mean','bwd_pkt_len_std','flow_byts_s','flow_pkts_s','flow_iat_mean','flow_iat_std','flow_iat_max','flow_iat_min','fwd_iat_tot','fwd_iat_mean', 'fwd_iat_std','fwd_iat_max', 'fwd_iat_min','bwd_iat_tot','bwd_iat_mean','bwd_iat_std','bwd_iat_max','bwd_iat_min','fwd_psh_flags','bwd_psh_flags','fwd_urg_flags', 'bwd_urg_flags','fwd_header_len', 'bwd_header_len','fwd_pkts_s','bwd_pkts_s','pkt_len_min','pkt_len_max','pkt_len_mean', 'pkt_len_std', 'pkt_len_var','fin_flag_cnt','syn_flag_cnt','rst_flag_cnt', 'psh_flag_cnt', 'ack_flag_cnt','urg_flag_cnt','cwe_flag_count','ece_flag_cnt', 'down_up_ratio', 'pkt_size_avg','fwd_seg_size_avg', 'bwd_seg_size_avg','fwd_byts_b_avg', 'fwd_pkts_b_avg','fwd_blk_rate_avg','bwd_byts_b_avg','bwd_pkts_b_avg','bwd_blk_rate_avg','subflow_fwd_pkts','subflow_fwd_byts','subflow_bwd_pkts','subflow_bwd_byts','init_fwd_win_byts', 'init_bwd_win_byts','fwd_act_data_pkts','fwd_seg_size_min','active_mean','active_std','active_max', 'active_min','idle_mean','idle_std','idle_max', 'idle_min'])
  prueba = prueba.replace([np.inf,-np.inf],0)
  prueba = prueba.values
  norm= pd.DataFrame(normalize(prueba))
  norm=norm.to_numpy()
  kkl=norm.shape[1]
  llk=norm.shape[0]
  kkl=np.array(kkl)
  llk=np.array(llk)
  norm=norm.reshape((llk,1,kkl,1))
  prediccion= np.argmax(new_model.predict(norm),axis=1)
  le = preprocessing.LabelEncoder()
  le.fit(["BENIGN","DDoS", "DoS GoldenEye","DoS Hulk","DoS Slowhttptest","DoS slowloris"])
  LabelEncoder()
  ññ=le.inverse_transform(prediccion)
  yu=pd.DataFrame(ññ)
  yu.rename({0: 'Total'}, axis=1,inplace=True)
  benignos=yu[yu['Total']=='BENIGN'].count()
  ddos=yu[yu['Total']=='DDoS'].count()
  goldeneye=yu[yu['Total']=='DoS GoldenEye'].count()
  hulk=yu[yu['Total']=='DoS Hulk'].count()
  slowhttptest=yu[yu['Total']=='DoS Slowhttptest'].count()
  slowloris=yu[yu['Total']=='DoS slowloris'].count()
  benignos=int(benignos)
  slowloris=int(slowloris)
  ddos=int(ddos)
  goldeneye=int(goldeneye)
  hulk=int(hulk)
  slowhttptest=int(slowhttptest)
  return benignos,ddos,goldeneye,hulk,slowhttptest,slowloris

  
