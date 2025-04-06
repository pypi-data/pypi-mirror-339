import pandas as pd
from house_prices_nguyen_nguyen.inference import load_model
from house_prices_nguyen_nguyen.preprocess import process_data
from house_prices_nguyen_nguyen.train import split_train_test_data


def test_refactor():
    model_path = ("/Users/nguyennguyen/"
                  "Desktop/github_repos/personal/"
                  "dsp-nguyen-nguyen/data")
    cols_for_encode = ["HouseStyle", "BldgType"]
    cols_for_scale = ["LotArea", "YearBuilt", "BedroomAbvGr"]
    cols_no_transform = ["OverallCond"]
    (loaded_model, loaded_one_hot_encoder, load_scaler) =\
        load_model(model_path)
    train_df = pd.read_csv(f"{model_path}/train.csv")
    (X_train, y_train, X_test, y_test) = split_train_test_data(
        train_df,
        cols_for_encode + cols_for_scale + cols_no_transform,
        "SalePrice"
    )
    X_split_test_processed = process_data(
        X_test, loaded_one_hot_encoder, load_scaler,
        cols_for_encode, cols_for_scale, cols_no_transform)
    expected_split_test_processed = (
        pd.read_parquet(f"{model_path}/x_split_test_processed.csv"))
    pd.testing.assert_frame_equal(
        expected_split_test_processed,
        X_split_test_processed
    )
