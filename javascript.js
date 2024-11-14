const selectMenu = document.getElementById('menu');
const description = document.getElementById('description');

const tituloInput = document.getElementById('tituloInput');
const sub1Input = document.getElementById('sub1Input');
const sub2Input = document.getElementById('sub2Input');
const imgInput = document.getElementById('imgInput');
const arquivoInput = document.getElementById('arquivoInput');

function showInputField(selectedValue) {
  tituloInput.style.display = 'none';
  sub1Input.style.display = 'none';
  sub2Input.style.display = 'none';
  imgInput.style.display = 'none';
  arquivoInput.style.display = 'none';

  if (selectedValue === 'titulo') {
    tituloInput.style.display = 'block';
    description.textContent = "Adicione um título à página.";
  } else if (selectedValue === 's1') {
    sub1Input.style.display = 'block';
    description.textContent = "Adicione um subtítulo grande.";
  } else if (selectedValue === 's2') {
    sub2Input.style.display = 'block';
    description.textContent = "Adicione um subtítulo menor.";
  } else if (selectedValue === 'img') {
    imgInput.style.display = 'block';
    description.textContent = "Insira uma imagem.";
  } else if (selectedValue === 'arquivo') {
    arquivoInput.style.display = 'block';
    description.textContent = "Carregue arquivos para a página.";
  }
}

selectMenu.addEventListener('change', function() {
  showInputField(selectMenu.value);
});

function addToContent(type) {
  const contentDisplay = document.getElementById('contentDisplay');
  let content = '';

  if (type === 'titulo') {
    const tituloText = document.getElementById('tituloText').value;
    content = `<h1>${tituloText}</h1>`;
  } else if (type === 'sub1') {
    const sub1Text = document.getElementById('sub1Text').value;
    content = `<h2>${sub1Text}</h2>`;
  } else if (type === 'sub2') {
    const sub2Text = document.getElementById('sub2Text').value;
    content = `<h3>${sub2Text}</h3>`;
  } else if (type === 'arquivo') {
    const arquivoFile = document.getElementById('arquivoFile').files[0];
    content = `<p>Arquivo carregado: ${arquivoFile ? arquivoFile.name : 'Nenhum arquivo selecionado'}</p>`;
  }

  contentDisplay.innerHTML += content;
}

function addImageToContent() {
  const contentDisplay = document.getElementById('contentDisplay');
  const imgFile = document.getElementById('imgFile').files[0];
  
  if (imgFile) {
    const reader = new FileReader();
    reader.onload = function(e) {
      contentDisplay.innerHTML += `<img src="${e.target.result}" alt="Imagem carregada" style="max-width: 100%; margin-top: 10px;">`;
    };
    reader.readAsDataURL(imgFile);
  }
}
