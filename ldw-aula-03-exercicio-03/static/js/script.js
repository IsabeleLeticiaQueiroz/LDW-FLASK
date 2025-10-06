// Script para melhorar a experiência do usuário
document.addEventListener('DOMContentLoaded', function() {
    // Validação adicional do formulário
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const inputs = this.querySelectorAll('input[required], select[required], textarea[required]');
            let valid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    valid = false;
                    input.classList.add('is-invalid');
                } else {
                    input.classList.remove('is-invalid');
                }
            });
            
            if (!valid) {
                event.preventDefault();
                alert('Por favor, preencha todos os campos obrigatórios.');
            }
        });
    });
    
    // Efeito de hover nas linhas da tabela
    const tableRows = document.querySelectorAll('.sylvanian-table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#ffebf3';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
    
    // Adicionar ícones fofos aos títulos
    const titles = document.querySelectorAll('h1, h2, h3');
    titles.forEach(title => {
        if (title.textContent.includes('Família') || title.textContent.includes('Famílias')) {
            title.innerHTML = '<i class="bi bi-house-heart"></i> ' + title.innerHTML;
        } else if (title.textContent.includes('Personagem') || title.textContent.includes('Personagens')) {
            title.innerHTML = '<i class="bi bi-people"></i> ' + title.innerHTML;
        }
    });
});