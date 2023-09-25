import h2o
import pandas as pd


def predict(model_PM10=None, model_PM25=None, dataset=None):
    if model_PM10 is None or model_PM25 is None:
        model_PM10, model_PM25 = load_model()
    
    if dataset is None:
        dataset = load_dataset()

    # 데이터셋 형식 변경
    h2o_dataset = h2o.H2OFrame(dataset)

    # 예측
    predictions_PM10 = model_PM10.predict(h2o_dataset)
    predictions_PM25 = model_PM25.predict(h2o_dataset)

    # 평가지표 계산
    performance_PM10 = model_PM10.model_performance(h2o_dataset)
    performance_PM25 = model_PM25.model_performance(h2o_dataset)

    print("PM10 Model Performance")
    print("MSE: ", performance_PM10.mse())
    print("MAE: ", performance_PM10.mae())

    print("PM2.5 Model Performance")
    print("MSE: ", performance_PM25.mse())
    print("MAE: ", performance_PM25.mae())

    # 예측값 저장
    dataset['PM10_prediction'] = predictions_PM10.as_data_frame().values.flatten()
    dataset['PM25_prediction'] = predictions_PM25.as_data_frame().values.flatten()
    dataset.to_csv('predictions.csv', index=False)

    print("자세한 수치는 csv파일을 확인하세요.")



def load_model(PM10="PM10_model.zip", PM25="PM25_model.zip"):
    h2o.init()
    saved_model_PM10 = h2o.load_model(PM10)
    saved_model_PM25 = h2o.load_model(PM25)

    return saved_model_PM10, saved_model_PM25



def load_dataset(air_data="air_test.csv", weather_data="weather_test.csv"):
    # 공기데이터 불러오기 및 필요없는 컬럼 제거
    law_air_dataset = pd.read_csv(air_data, sep=",", index_col=0, encoding="utf-8")
    air_dataset = law_air_dataset.drop(columns=["지역", 
                                                "망", 
                                                "측정소코드",
                                                "측정소명", 
                                                "주소"])
    
    
    # 날씨데이터 불러오기 및 필요없는 컬럼 제거
    law_weather_dataset = pd.read_csv(weather_data, sep=",", encoding="utf-8")
    weather_dataset = law_weather_dataset.drop(columns=["지점",
                                                        "지점명",
                                                        "기온 QC플래그",
                                                        "강수량 QC플래그", 
                                                        "풍속 QC플래그", 
                                                        "풍향 QC플래그", 
                                                        "습도 QC플래그", 
                                                        "현지기압 QC플래그", 
                                                        "해면기압 QC플래그", 
                                                        "지면상태(지면상태코드)", 
                                                        "지면온도 QC플래그",
                                                        "일조 QC플래그", 
                                                        "일사 QC플래그", 
                                                        "운형(운형약어)", 
                                                        "최저운고(100m )", 
                                                        "현상번호(국내식)"])
    
    
    # 날씨데이터 강수량, 적설, 3시간신적설, 일조, 일사 결측치 처리
    weather_dataset["강수량(mm)"] = weather_dataset["강수량(mm)"].fillna(weather_dataset["강수량(mm)"].rolling(5, min_periods=1).mean().shift(-5))
    weather_dataset["강수량(mm)"].fillna(method="ffill", inplace=True)

    weather_dataset["적설(cm)"] = weather_dataset["적설(cm)"].fillna(weather_dataset["적설(cm)"].rolling(5, min_periods=1).mean().shift(-5))
    weather_dataset["적설(cm)"].fillna(method="ffill", inplace=True)

    weather_dataset["3시간신적설(cm)"] = weather_dataset["3시간신적설(cm)"].fillna(weather_dataset["3시간신적설(cm)"].rolling(5, min_periods=1).mean().shift(-5))
    weather_dataset["3시간신적설(cm)"].fillna(method="ffill", inplace=True)

    weather_dataset["일조(hr)"] = weather_dataset["일조(hr)"].fillna(0)
    weather_dataset["일사(MJ/m2)"] = weather_dataset["일사(MJ/m2)"].fillna(0)


    # 날씨데이터 최종 결측치 제거
    weather_dataset = weather_dataset.dropna(axis=0)


    # 공기데이터, 날씨데이터 측정일시 통일
    air_dataset["측정일시"] = air_dataset["측정일시"].astype(str)
    air_dataset.loc[air_dataset["측정일시"].str[-2:] == "24", "측정일시"] = (pd.to_datetime(air_dataset["측정일시"].str[:-2], format="%Y%m%d") + pd.DateOffset(days=1)).dt.strftime("%Y%m%d") + "00"
    air_dataset["time"] = pd.to_datetime(air_dataset["측정일시"], format="%Y%m%d%H")

    weather_dataset["time"] = pd.to_datetime(weather_dataset["일시"], format="%Y-%m-%d %H:%M")


    # 데이터 합치기
    pre_df = pd.merge(air_dataset, weather_dataset, on="time")
    pre_df.set_index("time", inplace=True)
    pre_df.drop(columns=["측정일시", "일시"], inplace=True)


    # y값 생성 및 시간정보 생성
    pre_df["PM10_t+1"] = pre_df["PM10"].shift(-1)
    pre_df["PM25_t+1"] = pre_df["PM25"].shift(-1)
    pre_df.dropna(inplace=True)
    pre_df['year'] = pre_df.index.year
    pre_df['month'] = pre_df.index.month
    pre_df['day'] = pre_df.index.day
    pre_df['hour'] = pre_df.index.hour


    return pre_df



# 예측 시작(사전에 로드한 모델 혹은 데이터 셋이 있을 경우)
# predict(PM10_model, PM25_model, data)


# 예측 시작(사전에 로드한 모델 혹은 데이터 셋이 없을 경우)
predict()