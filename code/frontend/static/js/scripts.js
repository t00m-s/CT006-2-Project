$(document).ready(function () {
    // Richiama la funzione per randomizzare l'ordine all'avvio della pagina
    randomizeListOrder();
});


// Funzione per randomizzare l'ordine di un array
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

// Funzione per randomizzare l'ordine della lista
function randomizeListOrder() {
    const list = document.getElementById("myItems");
    const items = list.getElementsByTagName("li");

    const itemsArray = Array.from(items);
    shuffleArray(itemsArray);

    // Rimuove gli elementi dalla lista
    while (list.firstChild) {
        list.removeChild(list.firstChild);
    }

    // Aggiunge gli elementi randomizzati alla lista
    itemsArray.forEach(item => {
        list.appendChild(item);
    });
}


