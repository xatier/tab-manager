/* eslint-disable no-unused-vars */

const SERVER_URL = "http://localhost:9487"

function getAllTabs() {
    return new Promise(function (resolve, reject) {
        chrome.windows.getAll({ populate: true }, function (windows) {
            let tabs = [];
            for (let win in windows) {
                let w = windows[win];
                if (w.type === "normal") {
                    let current = { win: w.id, tabs: [] };
                    for (let t in w.tabs) {
                        current.tabs.push(w.tabs[t]);
                    }
                    tabs.push(current);
                }
            }
            resolve(tabs);
        });
    });
}

async function saveAllTabs(tab) {
    let tabs = await getAllTabs();

    let response = await fetch(SERVER_URL + "/save", {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ data: JSON.stringify(tabs) }),
    });

    console.log("save");
    console.log(response);
}

async function loadAllTabs(info, tab) {
    let response = await fetch(SERVER_URL + "/load");
    let windows = await response.json();

    console.log("load");
    console.log(windows);

    for (let win in windows) {
        let urls = windows[win].tabs.map((e) => e.url);
        chrome.windows.create({ url: urls });
    }
}

// main function
function _() {
    chrome.browserAction.onClicked.addListener(saveAllTabs);

    chrome.runtime.onInstalled.addListener(function () {
        chrome.contextMenus.create({
            id: "load-all-tabs",
            title: "Load all tabs",
            contexts: ["browser_action", "page"],
        });

        chrome.contextMenus.create({
            id: "save-all-tabs",
            title: "Save all tabs",
            contexts: ["browser_action", "page"],
        });
    });

    chrome.contextMenus.onClicked.addListener(function (info, tab) {
        if (info.menuItemId === "load-all-tabs") {
            loadAllTabs();
        } else if (info.menuItemId === "save-all-tabs") {
            saveAllTabs();
        }
    });
}
_();
