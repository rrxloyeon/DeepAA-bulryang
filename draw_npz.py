#찾은 policy 결과 파일로 bar chart 그리기
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


a="nepes_pretrain_45epoch" #사용시 이부분 바꾸면됨
npz_file_name = "policy_DeepAA_2022-06-10-23-52-06-535119"  #사용시 이부분 바꾸면됨

img_name = "policy_port/" + a + ".png"
npz_file = "policy_port/"+ npz_file_name +".npz"
data=np.load(npz_file)
data_df = pd.DataFrame(data['policy_probs'])
#data_df1 = pd.DataFrame(data['l_ops']) #l_ops =18
#data_df2 = pd.DataFrame(data['l_mags']) #l_mags =13
data_df3 = pd.DataFrame(data['ops'])
data_df4 = pd.DataFrame(data['mags'])
data_df5 = pd.DataFrame(data['op_names'])

nb_policy = len(data['policy_probs'])
colors = sns.color_palette("Set3", len(data['op_names']))
op_prob = []
for i in range(len(data['op_names'])) :
    extract = data['policy_probs'][:, np.reshape(data['ops'],(-1,))==i]
    op_prob.append(np.sum(extract, axis=1))
    plt.bar(range(nb_policy), op_prob[i], bottom=np.sum(op_prob[:i], axis=0), label=data['op_names'][i], color=colors[i], edgecolor=colors[-1], linewidth=0.1)
plt.legend(bbox_to_anchor=(1.05, 1))
plt.tight_layout()
plt.savefig(img_name)





