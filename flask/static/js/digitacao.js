const text = document.getElementById("letras").textContent;
const textoSemEspacos = text.replace(/\s+/g, "");
const text_aberto = textoSemEspacos.split(""); // Quebra o texto em um array de letras
const tamanho_text_aberto = text_aberto.length;
let i = 0;

document.querySelector("body").onkeyup = (event) => {
  const pressionada = event.key;

  if (pressionada === text_aberto[i]) {
    // Se a tecla pressionada for a correta, formata a letra com cor verde
    let formatado = text_aberto.slice(0, i + 1).map((char) => `<span style="color: green;">${char}</span>`);
    i = i + 1;
    let resto = text_aberto.slice(i, tamanho_text_aberto).map((char) => `<span>${char}</span>`);
    document.getElementById("letras").innerHTML = formatado.join("") + resto.join("");
  } else {
    // Se a tecla pressionada for incorreta, formata a letra com cor vermelha
    let armazenador_vermelho = text_aberto.slice(0, i).map((char) => `<span style="color: green;">${char}</span>`);
    let formatado = `<span style="color: red;">${text_aberto[i]}</span>`; // A letra incorreta fica vermelha
    let resto = text_aberto.slice(i + 1, tamanho_text_aberto).map((char) => `<span>${char}</span>`);
    document.getElementById("letras").innerHTML = armazenador_vermelho.join("") + formatado + resto.join("");
  }
};
