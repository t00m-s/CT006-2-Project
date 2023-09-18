$(document).ready(function () {
    // Richiama la funzione per randomizzare l'ordine all'avvio della pagina
    randomizeListOrder();
    activeNavbar();
    btnRounded();
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
    const items = list.getElementsByTagName("div");

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


function activeNavbar(){
    const title = $("title").text();

    switch (title){
        case "Dashboard":
            $("#DashboardNav").addClass("active");
            break;
        case "Add a new project":
        case "Projects":
            $(".ProjectsNav").addClass("active");
            break;
        case "Value project":
        case "View editable projects":
            $("#EditProjectsNav").addClass("active");
            break;
        case "Account":
            $("#AccountNav").addClass("active");
            break;
    }
}

/*function btnRounded(){
    const btn = $(".btn");
    btn.addClass("rounded");
}*/


