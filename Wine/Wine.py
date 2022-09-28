import pandas as pd

# 데이터 준비
red_df = pd.read_csv('./winequality-red.csv', sep = ';', header = 0, engine = 'python')
white_df = pd.read_csv('./winequality-white.csv', sep = ';', header = 0, engine= 'python')
red_df.to_csv('./winequality-red2.csv',index = False)
white_df.to_csv('./winequality-white2.csv', index = False)

# 레드 와인의 CSV 파일 타입 추가
red_df.head()
red_df.insert(0, column = 'type', value = 'red')
red_df.head()
red_df.shape

# 화이트 와인의 CSV 파일 타입 추가
white_df.head()
white_df.insert(0, column = 'type', value = 'white')
white_df.head()
white_df.shape

# 두 개의 CSV 파일 데이터 병합
wine = pd.concat([red_df, white_df])
wine.shape
wine.to_csv('./wine.csv', index = False)

# 데이터 탐색
print(wine.info())
wine.columns = wine.columns.str.replace(' ', '_')
wine.head()

# 데이터 모델링 - describe 함수로 그룹 비교
# type에 따라 그룹을 나눈 뒤, 종속 변수인 quality에 함수 사용
# 독립 변수 (x)는 type 부터 alcohol 까지 12개
# 종속 변수 (y)는 quality
# 실질적으로 기술 통계 구하는 부분
print(wine.describe())
sorted(wine.quality.unique())
print(wine.quality.value_counts())

# 개수, 평균, 표준편차, 최소값, 전체 데이터 백분율에 대한 백분위수
# 그룹 비교
print(wine.groupby('type')['quality'].describe())
print(wine.groupby('type')['quality'].mean())
print(wine.groupby('type')['quality'].std())
print(wine.groupby('type')['quality'].agg(['mean', 'std']))

# t-검정과 회귀 분석으로 그룹 비교
# t-검정이란 모집단의 분산이나 표준편차를 알지 못할 때 표본으로부터 추정된
# 분산이나 표준편차를 이용하여 두 모집단의 평균의 차이를 알아보는 검정 방법
from scipy import stats
from statsmodels.formula.api import ols, glm
red_wine_quality = wine.loc[wine['type'] == 'red', 'quality']
white_wine_quality = wine.loc[wine['type'] == 'white', 'quality']

# t-검정을 하고 두 그룹 간 차이를 확인한다.
print("\n===t-검정 후 그룹 간 차이===\n")
print(stats.ttest_ind(red_wine_quality, white_wine_quality, equal_var = False))

Rformula = 'quality ~ fixed_acidity + volatile_acidity + citric_acid + \
            residual_sugar + chlorides + free_sulfur_dioxide + \
            total_sulfur_dioxide + density + pH + sulphates + alcohol'
regression_result = ols(Rformula, data = wine).fit()

print(regression_result.summary())

# 회귀 분석 모델로 새로운 샘플의 품질 등급 예측하기
# 품질 등급을 예측하려면 먼저 독립 변수인 11개 속성에 대한 샘플 데이터가 필요함
sample1 = wine[wine.columns.difference(['quality', 'type'])]
sample1 = sample1[0:5][:]
sample1_predict = regression_result.predict(sample1)
print(sample1_predict)
wine[0:5]['quality']

# 임의의 data로 샘플 만들기
data = {"fixed_acidity" : [8.5, 8.1], "volatile_acidity":[0.8, 0.5],
"citric_acid":[0.3, 0.4], "residual_sugar":[6.1, 5.8], "chlorides":[0.055,
0.04], "free_sulfur_dioxide":[30.0, 31.0], "total_sulfur_dioxide":[98.0,
99], "density":[0.996, 0.91], "pH":[3.25, 3.01], "sulphates":[0.4, 0.35],
"alcohol":[9.0, 0.88]}

sample2 = pd.DataFrame(data, columns= sample1.columns)
print(sample2)
sample2_predict = regression_result.predict(sample2)
print(sample2_predict)

# 와인 유형에 따른 품질 등급 히스토그램 결과 시각화
import matplotlib.pyplot as plt
import seaborn as sns

# 차트 배경색
sns.set_style('dark')
# 레드 와인에 대한 distplot 객체 생성
sns.distplot(red_wine_quality, kde = True, color = "red", label = 'red wine')
# 화이트 화인 객체 생성
sns.distplot(white_wine_quality, kde = True, label = 'white wine')
plt.title("Quality of Wine Type")
plt.legend()
plt.show()

# 부분 회귀 플롯으로 시각화하기
import statsmodels.api as sm
others = list(set(wine.columns).difference(set(["quality", "fixed_acidity"])))
p, resids = sm.graphics.plot_partregress("quality", "fixed_acidity", others, data = wine, ret_coords = True)

# 각 독립 변수가 종속 변수 quality에 미치는 영향력을 시각화하기
fig = plt.figure(figsize = (8, 13))
sm.graphics.plot_partregress_grid(regression_result, fig = fig)
plt.show()