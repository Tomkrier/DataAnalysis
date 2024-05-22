import pandas as pd
from apriori import calcu_apriori


def load_data(fname):
    df = pd.read_csv(fname)
    # print(df.head())
    return df


dataset = load_data("招聘数据集(含技能列表).csv")
lst = list(dataset['skill_list'])
skill_list = [s.split(',') for s in lst]
big, biga = calcu_apriori(skill_list, 0.1, savefile="apriori.bin")
