function flutuacaoPassiva() {
    const images = document.getElementsByClassName('img');  
    Array.from(images).forEach(img => {
        const randomX = Math.sin(Date.now() / 500) * 5; // movimento suave no eixo X
        const randomY = Math.cos(Date.now() / 500) * 5; // movimento suave no eixo Y
        img.style.transform = `translate(${randomX}px, ${randomY}px)`; // aplica o estilo transform para cada imagem
    });
}

// Atualiza a posição das imagens a cada 100ms
setInterval(flutuacaoPassiva, 100);
