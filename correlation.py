import pandas as pd

# 데이터 로드
def load_data(file_path):
    data = pd.read_excel('survey_result.xlsx')
    return data


# 이진 변수로 변환
def transform_to_binary(df, columns):
    transformed_df = df.copy()
    for col in columns:
        transformed_df[col] = transformed_df[col].apply(lambda x: 1 if pd.notna(x) else 0)
    return transformed_df


# 응답 두개 있을 때 이진변환
def binary_conversion(df, column_name):
    binary_mapping = {1: 0, 2: 1}
    df[column_name] = df[column_name].map(binary_mapping)
    return df


# 더미변수 만들기
def create_dummy_variables(df, column_name, drop_first=True):
    df = pd.get_dummies(df, columns=[column_name], drop_first=drop_first)
    return df


# 데이터 저장
def save_data(df, output_path):
    df.to_excel(output_path, index=False)


if __name__ == "__main__":
    # 데이터 파일 경로
    input_file_path = 'transformed_survey_result.xlsx'
    output_file_path = 'transformed_result.xlsx'

    # 변환할 컬럼 리스트
    columns_to_transform = ['SQ5_1', 'SQ5_2', 'SQ5_3', 'SQ5_4', 'SQ5_5', 'SQ5_6', 'SQ5_7',
                            'Q3_1', 'Q3_2', 'Q3_3', 'Q3_4', 'Q3_5', 'Q3_6',
                            'Q6_1', 'Q6_2', 'Q6_3', 'Q6_4', 'Q6_5', 'Q6_6', 'Q6_7',
                            'Q9_1', 'Q9_2', 'Q9_3', 'Q9_4', 'Q9_5', 'Q9_6', 'Q9_7', 'Q9_8', 'Q9_9','Q9_10',
                            'Q10_1', 'Q10_2', 'Q10_3', 'Q10_4', 'Q10_5', 'Q10_6', 'Q10_7',
                            'Q11_1', 'Q11_2', 'Q11_3', 'Q11_4', 'Q11_5',
                            'Q12_1', 'Q12_2', 'Q12_3', 'Q12_4', 'Q12_5', 'Q12_6', 'Q12_7', 'Q12_8',
                            'Q19_1', 'Q19_2', 'Q19_3', 'Q19_4', 'Q19_5', 'Q19_6', 'Q19_7', 'Q19_8',
                            'Q21_1', 'Q21_2', 'Q21_3', 'Q21_4', 'Q21_5', 'Q21_6', 'Q21_7', 'Q21_8', 'Q21_9',
                            'Q23_1', 'Q23_2', 'Q23_3', 'Q23_4', 'Q23_5', 'Q23_6', 'Q23_7',
                            'Q27_1', 'Q27_2', 'Q27_3', 'Q27_4', 'Q27_5']

    columns_to_dummy = ['SQ2_1', 'SQ4', 'SQ5', 'Q7', 'Q8', 'Q14', 'Q15', 'Q16', 'Q17', 'Q18',
                        'Q20', 'Q22', 'Q24', 'Q26', 'Q28', 'Q29', 'Q30', 'Q31', 'Q33']

    columns_to_binary = ['SQ1', 'Q2', 'Q13', 'Q25', 'Q32']

    # 데이터 로드
    data = load_data(input_file_path)

    # 선택한 컬럼을 이진 변수로 변환
    # transformed_data = transform_to_binary(data, columns_to_transform)

    # 변환된 데이터 저장
    #save_data(transformed_data, output_file_path)

    transformed = binary_conversion(data, columns_to_binary)


    print(f"Transformed data saved to {output_file_path}")
