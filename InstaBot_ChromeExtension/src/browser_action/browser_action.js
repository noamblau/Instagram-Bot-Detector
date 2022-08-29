let playSiren;

const initLoginTab = () => {
    fetch('http://127.0.0.1:8000/isLogged/', {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'text/plain',
        },
        body: "",
    })
        .then(async (response) => {
            const resText = await response.text();
            if (resText == "yes")
                handleLogin();
        })
        .catch((error) => {
            console.error('Error:', error);
        });

}

initLoginTab();

// calculate the prediction when click on detection
document.getElementById("check-account").onclick = event => {
    chrome.tabs.query({ currentWindow: true, active: true }, async function () {
        let profileName = document.getElementById("input").value;
        document.getElementById("loading").style.visibility = "visible";
        clearInterval(playSiren);
        document.getElementsByTagName("img")[0].src = "../../logos/logo.png";
        await sendPredictionRequestToServer(profileName);
    });
}

// save username and password
document.getElementById("login_button").onclick = event => {
    chrome.tabs.query({ currentWindow: true, active: true }, async function () {
        let username = document.getElementById("username").value;
        let password = document.getElementById("password").value;
        if (password.length == 0 || username.length == 0)
            alert("username and password must have at least one character");
        else
            await sendUsernameAndPasswordToServer(username, password);
    });
}

// delete username and password
document.getElementById("logout_button").onclick = event => {
    chrome.tabs.query({ currentWindow: true, active: true }, async function () {
        await sendLogoutRequestToServer();
    });
}

// when login tab selected show the login page
document.getElementById("tablogin").onclick = event => {
    chrome.tabs.query({ currentWindow: true, active: true }, function () {
        document.getElementById("login").style.display = "block";
        document.getElementById("search").style.display = "none";
        document.getElementById("tabsearch").classList.remove("active");
        document.getElementById("tablogin").classList.add("active");
    });
}

// when search tab selected show the search page
document.getElementById("tabsearch").onclick = event => {
    chrome.tabs.query({ currentWindow: true, active: true }, function () {
        document.getElementById("login").style.display = "none";
        document.getElementById("search").style.display = "block";
        document.getElementById("tabsearch").classList.add("active");
        document.getElementById("tablogin").classList.remove("active");
    });
}

// send to server login data
async function sendUsernameAndPasswordToServer(username, password) {
    fetch('http://127.0.0.1:8000/login/', {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'text/plain',
        },
        body: password + " " + username,
    })
        .then(async (response) => {
            const resText = await response.text();
            if (resText == "success")
                handleLogin();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

// delete from server login data
async function sendLogoutRequestToServer() {
    fetch('http://127.0.0.1:8000/logout/', {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'text/plain',
        },
        body: "logout",
    })
        .then(async (response) => {
            const resText = await response.text();
            if (resText == "success")
                handleLogout();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

// use server to calculate user's prediction
async function sendPredictionRequestToServer(username) {
    fetch('http://127.0.0.1:8000/predict/', {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'text/plain',
        },
        body: username,
    })
        .then(async (response) => {
            const resText = await response.text();
            document.getElementById("loading").style.visibility = "hidden";
            handleResponse(resText);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

// add the prediction's result for the extension
function handleResponse(resText) {
    let textNode;
    let element = document.getElementById("result");
    let tag = document.createElement("p");
    document.getElementById("loading").style.visibility = "hidden";
    textNode = document.createTextNode(resText);
    tag.appendChild(textNode);
    let child = element.lastElementChild;
    if (child)
        element.removeChild(child);
    element.appendChild(tag);
    checkToPlaySiren(resText);
}

// check if siren should be turned on
function checkToPlaySiren(resText) {
    const splitted = resText.replaceAll("%", "").split(" ");
    const img = document.getElementsByTagName("img")[0];

    // more than 80% username may be bot then play siren, otherwise siren is off
    if (splitted[0] >= 80 || splitted[3] >= 80) {
        playSiren = siren(img);
    }
}

// add siren notification
function siren(img) {
    let sirenOn = true;

    const changePicture = () => {
        if (sirenOn)
            img.src = "../../logos/logo-red.png";
        else
            img.src = "../../logos/logo-red-light.png";

        sirenOn = !sirenOn;
    }
    return setInterval(changePicture, 300);
}

function handleLogin() {
    document.getElementById("logout_button").style.display = "block";
    document.getElementById("login_form").style.display = "none";
    document.getElementById("username").value = "";
    document.getElementById("password").value = "";
}

function handleLogout() {
    document.getElementById("logout_button").style.display = "none";
    document.getElementById("login_form").style.display = "block";
}