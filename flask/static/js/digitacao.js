//let text = "Paulo Silva"; // Basicamente Trocar o meu nome para encontrar o que o professor vai colocar
const text = document.getElementById("letras").textContent;
const text_aberto = text.split(""); // Divide o texto em um array de caracteres
const tamanho_text_aberto = text_aberto.length;
let i = 0;
let Qtd_Letras_Certas = 0;
let Porcentagem_Certas = 0;

document.querySelector("body").onkeydown = (event) => {
    // Previne o comportamento padrão da tecla de espaço (rolagem da página)
    if (event.key === " ") {
        event.preventDefault();  // Impede a rolagem da página ao pressionar espaço
    }

    let Pressionada = event.key;  // Captura a tecla pressionada
    console.log(tamanho_text_aberto);

    if (Pressionada === text_aberto[i]) {
        // Se a letra pressionada for a correta
        let formatado = `<span style="color:#502ffe">${text_aberto[i]}</span>`;  // Letra correta colorida de verde
        let armazen_V = text_aberto.slice(0, i);  // Letras corretas até o momento
        i = i + 1;
        Qtd_Letras_Certas = Qtd_Letras_Certas + 1;
        Porcentagem_Certas = (Qtd_Letras_Certas / tamanho_text_aberto) * 100;
        document.getElementById("Numero").innerHTML = Math.trunc(Porcentagem_Certas).toString();  // Atualiza a porcentagem

        let resto = text_aberto.slice(i, tamanho_text_aberto);  // Letras restantes
        document.getElementById("letras").innerHTML = armazen_V.join("") + formatado + resto.join("");  // Exibe o texto com a letra correta em verde
    } else {
        // Se a letra pressionada for incorreta
        let formatado = `<span style="color: red">${text_aberto[i]}</span>`;  // Letra incorreta colorida de vermelho
        let armazenador_vermelho = text_aberto.slice(0, i);  // Letras até o erro
        let resto = text_aberto.slice(i + 1, tamanho_text_aberto);  // Letras restantes
        document.getElementById("letras").innerHTML = armazenador_vermelho.join("") + formatado + resto.join("");  // Exibe a letra incorreta em vermelho
        i = i + 1;
    }
};
