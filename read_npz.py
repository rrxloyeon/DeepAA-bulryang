#찾은 policy 결과 파일 읽기
import numpy as np
import pandas as pd
import pdb

a="nepes_pretrain_45epoch" #사용시 이부분 바꾸면됨
npz_file_name = "policy_DeepAA_2022-06-10-23-52-06-535119"  #사용시 이부분 바꾸면됨

xlsx_name = "policy_port/" + a + ".xlsx"
npz_file = "policy_port/"+ npz_file_name +".npz"
data=np.load(npz_file)
data_df = pd.DataFrame(data['policy_probs'])
#data_df1 = pd.DataFrame(data['l_ops']) #l_ops =18
#data_df2 = pd.DataFrame(data['l_mags']) #l_mags =13
data_df3 = pd.DataFrame(data['ops'])
data_df4 = pd.DataFrame(data['mags'])
data_df5 = pd.DataFrame(data['op_names'])


with pd.ExcelWriter(xlsx_name) as writer:
    data_df.to_excel( writer, sheet_name = 'policy_probs')
    #data_df1.to_excel( writer, sheet_name = 'l_ops')
    #data_df2.to_excel( writer, sheet_name = 'l_mags')
    data_df3.to_excel( writer, sheet_name = 'ops')
    data_df4.to_excel( writer, sheet_name = 'mags')
    data_df5.to_excel( writer, sheet_name = 'op_names')


"""
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
"""
