
const API_URL = `http//localhost:8000`;

const scan = async url => {
    const params = new URLSearchParams({ url });

    return fetch(`${API_URL}/scan?${params.toString()}`)
        .then(response => response.json())
        .catch(err => err.message);
}

scan(window.location.href).then(showAvaliacaoPopup);

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

    document.body.prepend(popup);
    console.log('aqui')
}
