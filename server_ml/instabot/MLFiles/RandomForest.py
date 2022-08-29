from sklearn.ensemble import RandomForestClassifier
import pickle
import os
import sys
import pathlib

#fake
FAKE_TRAINING_FILENAME = 'MLFiles/TrainingFiles/fake_rf_model.sav'
FAKE_FILENAME = resource_path('fake_rf_model.sav')

# auto
AUTO_TRAINING_FILENAME = 'MLFiles/TrainingFiles/auto_rf_model.sav'
AUTO_FILENAME = resource_path('auto_rf_model.sav')


#Used for pyinstaller, for the creation of the exe
#Allows for getting the .sav files bundled into the exe
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = pathlib.Path(__file__).parent.resolve()


    return os.path.join(base_path, relative_path)


########################## Training ##########################
def save_rf_model_training(x_train, y_train, x_val, y_val, random_state, n_estimators, training_filename):
    rf_model = RandomForestClassifier(
        n_estimators=n_estimators, max_depth=15, random_state=random_state)
    rf_model.fit(x_train, y_train)
    rf_model.fit(x_val,y_val)
    pickle.dump(rf_model, open(training_filename, 'wb'))


def load_rf_model_training(training_filename):
    rf_loaded_model = pickle.load(open(training_filename, 'rb'))
    return rf_loaded_model



def save_rf_model(x_train, y_train, random_state, n_estimators, filename):
    rf_model = RandomForestClassifier(
        n_estimators=n_estimators, max_depth=15, random_state=random_state)
    rf_model.fit(x_train, y_train)
    pickle.dump(rf_model, open(filename, 'wb'))


########################## Predictions ##########################

def load_rf_model(filename):
    rf_loaded_model = pickle.load(open(filename, 'rb'))
    return rf_loaded_model



########################## Usage for fake and auto ##########################
N_ESTIMATORS_FAKE = 50
N_ESTIMATORS_AUTO = 100

def save_fake_rf_model_training(fake_x_train, fake_y_train, fake_x_val, fake_y_val, random_state):
    save_rf_model_training(fake_x_train, fake_y_train, fake_x_val, fake_y_val, N_ESTIMATORS_FAKE, random_state, FAKE_TRAINING_FILENAME)

def save_auto_rf_model_training(auto_x_train, auto_y_train, auto_x_val, auto_y_val, random_state):
    save_rf_model_training(auto_x_train, auto_y_train, auto_x_val, auto_y_val, N_ESTIMATORS_AUTO, random_state, AUTO_TRAINING_FILENAME)


def load_auto_rf_model_training():
    return load_rf_model_training(AUTO_TRAINING_FILENAME)

def load_fake_rf_model_training():
    return load_rf_model_training(FAKE_TRAINING_FILENAME)


def save_fake_rf_model(fake_x_train, fake_y_train, random_state):
    save_rf_model(fake_x_train, fake_y_train, random_state, N_ESTIMATORS_FAKE, FAKE_FILENAME)

def save_auto_rf_model(auto_x_train, auto_y_train, random_state):
    save_rf_model(auto_x_train, auto_y_train, random_state, N_ESTIMATORS_AUTO, AUTO_FILENAME)


def load_fake_rf_model():
    return load_rf_model(FAKE_FILENAME)

def load_auto_rf_model():
    return load_rf_model(AUTO_FILENAME)



######################## Evaluation ########################

# hyper parameters tuning using validation set
def eval_classifier_model_params(x_train, y_train, x_val, y_val):
    n_estimators = [1, 2, 3, 4, 5, 50, 100, 200]
    max_depth = [5, 10, 15, 20]
    scores = dict()

    for n in n_estimators:
        for d in max_depth:
            rfc = RandomForestClassifier(random_state=4)
            rfc.set_params(**{'n_estimators': n, 'max_depth': d})
            rfc.fit(x_train, y_train)
            c_score = rfc.score(x_val, y_val)
            print(f"n = {n}, d = {d}, c_score = {c_score}")
            scores[(n, d)] = c_score

    return max(scores.items(), key=lambda k: k[1])
