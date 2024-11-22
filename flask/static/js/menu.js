https://www.digitalocean.com/community/tutorials/how-to-use-python-markdown-with-flask-and-sqlite

const selectMenu = document.getElementById('menu');
const contentDisplay = document.getElementById('contentDisplay');
const imgInput = document.getElementById('imgInput');
const arquivoInput = document.getElementById('arquivoInput');

function showInputField(selectedValue) {
  imgInput.style.display = 'none';
  arquivoInput.style.display = 'none';

  if (selectedValue === 'img') {
    imgInput.style.display = 'block';
  } else if (selectedValue === 'arquivo') {
    arquivoInput.style.display = 'block';
  }
}

function addContent(selectedValue) {
  let content = ' ';

  if (selectedValue === 'titulo') {
    content = '<h1>Título Exemplo</h1>';
  } else if (selectedValue === 's1') {
    content = '<h2>Subtítulo 1 Exemplo</h2>';
  } else if (selectedValue === 's2') {
    content = '<h3>Subtítulo 2 Exemplo</h3>';
  } else if (selectedValue === 'txt') {
    content = '<h4>Texto Exemplo</h4>';
  }

  if (content) {
    contentDisplay.innerHTML += content;
  }
}

function addImageToContent() {
  const imgFile = document.getElementById('imgFile').files[0];

  if (imgFile) {
    const reader = new FileReader();
    reader.onload = function (e) {
      const imgTag = `<div class="image-container">
        <img src="${e.target.result}" alt="Imagem carregada" style="max-width: 100%; margin-top: 10px;">
        <button class="remove-img-btn" onclick="removeImage(this)">Remover Imagem</button>
      </div>`;
      contentDisplay.innerHTML += imgTag;
    };
    reader.readAsDataURL(imgFile);
  } else {
    alert("Por favor, selecione uma imagem.");
  }
}

function removeImage(button) {
  if (confirm("Deseja realmente remover esta imagem?")) {
    const imageContainer = button.closest('.image-container');
    imageContainer.remove();
  }
}

function addFileToContent() {
  const arquivoFile = document.getElementById('arquivoFile').files[0];

  if (arquivoFile) {
    const fileTag = `<p><a href="${URL.createObjectURL(arquivoFile)}" download="${arquivoFile.name}">
      📎 Baixar ${arquivoFile.name}
    </a></p>`;
    contentDisplay.innerHTML += fileTag;
  } else {
    alert("Por favor, selecione um arquivo.");
  }
}

function saveContent() {
  const content = contentDisplay.innerHTML;
  const blob = new Blob([content], { type: 'text/html' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'conteudo.html';
  link.click();
}

selectMenu.addEventListener('change', function () {
  showInputField(this.value);
  if (this.value !== 'img' && this.value !== 'arquivo') {
    addContent(this.value);
  }
});
