import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.formula.api import ols, glm

# 데이터 로드
today = pd.read_csv('./today.csv', header = 0, engine = 'python', encoding='euc-kr')

today.shape
print(today.info())
today.columns = today.columns.str.replace(' ', '_')
today.head()

print(today.describe())
sorted(today.e.unique())
print(today.e.value_counts())

today_e = today.loc['e']

sns.set_style('dark')
sns.distplot(today_e, kde = True, color = "red", label = 'End Price')

plt.title("End Price")
plt.legend()
plt.show()
