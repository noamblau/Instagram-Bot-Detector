
# Instagram Bot Detector

 A real-time Instagram annotator which computes, for each user in your Instagram home feed, the likelihood they are a bot.
 In addition, the user can ask for a specific profile prediction.

 Each prediction has an appropriate indicators to warn users if needed. 



[![logo.png](https://i.postimg.cc/C1BfkXq3/logo.png)](https://postimg.cc/R6mFzPGd)



## Screenshots

![1](https://i.postimg.cc/2js6sMyh/1.png)![2](https://i.postimg.cc/CxYK18jK/2.png)


## Installation

Installation would require two parts:

1. Installing the Chrome extension:  
    - In Google Chrome, go to **chrome://extensions/**
    - Activate **Developer Mode**
    - Press on **Load Unpacked**
    - Load the folder: **Insta-Bot-Detector\InstaBot_ChromeExtension**
    - Click on the **Extension** in the toolbar above (The icon would be a puzzle piece)
    - Click on the **pin** icon near **Instagram Bot Detector**
For your reference, a detailed step-by-step video guide is available here:
	![](https://youtu.be/WgiucD1dbME) https://youtu.be/WgiucD1dbME

2. Installing the Server:
Path: **Insta-Bot-Detector\server_ml\instabot\dist\set_autoran.bat** \
Double click this file. That’s all – you’re done! :)
The batch file would automatically set the python server to start each time with your Windows startup.

**Additional Information:**
* The server runs in windowless mode, in the background.
* If you’d like to stop the server, run Insta-Bot-Detector\server_ml\instabot\dist\stop.bat
* If you’d like to run the server with window (including logs), run Insta-Bot-Detector\server_ml\instabot\dist\instabotserver.exe
* If you’d like to remove the server from running automatically on WIndows startup:\
        1. Press WINKEY+R\
        2. Type: *shell:startup*\
        3. Delete instabot shortcut

## Dependencies

* Windows 10+
* Google Chrome Browser
## Demos

**Window:**
https://youtu.be/auaNqlR5sJA

**Instagram home feed automation:**
https://youtube.com/shorts/q6AMynH-1k4 \
**Comment:** The prediction's results presnted on this demo only are completely arbitrary and any connection between them and the reality is purely coincidental!
