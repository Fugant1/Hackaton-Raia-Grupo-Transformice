
const API_URL = `http://localhost:8000`;

const scan = async post_text => {
    const params = new URLSearchParams({ post_text });

    return fetch(`${API_URL}/scan?${params.toString()}`)
        .then(response => response.json())
        .catch(err => err.message);
}

let latest_path_name = '';

const observer = new MutationObserver(() => {
    if (window.location.pathname == latest_path_name) {
        return;
    }

    if (window.location.pathname.includes('/status/')) {
        latest_path_name = window.location.pathname;
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
    popup.style.background = "#222";
    popup.style.color = "#eee";
    popup.style.borderRadius = "10px";
    popup.style.boxShadow = "0 4px 12px rgba(0, 0, 0, 0.5)";
    popup.style.zIndex = "10000";
    popup.style.fontFamily = "Arial, sans-serif";
    popup.style.textAlign = "center";

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

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });
}
