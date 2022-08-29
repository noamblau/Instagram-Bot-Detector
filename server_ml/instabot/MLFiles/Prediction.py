from MLFiles.RandomForest import load_fake_rf_model, load_auto_rf_model
from MLFiles.Initialization import *


def predict_user(user: User):

    # fake
    print("Predicting if fake...")
    fake_rf_model = load_fake_rf_model()
    fake_user = build_fake_user_df_from_data(user)
    fake_user_np = fake_user.to_numpy()
    fake_prediction = fake_rf_model.predict_proba(fake_user_np)
    fake_prediction_prob = int(fake_prediction[0][1] * 100)

    # auto
    print("Predicting if automated...")
    auto_rf_model = load_auto_rf_model()
    auto_user = build_auto_user_df_from_data(user)
    auto_user_np = auto_user.to_numpy()
    auto_prediction = auto_rf_model.predict_proba(auto_user_np)
    auto_prediction_prob = int(auto_prediction[0][1] * 100)

    return f"{fake_prediction_prob}% fake and {auto_prediction_prob}% automated"
