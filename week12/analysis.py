from pathlib import Path
import pandas as pd

base = Path(__file__).resolve().parent
df = pd.read_csv(base / "scores_2026.csv")

def 정제(df):
    df = df.copy()

    # 점수가 비어 있는 행을 삭제한다.
    df = df.dropna(subset=["점수"])
    print(f"점수 결측 행 삭제 후: {len(df)}행")

    # 반과 과목 값의 앞뒤 공백을 제거한다.
    df["반"] = df["반"].str.strip()
    df["과목"] = df["과목"].str.strip()
    print(f"공백 제거 후: {len(df)}행")

    # 공백 정리 후 모든 열의 값이 같은 중복 행을 삭제한다.
    df = df.drop_duplicates()
    print(f"중복 행 삭제 후: {len(df)}행")

    # 점수가 0점 이상 100점 이하인 행만 남긴다.
    df = df[df["점수"].between(0, 100)]
    df["점수"] = df["점수"].astype(int)
    print(f"점수 범위 정리 후: {len(df)}행")

    return df


if __name__ == "__main__":
    print("\n정제 함수 실행 시작")
    df_cleaned = 정제(df)
    print(f"정제 완료: {df_cleaned.shape[0]}행 {df_cleaned.shape[1]}열")
    print(f"정제 후 중복 행 수: {df_cleaned.duplicated().sum()}행")
    print(f"정제 후 반 종류: {sorted(df_cleaned['반'].unique())}")
    print(f"정제 후 과목 종류: {sorted(df_cleaned['과목'].unique())}")
    print(f"정제 후 점수 범위: {df_cleaned['점수'].min()}~{df_cleaned['점수'].max()}")
    print("정제된 데이터 앞 5행:")
    print(df_cleaned.head())

    # 과목이 '수학'인 행만 남기기
    df_math = df_cleaned[df_cleaned["과목"] == "수학"]
    print(f"과목이 '수학'인 행 수: {len(df_math)}행")

    # '반'으로 묶어 점수 평균 계산
    avg_by_class = df_cleaned.groupby("반")["점수"].mean().reset_index()
    print("반별 점수 평균:")
    print(avg_by_class)

    # '과목'과 '반' 두 기준으로 묶어 점수 평균 계산
    avg_by_subject_class = df_cleaned.groupby(["과목", "반"])["점수"].mean().reset_index()
    print("과목 및 반별 점수 평균:")
    print(avg_by_subject_class)

    # '반'으로 묶어 개수, 평균, 중앙값, 최댓값 계산
    summary_by_class = df_cleaned.groupby("반")["점수"].agg(['count', 'mean', 'median', 'max']).reset_index()
    summary_by_class = summary_by_class.round(2)  # 소수 둘째 자리까지 반올림
    print("반별 점수 요약 통계:")
    print(summary_by_class)