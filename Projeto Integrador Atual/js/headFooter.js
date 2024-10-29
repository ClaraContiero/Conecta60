/*Header */

function loadHeader() {
    fetch('header.html') // acho que pega a página em si
        .then(response => {
            if (!response.ok) {
                throw new Error('Deu erro.');
            }
            return response.text();
        })
        .then(data => {
            document.getElementById('header').innerHTML = data; // pega todos os elementos da página com esse id
        })
        .catch(error => {
            console.error('Houve um problema com a solicitação:', error);
        });
}

document.addEventListener("DOMContentLoaded", loadHeader); // carrega a função nas páginas


/*Footer */

function loadFooter() {
    fetch('footer.html') // acho que pega a página em si
        .then(response => {
            if (!response.ok) {
                throw new Error('Deu erro.');
            }
            return response.text();
        })
        .then(data => {
            document.getElementById('footer').innerHTML = data; // pega todos os elementos da página com esse id
        })
        .catch(error => {
            console.error('Houve um problema com a solicitação:', error);
        });
}

document.addEventListener("DOMContentLoaded", loadFooter); // carrega a função nas páginas