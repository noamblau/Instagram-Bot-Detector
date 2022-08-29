py -m venv venv_build
call venv_build\Scripts\activate.bat
py -m pip install numpy
py -m pip install pandas
py -m pip install scikit-learn
py -m pip install Pillow
py -m pip install fastapi
py -m pip install instaloader
py -m pip install uvicorn
py -m pip install pyinstaller