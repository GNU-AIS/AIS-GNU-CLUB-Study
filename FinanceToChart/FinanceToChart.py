import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

def main():
    # 데이터 로드
    today = pd.read_csv('./today.csv', header = 0, thousands=',', engine = 'python', encoding='euc-kr')

    today.shape
    print(today.info())
    today.columns = today.columns.str.replace(' ', '_')
    today.head()

    print(today.describe())
    sorted(today.e.unique())
    print(today.e.value_counts())

    today_e = today.loc[:, 'e']

    sns.set_style('dark')
    sns.distplot(today_e, kde = True, color = "red", label = 'End Price')

    plt.title("End Price")
    plt.xlabel('종가')
    plt.ylabel('밀도')
    plt.legend()
    plt.show()
    

if __name__ == '__main__':
    font_location = 'NanumGothic.ttf'  #font 경로 설정
    font_name = fm.FontProperties(fname=font_location).get_name()
    plt.rc('font', family=font_name)
    sns.set(font="NanumGothic", rc={"axes.unicode_minus":False}, style='white')
    main()