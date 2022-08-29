from fastapi import FastAPI, Body, Response
from typing import Any
from user_builder import build_user
from MLFiles.Prediction import predict_user
import uvicorn


################### Initializations #######################

user_db = {"username": None,
           "password": None
           }

app = FastAPI()

################### REST Requests handling #######################

@app.get("/")
def home():
    print("not here")
    return {"Data": "Test"}


@app.post("/predict/")
def predict(body: Any = Body(...)):
    username = user_db["username"]
    password = user_db["password"]
    if not username or not password:
        content = "Please Login First!"
    else:
        # body is the username to send details
        print("Logging in...")
        user = build_user(body.decode("utf-8"), username, password)
        if user != None:
            print("User built successfuly.")
            print("Predicting...")
            content = predict_user(user)
            print(f"Prediction results: {content}")
        else:
            content = "An Error Has Occured! Please Try Again :)"
    headers = {'Content-Type': 'text/plain',
               'Access-Control-Allow-Origin': '*'}
    return Response(content=content, headers=headers)


@app.post("/login/")
def login(body: Any = Body(...)):
    # body is the username and password separated by whitespace
    password, username = body.decode("utf-8").split(" ", 1)
    user_db["username"] = username
    user_db["password"] = password
    content = "success"
    headers = {'Content-Type': 'text/plain',
               'Access-Control-Allow-Origin': '*'}
    return Response(content=content, headers=headers)


@app.post("/logout/")
def logout(body: Any = Body(...)):
    user_db["username"] = None
    user_db["password"] = None
    content = "success"
    headers = {'Content-Type': 'text/plain',
               'Access-Control-Allow-Origin': '*'}
    return Response(content=content, headers=headers)



@app.post("/isLogged/")
def isLogged():
    content = "no"
    if user_db["username"]:
        content = "yes"
    headers = {'Content-Type': 'text/plain',
               'Access-Control-Allow-Origin': '*'}
    return Response(content=content, headers=headers)

################### main #######################
def main():
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
