import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 설정
font_path = '/NanumGothic/29131424179.ttf'
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.family'] = font_manager.FontProperties(fname=font_path).get_name()


# 데이터 로드
@st.cache_data
def load_data():
    data = pd.read_excel('label_survey.xlsx')
    mapping = {
        'SQ3_1': {
            1: '서울', 2: '부산', 3: '대구', 4: '인천', 5: '광주', 6: '대전',
            7: '울산', 8: '경기', 9: '강원', 10: '충북', 11: '충남', 12: '전북',
            13: '전남', 14: '경북', 15: '경남', 16: '제주', 17: '세종'
        },
        'SQ2_1': {
            1: '만 40대', 2: '만 50대', 3: '만 60대'
        },
        'Q2': {
            1: '시골', 2: '도시'
        },
        'Q3_1': {
            1: '60대 이하', 2: '70대 초반(70-75)', 3: '70대 후반(76-79)', 4: '80대 초반 (80-85)', 5: '80대 후반 (86-90)', 6: '90대 이상'
        },
        'Q3_2': {
            1: '60대 이하', 2: '70대 초반(70-75)', 3: '70대 후반(76-79)', 4: '80대 초반 (80-85)', 5: '80대 후반 (86-90)', 6: '90대 이상'
        },
        'Q3_3': {
            1: '60대 이하', 2: '70대 초반(70-75)', 3: '70대 후반(76-79)', 4: '80대 초반 (80-85)', 5: '80대 후반 (86-90)', 6: '90대 이상'
        },
        'Q3_4': {
            1: '60대 이하', 2: '70대 초반(70-75)', 3: '70대 후반(76-79)', 4: '80대 초반 (80-85)', 5: '80대 후반 (86-90)', 6: '90대 이상'
        },
        'Q3_5': {
            1: '60대 이하', 2: '70대 초반(70-75)', 3: '70대 후반(76-79)', 4: '80대 초반 (80-85)', 5: '80대 후반 (86-90)', 6: '90대 이상'
        },
        'Q3_6': {
            1: '60대 이하', 2: '70대 초반(70-75)', 3: '70대 후반(76-79)', 4: '80대 초반 (80-85)', 5: '80대 후반 (86-90)', 6: '90대 이상'
        }
    }
    data.replace(mapping, inplace=True)
    return data

data = load_data()

# streamlit 시작
st.title('설문조사 결과 시각화')
시도 = st.selectbox('시도 선택', ['', '서울', '부산', '대구', '인천', '광주', '대전', '울산', '경기', '강원', '충북', '충남', '세종', '전남', '전북', '경북', '경남', '제주'])
작성자_나이대 = st.selectbox('조사자 나이대', ['', '만 40대', '만 50대', '만 60대'])

부모님_시골 = st.selectbox('부모님 시골 거주 유무', ['', '도시', '시골'])
부모님_나이대 = st.selectbox('부모님 나이대', ['', '60대 이하', '70대 초반(70-75)', '70대 후반(76-79)', '80대 초반 (80-85)', '80대 후반 (86-90)', '90대 이상'])

# 필터링 조건 생성
filter_conditions = pd.Series([True] * len(data))

if 시도:
    filter_conditions &= (data['SQ3_1'] == 시도)
if 작성자_나이대:
    filter_conditions &= (data['SQ2_1'] == 작성자_나이대)
if 부모님_시골:
    filter_conditions &= (data['Q2'] == 부모님_시골)
if 부모님_나이대:
    filter_conditions &= data[['Q3_1', 'Q3_2', 'Q3_3', 'Q3_4', 'Q3_5', 'Q3_6']].apply(
        lambda row: 부모님_나이대 in row.values, axis=1
    )

# 필터링
filtered_df = data[filter_conditions]

# 시각화 함수 정의
def plot_data(filtered_df):
    # 부모님을 대신한 경험
    st.header('SQ5. 부모님을 대신한 경험')
    experience_columns = ['SQ5_1', 'SQ5_2', 'SQ5_3', 'SQ5_4', 'SQ5_5', 'SQ5_6', 'SQ5_7']
    experience_counts = filtered_df[experience_columns].apply(pd.Series.value_counts).fillna(0).sum(axis=1)
    st.bar_chart(experience_counts)

    # 부모님 시골 거주 여부
    st.header('Q2. 부모님이 시골에 거주하고 계신가요?')
    parent_rural_counts = filtered_df['Q2'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(parent_rural_counts, labels=parent_rural_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title('부모님 시골 거주 여부')
    st.pyplot(fig)

    # 부모님 연령대
    st.header('Q3. 부모님 연령대')
    parent_age_columns = ['Q3_1', 'Q3_2', 'Q3_3', 'Q3_4', 'Q3_5', 'Q3_6']
    parent_age_counts = filtered_df[parent_age_columns].apply(pd.Series.value_counts).fillna(0).sum(axis=1)
    st.bar_chart(parent_age_counts)

    # 부모님의 주 구매처에서 식료품과 생필품을 구매하는 주기
    st.header('Q5. 부모님께서 주 구매처에서 식료품과 생필품을 구매하는 주기')
    purchase_frequency_counts = filtered_df['Q5'].value_counts()
    st.bar_chart(purchase_frequency_counts)

    # 식료품 및 생필품 구매처
    st.header('Q6. 식료품 및 생필품 구매처')
    purchase_location_columns = ['Q6_1', 'Q6_2', 'Q6_3', 'Q6_4', 'Q6_5', 'Q6_6', 'Q6_7']
    purchase_location_counts = filtered_df[purchase_location_columns].apply(pd.Series.value_counts).fillna(0).sum(axis=1)
    st.bar_chart(purchase_location_counts)

    # 오프라인 구매처까지의 이동 시간
    st.header('Q8. 식자재 및 생필품 오프라인 구매처까지의 이동 시간')
    travel_time_counts = filtered_df['Q8'].value_counts()
    st.bar_chart(travel_time_counts)

    # 보통 구매하는 식료품 종류
    st.header('Q9. 보통 구매하는 식료품 종류')
    food_types_columns = ['Q9_1', 'Q9_2', 'Q9_3', 'Q9_4', 'Q9_5', 'Q9_6', 'Q9_7', 'Q9_8', 'Q9_9', 'Q9_10']
    food_types_counts = filtered_df[food_types_columns].apply(pd.Series.value_counts).fillna(0).sum(axis=1)
    st.bar_chart(food_types_counts)

    # 오프라인 구매를 선호하는 생필품 종류
    st.header('Q10. 오프라인 구매를 선호하는 생필품 종류')
    essential_goods_columns = ['Q10_1', 'Q10_2', 'Q10_3', 'Q10_4', 'Q10_5', 'Q10_6', 'Q10_7']
    essential_goods_counts = filtered_df[essential_goods_columns].apply(pd.Series.value_counts).fillna(0).sum(axis=1)
    st.bar_chart(essential_goods_counts)

    # 오프라인 매장에서 식자재 및 생필품 구매 시 어려움
    st.header('Q11. 오프라인 매장에서 식자재 및 생필품 구매 시 어려움')
    purchase_difficulty_columns = ['Q11_1', 'Q11_2', 'Q11_3', 'Q11_4', 'Q11_5']
    purchase_difficulty_counts = filtered_df[purchase_difficulty_columns].apply(pd.Series.value_counts).fillna(0).sum(axis=1)
    st.bar_chart(purchase_difficulty_counts)

    # 시골 거주로 겪는 서비스 절차 및 문제점
    st.header('Q12. 시골 거주로 겪는 서비스 절차 및 문제점')
    rural_issues_columns = ['Q12_1', 'Q12_2', 'Q12_3', 'Q12_4', 'Q12_5', 'Q12_6', 'Q12_7', 'Q12_8']
    rural_issues_counts = filtered_df[rural_issues_columns].apply(pd.Series.value_counts).fillna(0).sum(axis=1)
    st.bar_chart(rural_issues_counts)

    # 이동형 상점 서비스 사용 의사
    st.header('Q13. 이동형 상점 서비스 사용 의사')
    service_use_intent_counts = filtered_df['Q13'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(service_use_intent_counts, labels=service_use_intent_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title('이동형 상점 서비스 사용 의사')
    st.pyplot(fig)

    # Q14. 이동형 상점을 이용할 의사가 있다면 그 이유는 무엇입니까?
    st.header('Q14. 이동형 상점을 이용할 의사가 있다면 그 이유는 무엇입니까?')
    q14_counts = filtered_df['Q14'].value_counts()
    st.bar_chart(q14_counts)

    # Q15. 이 이동형 상점 트럭은 얼마나 자주 방문하는 것이 이상적이라고 생각합니까?
    st.header('Q15. 이 이동형 상점 트럭은 얼마나 자주 방문하는 것이 이상적이라고 생각합니까?')
    q15_counts = filtered_df['Q15'].value_counts()
    st.bar_chart(q15_counts)

    # Q16. 귀하의 부모님을 위하여 미스터아빠의 이동형 트럭의 적절한 방문 시간은 언제가 좋을 것 같습니까?
    st.header('Q16. 귀하의 부모님을 위하여 미스터아빠의 이동형 트럭의 적절한 방문 시간은 언제가 좋을 것 같습니까?')
    q16_counts = filtered_df['Q16'].value_counts()
    st.bar_chart(q16_counts)

    # Q17. 이동형 상점이 운영하는데 있어서 부모님을 위해 물건을 구매해 드리는 당신의 구매의사결정에 가장 중요한 것은 무엇이라고 생각하시나요?
    st.header('Q17. 이동형 상점이 운영하는데 있어서 부모님을 위해 물건을 구매해 드리는 당신의 구매의사결정에 가장 중요한 것은 무엇이라고 생각하시나요?')
    q17_counts = filtered_df['Q17'].value_counts()
    st.bar_chart(q17_counts)

    # Q18. 이동형 상점에서 판매하는 제품들의 가격대는 어느 정도가 적합한 것 같습니까?
    st.header('Q18. 이동형 상점에서 판매하는 제품들의 가격대는 어느 정도가 적합한 것 같습니까?')
    q18_counts = filtered_df['Q18'].value_counts()
    st.bar_chart(q18_counts)

    # Q19. [미스터아빠 이동형 상점을 통해 구매 시 관심제품]
    st.header('Q19. 미스터아빠 이동형 상점을 통해 구매 시 관심제품')
    q19_columns = ['Q19_1', 'Q19_2', 'Q19_3', 'Q19_4', 'Q19_5', 'Q19_6', 'Q19_7', 'Q19_8']
    q19_counts = filtered_df[q19_columns].apply(pd.Series.value_counts).fillna(0).sum(axis=1)
    st.bar_chart(q19_counts)

    # Q20. 부모님께서 얼마나 자주 병원 혹은 약국 등에 방문하시나요?
    st.header('Q20. 부모님께서 얼마나 자주 병원 혹은 약국 등에 방문하시나요?')
    q20_counts = filtered_df['Q20'].value_counts()
    st.bar_chart(q20_counts)

    # Q21. [구매용의가 높거나 도움이 된다고 평가할 것 같은 제품류]
    st.header('Q21. 구매용의가 높거나 도움이 된다고 평가할 것 같은 제품류')
    q21_columns = ['Q21_1', 'Q21_2', 'Q21_3', 'Q21_4', 'Q21_5', 'Q21_6', 'Q21_7', 'Q21_8', 'Q21_9']
    q21_counts = filtered_df[q21_columns].apply(pd.Series.value_counts).fillna(0).sum(axis=1)
    st.bar_chart(q21_counts)

    # Q22. 만약 미스터아빠의 이동형 상점이 어르신들이 건강 문제와 식사 제한 때문에 먹지 못했던 음식을 먹어볼 수 있는 대안을 제공한다면, 부모님께서는 구매하실 의향이 있으실 것 같습니까?
    st.header('Q22. 미스터아빠의 이동형 상점이 어르신들이 건강 문제와 식사 제한 때문에 먹지 못했던 음식을 먹어볼 수 있는 대안을 제공한다면, 부모님께서는 구매하실 의향이 있으실 것 같습니까?')
    q22_counts = filtered_df['Q22'].value_counts()
    st.bar_chart(q22_counts)

    # Q23. [다양하고 건강에 좋은 식재료 및 구매 옵션 제공 시 구매 선호 예상 카테고리]
    st.header('Q23. 다양한 건강 식재료 및 구매 옵션 제공 시 선호 카테고리')
    q23_columns = ['Q23_1', 'Q23_2', 'Q23_3', 'Q23_4', 'Q23_5', 'Q23_6', 'Q23_7']
    q23_counts = filtered_df[q23_columns].apply(pd.Series.value_counts).fillna(0).sum(axis=1)
    st.bar_chart(q23_counts)

    # Q24. 미스터아빠의 이동형 상점에서 배달 서비스 제공 시, 부모님께서 맞춤형 배송 서비스에 대해 선호하시는 방식이 무엇입니까?
    st.header('Q24. 미스터아빠의 이동형 상점에서 배달 서비스 제공 시 선호 방식')
    q24_counts = filtered_df['Q24'].value_counts()
    st.bar_chart(q24_counts)

    # Q25. 귀하는 평소 온라인 쇼핑을 자주 이용하십니까?
    st.header('Q25. 평소 온라인 쇼핑을 자주 이용하십니까?')
    q25_counts = filtered_df['Q25'].value_counts()
    st.bar_chart(q25_counts)

    # Q26. 귀하는 얼마나 자주 온라인 쇼핑을 하십니까?
    st.header('Q26. 얼마나 자주 온라인 쇼핑을 하십니까?')
    q26_counts = filtered_df['Q26'].value_counts()
    st.bar_chart(q26_counts)

    # Q27. [식료품 소비 위해 이용하는 온라인 쇼핑몰]
    st.header('Q27. 식료품 소비 위해 이용하는 온라인 쇼핑몰')
    q27_columns = ['Q27_1', 'Q27_2', 'Q27_3', 'Q27_4', 'Q27_5']
    q27_counts = filtered_df[q27_columns].apply(pd.Series.value_counts).fillna(0).sum(axis=1)
    st.bar_chart(q27_counts)

    # Q28. 귀하께서는 미스터아빠의 이동형 상점에서 제품 업데이트를 얼마나 자주 받고 싶으신가요?
    st.header('Q28. 미스터아빠 이동형 상점 제품 업데이트 빈도')
    q28_counts = filtered_df['Q28'].value_counts()
    st.bar_chart(q28_counts)

    # Q29. 어떤 종류의 제품 업데이트를 받고 싶으신가요?
    st.header('Q29. 받고 싶은 제품 업데이트 종류')
    q29_counts = filtered_df['Q29'].value_counts()
    st.bar_chart(q29_counts)

    # Q30. 어떤 방법으로 미스터아빠의 이동형 상점으로부터 업데이트를 받고 싶으신가요?
    st.header('Q30. 제품 업데이트 방법 선호')
    q30_counts = filtered_df['Q30'].value_counts()
    st.bar_chart(q30_counts)

    # Q31. 언제 미스터아빠의 이동형 상점으로부터 커뮤니케이션을 받기를 원하시나요?
    st.header('Q31. 커뮤니케이션 받기를 원하는 시간')
    q31_counts = filtered_df['Q31'].value_counts()
    st.bar_chart(q31_counts)

    # Q32. 정기 배송을 위한 구독 서비스에 관심 있으신가요?
    st.header('Q32. 정기 배송 구독 서비스 관심 여부')
    q32_counts = filtered_df['Q32'].value_counts()
    st.bar_chart(q32_counts)

    # Q33. 모바일 상점 앱에서 가장 중요하게 생각하는 기능은 무엇인가요?
    st.header('Q33. 모바일 상점 앱에서 가장 중요하게 생각하는 기능')
    q33_counts = filtered_df['Q33'].value_counts()
    st.bar_chart(q33_counts)

# 필터링된 데이터를 기반으로 시각화
plot_data(filtered_df)
