#찾은 policy 결과 파일 읽기.
import numpy as np
import pandas as pd

npz_file_name = "policy_DeepAA_cifar_1"  #파일 사용 시 이부분만 수정하면 됨

npz_file = "./policy_port/"+ npz_file_name +".npz"
data=np.load(npz_file)
data_df = pd.DataFrame(data)

print("=================================policy_probs===================================")
print(data['policy_probs'])
print("======================================l_ops===========================================")
print(data['l_ops'])
print("============================l_mags=========================")
print(data['l_mags'])
print("===========================ops============================")
print(data['ops'])
print("===========================mags===========================")
print(data['mags'])
print("========================op_names==============================")
print(data['op_names'])