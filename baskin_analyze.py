import warnings
warnings.filterwarnings('ignore')
# warning 메시지 제거, warning 메시지는 라이브러리 업데이트나 사용법에 대한 안내 등이 있습니다.
# 코딩을 처음 시작할 때는  warning 메시지가 나오면 당황하실 수도 있어서 제거를 하고 보도록 합니다.
# warning 메시지는 제거하고 보셔도 되지만 Error 메시지를 꼭 고쳐주셔야 합니다.
warnings.filterwarnings('ignore', 'This pattern has match groups')
warnings.filterwarnings('ignore', 'The iterable function was deprecated in Matplotlib')

from matplotlib import font_manager



import pandas as pd
import numpy as np

import seaborn as sns
# 지도 시각화를 위해
import folium

import matplotlib.pyplot as plt
from IPython.display import set_matplotlib_formats
import IPython.display as display


# Window 의 한글 폰트 설정
plt.rc('font',family='Malgun Gothic')
# Mac 의 한글 폰트 설정
# plt.rc('font', family='AppleGothic')
plt.rc('axes', unicode_minus=False)

set_matplotlib_formats('retina')
# data_load
shop_2018 = pd.read_csv(r'C:\Users\ymecc\Desktop\programming\graph\소상공인시장진흥공단_상가(상권)정보_20200930\소상공인시장진흥공단_상가(상권)정보_전북_202009.csv',
                        encoding='cp949' , error_bad_lines=False)

coffee = shop_2018[shop_2018['상권업종소분류명'].str.contains('커피',na=False)]
print(coffee.shape)
													

print(coffee.loc[coffee['상호명'].str.contains('스타벅스|starbucks|STARBUCKS'), '상호명'].unique())
df_JB = shop_2018.loc[shop_2018['시도명'].str.startswith('전라북도',na=False)].copy()
print(df_JB['상권업종대분류명'].value_counts())

print(df_JB.describe(include=np.object))

df_JB[['위도', '경도']].describe(include=np.number)

df_fast_food = df_JB.loc[df_JB['상권업종중분류명']=="패스트푸드"]

# 베스킨라빈스와 던킨도넛  입지 분석
df_31 = df_fast_food[df_fast_food['상호명'].str.contains("베스킨라빈스|던킨")]
df_31 = df_31[['상호명', '지점명', '상권업종대분류명', '상권업종중분류명', 
               '지번주소', '도로명주소',  '위도', '경도', '시군구명', '행정동명']].copy()

# df_31.loc[df_31['상호명'].str.contains('배스킨'), '브랜드명'] = '배스킨라빈스'
# df_31.loc[df_31['상호명'].str.contains('던킨'), '브랜드명'] = '던킨도너츠'

# 각 총 점호수를 count 해보자
df_31_group_count = df_31['상호명'].value_counts()
df_ratio = df_31_group_count[0]/df_31_group_count[1]
print("제공된 데이터로 보았을때, 전라북도에 던킨보다 배스킨라빈스가 {0:.2f}배 많습니다.".format(df_ratio))

df_31['위도'] = df_31['위도'].astype(float)

df_31['경도'] = df_31['경도'].astype(float)
# df_31.plot.scatter(x='위도',y='경도')
# print(df_31.head())
# sns.scatterplot(data=df_31,x='위도',y='경도',hue="브랜드명")


# 지도 설정----------------------------------------------------------------------------
# geo_df = df_31.copy().fillna(method="ffill")
geo_df = df_31.fillna(method="bfill")
# print(geo_df['상호명'])

# 지도를 초기화 해줄 때 어디를 중심으로 보여줄지 설정합니다.
# 우리가 가져온 데이터프레임 안에 있는 데이터를 기준으로 출력할 수 있도록 위경도의 평균값을 구해옵니다.
# map = folium.Map(location=[geo_df['위도'].mean(), geo_df['경도'].mean()], zoom_start=12)


geo_df = geo_df.copy()

# 지도를 초기화 해줄 때 어디를 중심으로 보여줄지 설정합니다.
# 우리가 가져온 데이터프레임 안에 있는 데이터를 기준으로 출력할 수 있도록 위경도의 평균값을 구해옵니다.
map = folium.Map(location=[geo_df['위도'].mean(), geo_df['경도'].mean()], zoom_start=12, tiles='Stamen Toner')


# ---------------------tiles 세팅 값 모음.
# - Open street map (기본 값입니다.)
# - Map Quest Open
# - MapQuest Open Aerial
# - Mapbox Bright
# - Mapbox Control Room
# - Stamenterrain
# - Stamentoner
# - Stamenwatercolor
# - cartodbpositron
# - cartodbdark_matter
# print(geo_df.isnull().sum())
for n in geo_df.index:
    # 팝업에 들어갈 텍스트를 지정해 줍니다.
    popup_name = str(geo_df.loc[n, '상호명']) + ' - ' + str(geo_df.loc[n, '도로명주소'])
    # 브랜드명에 따라 아이콘 색상을 달리해서 찍어줍니다.
    if geo_df['상호명'][n] == '던킨도너츠' :
        icon_color = 'red'
    else:
        icon_color = 'blue'    
    print(icon_color)
    folium.CircleMarker(
        location=[geo_df['위도'][n], geo_df['경도'][n]],
        radius=5,
        popup=popup_name,
        color= icon_color,
        fill=True,
        fill_color=icon_color
    ).add_to(map)
    
map.save('./location_map.html')