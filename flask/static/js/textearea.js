function autoResize(element) {
    element.style.height = "auto"; // Reseta a altura para calcular o novo tamanho
    element.style.height = (element.scrollHeight) + "px"; // Ajusta a altura para o tamanho do conteúdo
}