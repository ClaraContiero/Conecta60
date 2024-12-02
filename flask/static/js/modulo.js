document.addEventListener("DOMContentLoaded", () => {
    const modulos = document.querySelectorAll(".modulo");

    modulos.forEach((modulo) => {
        const moduloId = modulo.id.replace("modulo-", ""); // Obtém o id_modulo do atributo ID
        const conteudo = document.querySelector(`#conteudos-${moduloId}`);
        const toggle = modulo.querySelector(".toggle");

        // Inicialmente, todos os conteúdos estão ocultos
        conteudo.style.display = "none";

        modulo.addEventListener("click", () => {
            // Fecha todos os outros módulos
            modulos.forEach((outroModulo) => {
                const outroId = outroModulo.id.replace("modulo-", "");
                const outroConteudo = document.querySelector(`#conteudos-${outroId}`);
                const outroToggle = outroModulo.querySelector(".toggle");

                if (outroModulo !== modulo) {
                    outroConteudo.style.display = "none";
                    outroToggle.style.transform = "rotate(0deg)";
                }
            });

            // Alterna o estado do módulo atual
            if (conteudo.style.display === "none") {
                conteudo.style.display = "flex";
                toggle.style.transform = "rotate(90deg)";
            } else {
                conteudo.style.display = "none";
                toggle.style.transform = "rotate(0deg)";
            }
        });
    });
});
