const dado = document.getElementById('nome')

formulario.addEventListener('submit', (event) => {
    event.preventDefault(); // Impede o envio padrão do formulário

    let isValid = true; // Variável para controlar se o formulário é válido

    // Validação do campo 'nome'
    if (dado.value.trim() === "") {
        alert("Insira o CPF/Nome");
        isValid = false;    
    }
})