# Air_Quality_Prediction
시계열 데이터를 바탕으로 1일 후 미세먼지 농도를 예측하는 모델 개발 프로젝트
<br>
<br>
<br>

## 목차
- [프로젝트 개요](#프로젝트-개요)
- [프로젝트 목적](#프로젝트-목적)
- [개발 환경](#개발-환경)
- [사용 기술](#사용-기술)
- [데이터 소개](#데이터-소개)
- [데이터 분석 및 전처리](#데이터-분석-및-전처리)
- [모델링](#모델링)
- [결론](#결론)
- [프로젝트를 통해 느낀점](#프로젝트를-통해-느낀점)
<br>
<br>

## 프로젝트 개요
**미세 먼지 농도 예측**

공기, 날씨 데이터를 바탕으로 1일 후 미세먼지 농도 예측
<br>
<br>

**예측 값 csv파일 저장**

예측 값을 csv파일로 저장
<br>
<br>
<br>

## 프로젝트 목적
**왜?**

시계열 데이터 이용한 ML 모델링과 AutoML을 사용해보고자 시작하였습니다.

실생활에 조금이나마 도움이 될 수 있는 예측 모델로 미세먼지 예측을 하는 모델을 만들었습니다.
<br>
<br>
<br>

## 개발 환경
- Visual Studio Code
- Github
- Colab
- Ubuntu 22.04
<br>
<br>

## 사용 기술
- Python
- H2O AutoML
<br>
<br>

## 데이터 소개
**대기질 관련 수치데이터, 날씨 수치데이터**

- 학습데이터(21년 01월 01일 01시 ~ 21년 12월 31일 24시)

- 검증데이터(22년 01월 01일 01시 ~ 22년 03월 31일 24시)

- 테스트데이터(22년 09월 01일 01시 ~ 23년 02월 28일 24시)
<br>

대기질 데이터
![image](https://github.com/hwtheowl/Air_Quality_Prediction/assets/132368135/7963f869-e8ee-4fd6-b07d-86fcbb7b4b2b)

날씨 데이터
![image](https://github.com/hwtheowl/Air_Quality_Prediction/assets/132368135/466fcdd6-92bb-415d-8e97-a62ca67e52c5)
<br>
<br>
<br>

## 데이터 분석 및 전처리
![image](https://github.com/hwtheowl/Air_Quality_Prediction/assets/132368135/98217526-e884-4b22-9985-dfd26c428ea4)

**음의 상관관계**
- 중간 : (CO, O3), (O3, NO2)


**양의 상관관계**
- 매우 강함 : (CO, NO2)
- 강함 : (CO, PM25), (PM10, PM25)
- 중간 : (NO2, PM25)

### 결측치 처리
**데이터가 전혀 없거나 모든 데이터가 동일한(지점명, 지점 등) 컬럼 제거**

![image](https://github.com/hwtheowl/Air_Quality_Prediction/assets/132368135/3e62e0ee-ec2f-470c-b6de-9506f8f96a35)

**강수량, 적설량 등 데이터의 경우 큰 수치 사이에도 결측치 존재**
**단순히 제거하는 것보다 뒷 5개의 행에 대한 평균 및 마지막 5개 행의 경우 앞의 값을 넣는 방법 사용**

![image](https://github.com/hwtheowl/Air_Quality_Prediction/assets/132368135/c760eced-34fc-4f1a-bb0f-6014ba4f3e40)

**일조, 일사의 경우 해가 뜨지 않는 시간에는 결측치이기 때문에 0으로 대체**
**플래그의 경우 일사, 일조에 관련한 결측치와 1:1매칭으로 확인 되어 컬럼 제거**
<br>
<br>
<br>

## 모델링
**H2O AutoML 사용**

### PM10 예측 모델
![image](https://github.com/hwtheowl/Air_Quality_Prediction/assets/132368135/c6154f02-5004-4db6-9e85-373728c21fe4)

![image](https://github.com/hwtheowl/Air_Quality_Prediction/assets/132368135/f77892c6-a36c-4c80-bfc4-309950d62b89)

여러 모델을 앙상블 하여 만들어진 모델이 사용 되었고, MAE는 3.68 MSE는 63.08의 성능을 보임

### PM25 예측 모델
![image](https://github.com/hwtheowl/Air_Quality_Prediction/assets/132368135/aef0e6f2-f51b-4e34-a6d1-43d396e43837)

![image](https://github.com/hwtheowl/Air_Quality_Prediction/assets/132368135/465cc104-5062-4b82-b335-f7c1a29a9a4e)

PM10모델과 마찬가지로 여러 모델을 앙상블 하였고, MAE는 2.13 MSE는 9.89로 상대적으로 더 좋은 성능을 보임

### 최종 모델
![image](https://github.com/hwtheowl/Air_Quality_Prediction/assets/132368135/b50ec148-cd45-4656-a2e9-a8b5950891ef)

학습된 모델을 합쳐 동시에 예측하도록 구성
<br>
<br>
<br>

## 결론

**PM10 예측값 vs 실제값 비교그래프**
![predict_PM10](https://github.com/hwtheowl/Air_Quality_Prediction/assets/132368135/7052ac87-8ee3-4ecf-aebe-326894d4da44)

**PM25 예측값 vs 실제값 비교그래프**
![predict_PM25](https://github.com/hwtheowl/Air_Quality_Prediction/assets/132368135/439e1092-861d-4a97-9d40-3941b3db1806)

실제 데이터와 추세적으로 거의 유사한 예측 가능
수치적으로도 큰 차이가 보이지 않음
<br>
<br>
<br>

## 프로젝트를 통해 느낀점
실제 기상 관측을 통해 구해진 데이터를 바탕으로 학습하고 예측하여 괜찮은 성능의 모델을 만들수 있어 기분이 좋았습니다.

AutoML의 경우 굉장히 편리하고 어떠한 모델을 사용하였는지, 성능지표는 어떤지 간편하게 보여주는 점에서 좋은 점을 느꼈고 향후에도 계속 써나갈 생각입니다.

크게 어려움이 있던 프로젝트는 아니었고 간단했지만 AutoML을 사용하고 데이터를 구하고 가공하는 과정이 재밌었습니다.

매번 새로운 머신러닝 분야이지만 계속 배우고 사용해가며 조금씩 성장해나가도록 할 것입니다.
