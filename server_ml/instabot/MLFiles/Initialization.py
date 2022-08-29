import re
import json
import numpy as np
from MLFiles.InstaUser import User
from MLFiles.UtilsFunctions import minimal_diff_between, select_random_rows_for_validation_and_test
import pandas as pd
from statistics import median, mean


FAKE_COLS = ['follower_following_ratio', 'user_biography_length',
             'user_follower_count', 'user_following_count', 'user_has_profile_pic',
             'user_is_private', 'user_media_count', 'username_digit_count',
             'username_length']

AUTO_COLS = ['follower_following_ratio', 'mediaUpload_times',
             'media_comment_numbers', 'media_has_location_info', 'media_hashtag_numbers',
             'media_like_numbers', 'user_biography_length', 'user_follower_count',
             'user_following_count', 'user_has_external_url',
             'user_has_highlight_reels', 'user_media_count', 'user_tags_count',
             'username_digit_count', 'username_length']

AUTO_MEDIA_COLS = ["media_comment_numbers", "media_hashtag_numbers",
                   "media_like_numbers", "media_has_location_info"]


# Create dataframe according to dataset_type (fake/auto)
def create_dataframe(account_data_list, dataset_type):
    dataframe = pd.DataFrame({})

    if dataset_type == "automated":
        for account_data in account_data_list:
            user_follower_count = account_data["userFollowerCount"]
            user_following_count = account_data["userFollowingCount"]
            follower_following_ratio = user_follower_count / max(1, user_following_count)

            temp_dataframe = pd.Series({"user_media_count": account_data["userMediaCount"],
                                        "user_follower_count": account_data["userFollowerCount"],
                                        "user_following_count": account_data["userFollowingCount"],
                                        "user_has_highlight_reels": account_data["userHasHighlighReels"],
                                        "user_has_external_url": account_data["userHasExternalUrl"],
                                        "user_tags_count": account_data["userTagsCount"],
                                        "follower_following_ratio": follower_following_ratio,
                                        "user_biography_length": account_data["userBiographyLength"],
                                        "username_length": account_data["usernameLength"],
                                        "username_digit_count": account_data["usernameDigitCount"],
                                        "media_comment_numbers": account_data["mediaCommentNumbers"],
                                        "media_has_location_info": account_data["mediaHasLocationInfo"],
                                        "media_hashtag_numbers": account_data["mediaHashtagNumbers"],
                                        "media_like_numbers": account_data["mediaLikeNumbers"],
                                        "mediaUpload_times": account_data["mediaUploadTimes"],
                                        "automated_behaviour": account_data["automatedBehaviour"]
                                        })
            dataframe = dataframe.append(temp_dataframe, ignore_index=True)

    elif dataset_type == "fake":
        for account_data in account_data_list:
            user_follower_count = account_data["userFollowerCount"]
            user_following_count = account_data["userFollowingCount"]
            follower_following_ratio = user_follower_count / \
                max(1, user_following_count)

            temp_dataframe = pd.Series({"user_media_count": account_data["userMediaCount"],
                                        "user_follower_count": account_data["userFollowerCount"],
                                        "user_following_count": account_data["userFollowingCount"],
                                        "user_has_profile_pic": account_data["userHasProfilPic"],
                                        "user_is_private": account_data["userIsPrivate"],
                                        "follower_following_ratio": follower_following_ratio,
                                        "user_biography_length": account_data["userBiographyLength"],
                                        "username_length": account_data["usernameLength"],
                                        "username_digit_count": account_data["usernameDigitCount"],
                                        "is_fake": account_data["isFake"]
                                        })
            dataframe = dataframe.append(temp_dataframe, ignore_index=True)
    return dataframe


def import_data(dataset_path, dataset_version, dataset_type, account_data_positive_file, account_data_negative_file, is_merged=False):
    with open(dataset_path + "/" + dataset_version + account_data_positive_file) as json_file:
        positive_account_data = json.load(json_file)
    with open(dataset_path + "/" + dataset_version + account_data_negative_file) as json_file:
        negative_account_data = json.load(json_file)
    positive_account_dataframe = create_dataframe(
        positive_account_data, dataset_type)
    negative_account_dataframe = create_dataframe(
        negative_account_data, dataset_type)
    if is_merged:
        merged_dataframe = positive_account_dataframe.append(
            negative_account_dataframe, ignore_index=True)
        data = dict({"dataset_type": dataset_type,
                     "dataframe": merged_dataframe})
    else:
        data = dict({"dataset_type": dataset_type,
                    "positive_account_dataframe": positive_account_dataframe,
                    "negative_account_dataframe": negative_account_dataframe})
    return data


# Used for trainig and evalutaion
# This function returns a list of four tuples:
# 1) (fake dataframe without the is_fake column, fake is_fake column)
# 2) (real dataframe without the is_fake column, real is_fake column)
# 3) (automated dataframe without the automated_behaviour column, automated automated_behaviour column)
# 4) (nonautomated dataframe without the automated_behaviour column, nonautomated automated_behaviour column)
def build_dataframes_from_dataset():
    dataset_path = "data"

    dataset_version = "fake-v1.0"
    fake_dataset_dict = import_data\
        (dataset_path, dataset_version, "fake", "/fakeAccountData.json", "/realAccountData.json")

    fake_account_df = fake_dataset_dict['positive_account_dataframe']
    real_account_df = fake_dataset_dict['negative_account_dataframe']
    fake_df_is_fake_col = fake_account_df.pop("is_fake")
    read_df_is_fake_col = real_account_df.pop("is_fake")

    dataset_version = "automated-v1.0"
    automated_dataset_dict =  import_data\
        (dataset_path, dataset_version, "automated", "/automatedAccountData.json", "/nonautomatedAccountData.json")

    automated_account_df = automated_dataset_dict['positive_account_dataframe']
    nonautomated_account_df = automated_dataset_dict['negative_account_dataframe']
    automated_account_auto_behavior_col = automated_account_df.pop(
        "automated_behaviour")
    nonauto_account_auto_behavior_col = nonautomated_account_df.pop(
        "automated_behaviour")
    custom_automated_df(automated_account_df)
    custom_automated_df(nonautomated_account_df)

    return [(fake_account_df, fake_df_is_fake_col),
            (real_account_df, read_df_is_fake_col),
            (automated_account_df, automated_account_auto_behavior_col),
            (nonautomated_account_df, nonauto_account_auto_behavior_col)]


def build_merged_dataframes_from_dataset():
    dataset_path = "data"
    dataset_version = "fake-v1.0"

    fake_dataset_dict = import_data(dataset_path, dataset_version, "fake", "/fakeAccountData.json", "/realAccountData.json", is_merged=True)
    fake_account_df = fake_dataset_dict['dataframe']
    fake_df_is_fake_col = fake_account_df.pop("is_fake")

    dataset_version = "automated-v1.0"

    automated_dataset_dict = import_data(dataset_path, dataset_version, "automated", "/automatedAccountData.json", "/nonautomatedAccountData.json", is_merged=True)
    automated_account_df = automated_dataset_dict['dataframe']
    automated_account_auto_behavior_col = automated_account_df.pop(
        "automated_behaviour")
    custom_automated_df(automated_account_df)

    return [(fake_account_df, fake_df_is_fake_col),
            (automated_account_df, automated_account_auto_behavior_col)]


# modify automated dataframes by taking media related columns and replace with average and median based columns
# and also for mediaUpload_times column, take the minimal difference between two values in list
def custom_automated_df(automated_dataset_df):
    for col in AUTO_MEDIA_COLS:
        for i in automated_dataset_df.index:
            avg_col = col + "_avg"
            median_col = col + "_median"
            curr_list = automated_dataset_df.at[i, col]
            if len(curr_list) >= 5:
                curr_list = curr_list[:5]
            new_avg_val = 0
            new_median_val = 0
            if len(curr_list) != 0:
                new_avg_val = mean(curr_list)
                new_median_val = median(curr_list)
            automated_dataset_df.at[i, avg_col] = new_avg_val
            automated_dataset_df.at[i, median_col] = new_median_val
        automated_dataset_df.drop(col, inplace=True, axis=1)

    for i in automated_dataset_df.index:
        media_upload_times_list = automated_dataset_df.at[i,
                                                          "mediaUpload_times"]
        if len(media_upload_times_list) == 0:
            automated_dataset_df.at[i, "mediaUpload_times"] = 0
        elif len(media_upload_times_list) >= 5:
            media_upload_times_list = media_upload_times_list[:5]
        automated_dataset_df.at[i, "mediaUpload_times"] = minimal_diff_between(
            media_upload_times_list)
    automated_dataset_df.rename(
        columns={'mediaUpload_times': 'mediaUpload_time_diff'}, inplace=True)



# if data_type == 'fake' -> merge fake dataframe with real dataframe and fake is_fake column with real is_fake column
# if data_type == 'auto' -> merge auto dataframe with nonauto dataframe and auto automated_behaviour column with nonauto
# automated_behaviour column.
# Also merge the random rows for test and validation
def get_merged_df_and_test_data(df1, col1, df2, col2, data_type, random_seed):
    if data_type == 'fake':
        # df1 = fake, col1 = fake_is_fake_col, df2 = real, col2 = real_is_fake_col
        x1_val, y1_val, x1_test, y1_test = select_random_rows_for_validation_and_test(
            df1, col1, 'fake', random_seed)
        x2_val, y2_val, x2_test, y2_test = select_random_rows_for_validation_and_test(
            df2, col2, 'real', random_seed)

    else:  # data_type == 'auto':
        # df1 = auto, col1 = auto_automated_behavior_col, df2 = nonauto, col2 = nonauto_automated_behavior_col
        x1_val, y1_val, x1_test, y1_test = select_random_rows_for_validation_and_test(
            df1, col1, 'auto', random_seed)
        x2_val, y2_val, x2_test, y2_test = select_random_rows_for_validation_and_test(
            df2, col2, 'nonauto', random_seed)

    merged_df = df1.append(df2, ignore_index=True)
    merged_col = col1.append(col2, ignore_index=True)
    merged_x_val = x1_val + x2_val
    merged_y_val = y1_val + y2_val
    merged_x_test = x1_test + x2_test
    merged_y_test = y1_test + y2_test

    return merged_df, merged_col, merged_x_val, merged_y_val, merged_x_test, merged_y_test


def build_train_val_test(x_df, y_df, x_val, y_val, x_test, y_test):
    x_train_np = x_df.to_numpy()
    y_train_np = y_df.to_numpy()
    x_train, y_train = x_train_np, y_train_np

    x_val_np = np.asarray(x_val)
    y_val_np = np.asarray(y_val)
    x_val, y_val = x_val_np, y_val_np

    x_test_np = np.asarray(x_test)
    y_test_np = np.asarray(y_test)
    x_test, y_test = x_test_np, y_test_np

    return x_train, y_train, x_val, y_val, x_test, y_test


def get_train_data(tup):
    x_df = tup[0]
    y_df = tup[1]
    x_train_np = x_df.to_numpy()
    y_train_np = y_df.to_numpy()
    x_train, y_train = x_train_np, y_train_np

    return x_train, y_train


def build_fake_user_df_from_data(user: User):
    follower_following_ratio = user.user_follower_count / \
        max(1, user.user_following_count)
    df = pd.DataFrame([follower_following_ratio, user.user_biography_length, user.user_follower_count,
                       user.user_following_count, user.user_has_profile_pic, user.user_is_private,
                       user.user_media_count, user.username_digit_count, user.username_length]
                      ).transpose()

    df.columns = FAKE_COLS

    return df


def build_auto_user_df_from_data(user: User):
    follower_following_ratio = user.user_follower_count / \
        max(1, user.user_following_count)
    df = pd.DataFrame([follower_following_ratio, user.mediaUpload_times, user.media_comment_numbers,
                       user.media_has_location_info, user.media_hashtag_numbers,
                       user.media_like_numbers, user.user_biography_length, user.user_follower_count,
                       user.user_following_count, user.user_has_external_url, user.user_has_highlight_reels,
                       user.user_media_count, user.user_tags_count, user.username_digit_count,
                       user.username_length]).transpose()
    df.columns = AUTO_COLS
    custom_automated_df(df)

    return df
