const modulos = document.querySelectorAll(".modulo-principal");

//o foreach serve para percorrer listas com elementos
//nesse caso, dentro do elemento modulos, ele vai percorrer cada classe que for igual a .conteudo e .toggle
// (elemento atual sendo processado, index => {}
modulos.forEach(modulo => {
    const conteudo = modulo.querySelector(".conteudos");
    const toggle = modulo.querySelector(".toggle");

    conteudo.style.display = "none"; 

//e aqui aplicamos essas propriedades css em cada elemento modulo, contido em modulos
    modulo.addEventListener("click", function () {
        if (conteudo.style.display === "none") {
            toggle.style.transform = "rotate(90deg)";
            conteudo.style.display = "flex";
        
        } else {
            toggle.style.transform = "rotate(0deg)";
            conteudo.style.display = "none";
        }
    });
});
