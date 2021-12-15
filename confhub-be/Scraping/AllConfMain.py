import pandas as pd
import re
import numpy as np

conf1 = pd.read_csv('conf1.csv')
conf2 = pd.read_csv('conf2.csv')
conf3 = pd.read_csv('conf3.csv')


df = pd.concat([conf1, conf2, conf3])
df['Name'] = [name.strip() for name in df['Name'].values]
df = df[~df.duplicated(subset=['Name','Date','Location'], keep='first')]
df.to_csv('AllConf.csv', header=True, index=False)




