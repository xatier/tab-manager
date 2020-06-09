/* eslint-disable no-console */
/* global fetch:false */

(function _() {
    const SERVER_URL = 'http://localhost:9487';

    // an hour
    const TIMEOUT = 60 * 60 * 1000;

    function getAllTabs() {
        return new Promise((resolve) => {
            chrome.windows.getAll({ populate: true }, (windows) => {
                const tabs = [];
                windows
                    .filter(({ type }) => type === 'normal')
                    .forEach((win) => {
                        const current = { win: win.id, tabs: [] };
                        win.tabs.forEach((tab) => {
                            current.tabs.push(tab);
                        });
                        tabs.push(current);
                    });
                resolve(tabs);
            });
        });
    }

    async function saveAllTabs() {
        const tabs = await getAllTabs();

        const response = await fetch(`${SERVER_URL}/save`, {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data: JSON.stringify(tabs) }),
        });

        console.log('save');
        console.log(response);
    }

    async function loadAllTabs() {
        const response = await fetch(`${SERVER_URL}/load`);
        const windows = await response.json();

        console.log('load');
        console.log(windows);

        windows.forEach(({ tabs }) => {
            chrome.windows.create({ url: tabs.map(({ url }) => url) });
        });
    }

    function setupChromeExtension() {
        chrome.browserAction.onClicked.addListener(saveAllTabs);

        chrome.runtime.onInstalled.addListener(() => {
            chrome.contextMenus.create({
                id: 'load-all-tabs',
                title: 'Load all tabs',
                contexts: ['browser_action', 'page'],
            });

            chrome.contextMenus.create({
                id: 'save-all-tabs',
                title: 'Save all tabs',
                contexts: ['browser_action', 'page'],
            });
        });

        chrome.contextMenus.onClicked.addListener(({ menuItemId }) => {
            if (menuItemId === 'load-all-tabs') {
                loadAllTabs();
            } else if (menuItemId === 'save-all-tabs') {
                saveAllTabs();
            }
        });
    }

    function setupTimeout() {
        // auto save all tabs every TIMEOUT ms
        setInterval(saveAllTabs, TIMEOUT);
    }

    // init
    setupChromeExtension();
    setupTimeout();
})();
