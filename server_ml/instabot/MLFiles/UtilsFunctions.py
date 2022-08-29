import random


#Used for training only
# remove row with given index from dataframe and return it
def drop_return(df, index):
    row = df.loc[index]
    df.drop(index, inplace=True)
    return row


# find minimal difference between two following items in list
def minimal_diff_between(lst):
    if len(lst) <= 1:
        return 0
    min_val = lst[0] - lst[1]
    for i in range(1, len(lst) - 1):
        diff = lst[i] - lst[i + 1]
        if min_val > diff:
            min_val = diff
    return min_val


#Used for training only
# choose random rows to remove from df with their corresponding rows on column and return validation and test lists
def select_random_rows_for_validation_and_test(df, column, df_type, random_seed):
    random.seed(random_seed)
    random_x_validation = []
    random_y_validation = []
    random_x_test = []
    random_y_test = []

    # we split the data to about 70% train, 20% test and 10% validation
    if df_type == 'fake':
        random_validation_counter = 20
        random_test_counter = 40
    elif df_type == 'real':
        random_validation_counter = 100
        random_test_counter = 200
    elif df_type == 'auto' or df_type == 'nonauto':
        random_validation_counter = 70
        random_test_counter = 140

    random_validation_index_list = random.sample(
        list(df.index), random_validation_counter)
    for i in random_validation_index_list:
        random_x_validation.append(drop_return(df, i))
        random_y_validation.append(drop_return(column, i))

    random_test_index_list = random.sample(list(df.index), random_test_counter)
    for i in random_test_index_list:
        random_x_test.append(drop_return(df, i))
        random_y_test.append(drop_return(column, i))

    return random_x_validation, random_y_validation, random_x_test, random_y_test
