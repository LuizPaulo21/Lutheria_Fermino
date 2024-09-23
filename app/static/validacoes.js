//Busca o formulário pelo seu ID e os campos do mesmo
const formulario = document.getElementById('formcad')
const nome = document.getElementById('nome')
const cpf = document.getElementById('cpf')
const endereco = document.getElementById('endereco')
const cidade = document.getElementById('cidade')
const estado = document.getElementById('estado')
const cep = document.getElementById('cep')
const telefone = document.getElementById('telefone')
const email = document.getElementById('email')

formulario.addEventListener('submit', (event) => {
    event.preventDefault(); // Impede o envio padrão do formulário

    let isValid = true; // Variável para controlar se o formulário é válido

    // Validação do campo 'nome'
    if (nome.value.trim() === "") {
        alert("Insira seu nome");
        isValid = false;
    }

    // Validação do campo 'cpf'
    if (cpf.value.trim() === "" || !validarCPF(cpf.value)) {
        alert("Insira um CPF válido");
        isValid = false;
    }

     // Validação do campo 'endereco'
    if (endereco.value.trim() === "") {
        alert("Insira seu Endereço");
        isValid = false;
    }

    // Validação do campo 'Cidade'
    if (cidade.value.trim() === "") {
        alert("Insira sua Cidade");
        isValid = false;
    }
    
    // Validação do campo 'Estado'
    if (estado.dade.value.trim() === "") {
        alert("Insira seu Estado");
        isValid = false;
    }

    // Validação do campo 'CEP'
    if (cep.value.trim() === "") {
        alert("Insira seu CEP");
        isValid = false;
    }

    // Validação do campo 'Telefone'
    if (telefone.value.trim() === "") {
        alert("Insira seu Telefone");
        isValid = false;
    }

    // Validação do campo 'Email'
    if (email.value.trim() === "") {
        alert("Insira seu E-mail");
        isValid = false;
    }
}
)

function validarCPF(cpf) {
    // Remove caracteres não numéricos
    cpf = cpf.replace(/\D/g, '');

    // Verifica se o CPF tem 11 dígitos
    if (cpf.length !== 11) {
        return false;   

    }

    // Verifica se todos os dígitos são iguais (CPF inválido)
    if (/^(\d)\1+$/.test(cpf)) {
        return false;   

    }

    // Cálculo do primeiro dígito verificador
    let soma = 0;
    for (let i = 0; i < 9; i++) {
        soma += parseInt(cpf.charAt(i)) * (10 - i);
    }
    let resto = soma % 11;
    let digito1 = resto < 2 ? 0 : 11 - resto;   


    // Cálculo do segundo dígito verificador
    soma = 0;
    for (let i = 0; i < 10; i++) {
        soma += parseInt(cpf.charAt(i)) * (11 - i);
    }
    resto = soma % 11;
    let digito2 = resto < 2 ? 0 : 11 - resto;

    // Verifica se os dígitos verificadores calculados correspondem aos fornecidos
    return digito1 === parseInt(cpf.charAt(9)) && digito2 === parseInt(cpf.charAt(10));
}