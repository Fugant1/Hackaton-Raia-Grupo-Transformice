
const API_URL = `http://localhost:8000`;

const scan = async post_text => {
    const params = new URLSearchParams({ post_text });

    return fetch(`${API_URL}/scan?${params.toString()}`)
        .then(response => response.json())
        .catch(err => err.message);
}

const observer = new MutationObserver(() => {
    if (window.location.pathname.includes('/status/')) {
        waitForElement('[data-testid="tweetText"]')
            .then(element => scan(element.innerText))
            .then(showAvaliacaoPopup);
    } else {
        hideAvaliacaoPopup();
    }
});

observer.observe(document.body, {
    subtree: true,
    childList: true,
    attributes: true,
});

function showAvaliacaoPopup(avaliacao) {
    console.log({ avaliacao });

    const popup = document.createElement('div');
    const text = document.createTextNode('Avaliacao aqui');

    popup.appendChild(text);
    popup.style.position = "fixed";
    popup.style.top = "5%";
    popup.style.right = "5%";
    popup.style.width = "400px";
    popup.style.padding = "20px";
    popup.style.background = "#fff"; /* Changed to white */
    popup.style.color = "#333"; /* Changed to a dark gray */
    popup.style.borderRadius = "10px"; /* Adds rounded corners */
    popup.style.boxShadow = "0 4px 12px rgba(0, 0, 0, 0.15)"; /* Adds a subtle shadow */
    popup.style.zIndex = "10000";
    popup.style.fontFamily = "Arial, sans-serif"; /* Sets a modern font */
    popup.style.textAlign = "center"; /* Centers the text */

    popup.id = "unfaker-popup-123123123";
    document.body.prepend(popup);
}

function hideAvaliacaoPopup() {
    document.querySelector('#unfaker-popup-123123123')?.remove();
}

function waitForElement(selector) {
    return new Promise(resolve => {
        if (document.querySelector(selector)) {
            return resolve(document.querySelector(selector));
        }

        const observer = new MutationObserver(mutations => {
            if (document.querySelector(selector)) {
                observer.disconnect();
                resolve(document.querySelector(selector));
            }
        });

        // If you get "parameter 1 is not of type 'Node'" error, see https://stackoverflow.com/a/77855838/492336
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });
}
