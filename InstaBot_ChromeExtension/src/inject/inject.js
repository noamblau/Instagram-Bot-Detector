chrome.runtime.sendMessage({}, function (response) {
	const readyStateCheckInterval = setInterval(function () {
		if (document.readyState === "complete") {
			clearInterval(readyStateCheckInterval);

			// ----------------------------------------------------------
			// This part of the script triggers when page is done loading

			// variables
			const INSTAGRAM_URL = 'www.instagram.com';

			// initialize automation
			const initAutomation = () => {

				// create users list
				const users = getUsers();
				let prevUsersLength = Object.keys(users).length;

				let filteredLinks, usernames;
				let prevLastUsername, prevFirstUsername, currLastUsername, currFirstUsername;

				filteredLinks = filterLinksContainsUsernames();
				usernames = getUsernamesFromLinks(filteredLinks);

				prevFirstUsername = usernames[0];
				prevLastUsername = usernames[usernames.length - 1];

				// inject functions
				injectLoading(filteredLinks);
				injectUserBotness(users, filteredLinks);

				setInterval(() => {
					filteredLinks = filterLinksContainsUsernames();
					usernames = getUsernamesFromLinks(filteredLinks);

					currFirstUsername = usernames[0];
					currLastUsername = usernames[usernames.length - 1];

					if (currFirstUsername != prevFirstUsername ||
						currLastUsername != prevLastUsername) {
						injectLoading(filteredLinks);
						injectUserBotness(users, filteredLinks);
					}

					prevFirstUsername = currFirstUsername;
					prevLastUsername = currLastUsername;

					if (Object.keys(users).length != prevUsersLength)
						saveUsers(users);

					prevUsersLength = Object.keys(users).length;
				}, 1000);
			};

			// restore users list from local storage
			const getUsers = () => {
				if (localStorage.getItem('sadna-users') == undefined) {
					localStorage.setItem('sadna-users', JSON.stringify({}))
				}
				return JSON.parse(localStorage.getItem('sadna-users'));
			};

			const getLinks = () => Array.from(document.getElementsByTagName('a'));

			// return list of all links in the page that contains usernames
			const filterLinksContainsUsernames = () => {
				let links = getLinks();
				return links.filter((link) => {
					const splitted = link.href.split('/');

					//check that the link is user in Instagram
					if (splitted.length != 5) return;
					if (splitted[2] != INSTAGRAM_URL) return;

					//check that the link's name is the actual title
					return splitted[splitted.length - 2] === link.innerHTML;
				});
			};

			// return list of usernames in the page
			const getUsernamesFromLinks = (links) => {
				const usernames = [];
				links.forEach(element => {
					const splitted = element.href.split('/');
					usernames.push(splitted[splitted.length - 2]);
				});
				return usernames;
			};

			const isLoadingExists = (element) => {
				if (element.parentElement.lastChild != undefined)
					return (element.parentElement.lastChild.classList[0] === 'loading');
				return false;
			};

			const isPredictionExists = (element) => {
				return (element.parentElement.lastChild.classList[0] === 'prediction');
			};

			// create for every username loading sign before prediction's calculation
			const injectLoading = (links) => {
				for (const link of links) {
					if (!isLoadingExists(link) && !isPredictionExists(link)) {
						const tempDiv = document.createElement('div');
						tempDiv.classList.add("loading");
						tempDiv.innerHTML = "loading...";
						link.parentElement.insertBefore(tempDiv, link.nextSibling);
					}
				}
			}

			// insert for every username his prediction result
			const injectUserBotness = async (users, links) => {
				for (const link of links) {
					if (isLoadingExists(link) && !isPredictionExists(link)) {
						const tempDiv = link.parentElement.lastChild;
						const userName = link.innerHTML;
						await getUserPrediction(users, userName, tempDiv);
					}
				}
			};

			// if user's prediction is saved use this value, otherwise calculate prediction 
			const getUserPrediction = async (users, userName, tempDiv) => {
				const prediction = users[userName];
				// user not in cache
				if (prediction === undefined) {
					await sendUsernameToServer(users, userName, tempDiv);
				}
				else {
					addPredict(prediction, tempDiv);
				}
			};

			// insert prediction for username
			const addPredict = (prediction, tempDiv) => {
				tempDiv.classList.add("prediction");
				tempDiv.classList.remove("loading");

				// insert prediction
				tempDiv.innerHTML = prediction + "%";

				let img = new Image();
				img.src = "https://i.postimg.cc/mrDZn90b/person.png";
				img.className = "indication";

				// more than 80% username may be bot
				if (prediction >= 80) {
					tempDiv.classList.add("bot");
					img.src = "https://i.postimg.cc/cLT4Thk9/bot.png";
				}
				tempDiv.appendChild(img);
			};

			// use server to calculate user's prediction
			async function sendUsernameToServer(users, username, tempDiv) {
				fetch('http://127.0.0.1:8000/predict/', {
					method: 'POST', // or 'PUT'
					headers: {
						'Content-Type': 'text/plain',
					},
					body: username,
				})
					.then(async (response) => {
						const resText = await response.text();

						// prediction was calculated properly 
						if (resText != undefined && !resText.startsWith("An") && !resText.startsWith("Please")) {
							const splitted = resText.replaceAll("%", "").split(" ");
							const fakePrediction = Number(splitted[0]);
							const autoPrediction = Number(splitted[3]);
							const prediction = Math.max(fakePrediction, autoPrediction);
							addPredict(prediction, tempDiv);
							users[username] = prediction;
						}
					})
					.catch((error) => {
						console.error('Error:', error);
					});
			};

			// save current users list to local storage
			const saveUsers = (users) => {
				localStorage.setItem('sadna-users', JSON.stringify(users));
			};

			initAutomation();

		}
	}, 10);
});