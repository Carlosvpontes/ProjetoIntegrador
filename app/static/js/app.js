// Confirmação antes de ações irreversíveis (M40).
// Uso: <form data-confirmar="Tem certeza que deseja excluir ...?">
document.addEventListener("submit", (evento) => {
  const mensagem = evento.target.dataset.confirmar;
  if (mensagem && !window.confirm(mensagem)) {
    evento.preventDefault();
  }
});
