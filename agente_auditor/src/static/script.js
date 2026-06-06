// script.js - Lógica interativa do frontend

document.addEventListener('DOMContentLoaded', () => {
    const uploadZone = document.getElementById('upload-zone');
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.getElementById('file-info');
    const fileNameDisplay = document.getElementById('file-name');
    const removeFileBtn = document.getElementById('remove-file');
    const submitBtn = document.getElementById('submit-btn');
    const loaderContainer = document.getElementById('loader-container');
    const resultsSection = document.getElementById('results-section');
    const checkboxCards = document.querySelectorAll('.checkbox-card');
    
    let currentFile = null;

    // --- Drag and Drop Logic ---
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadZone.addEventListener(eventName, () => {
            uploadZone.classList.add('dragover');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadZone.addEventListener(eventName, () => {
            uploadZone.classList.remove('dragover');
        }, false);
    });

    uploadZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    });

    uploadZone.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length === 0) return;
        
        const file = files[0];
        if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
            alert('Por favor, selecione apenas arquivos PDF.');
            return;
        }

        currentFile = file;
        fileNameDisplay.textContent = file.name;
        uploadZone.style.display = 'none';
        fileInfo.classList.add('visible');
        updateSubmitButtonState();
        
        // Hide previous results
        resultsSection.style.display = 'none';
    }

    removeFileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        currentFile = null;
        fileInput.value = '';
        fileInfo.classList.remove('visible');
        uploadZone.style.display = 'block';
        updateSubmitButtonState();
    });

    // --- Checkbox Logic ---
    checkboxCards.forEach(card => {
        const checkbox = card.querySelector('input[type="checkbox"]');
        
        // Sync visual state on load
        if(checkbox.checked) card.classList.add('selected');

        card.addEventListener('click', (e) => {
            if (e.target !== checkbox) {
                checkbox.checked = !checkbox.checked;
            }
            if (checkbox.checked) {
                card.classList.add('selected');
            } else {
                card.classList.remove('selected');
            }
            updateSubmitButtonState();
        });
    });

    function getSelectedCategories() {
        const selected = [];
        document.querySelectorAll('input[name="categorias"]:checked').forEach(cb => {
            selected.push(cb.value);
        });
        return selected;
    }

    function updateSubmitButtonState() {
        const hasFile = currentFile !== null;
        const hasCategories = getSelectedCategories().length > 0;
        submitBtn.disabled = !(hasFile && hasCategories);
    }

    // --- Form Submission Logic ---
    submitBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        const categorias = getSelectedCategories();
        
        const formData = new FormData();
        formData.append('file', currentFile);
        formData.append('categorias', JSON.stringify(categorias));

        // UI Changes
        submitBtn.style.display = 'none';
        loaderContainer.style.display = 'flex';
        resultsSection.style.display = 'none';

        try {
            const response = await fetch('/auditar', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            displayResults(result);
        } catch (error) {
            console.error('Erro na requisição:', error);
            alert('Falha ao comunicar com o servidor. Tente novamente.');
        } finally {
            submitBtn.style.display = 'block';
            loaderContainer.style.display = 'none';
        }
    });

    // --- Display Results ---
    function displayResults(data) {
        resultsSection.style.display = 'block';
        const banner = document.getElementById('status-banner');
        const resultsGrid = document.getElementById('results-grid');
        
        resultsGrid.innerHTML = ''; // Clear previous
        
        // Render Banner
        banner.className = 'status-banner'; // reset classes
        if (data.status_final === 'erro' || !data.validacao) {
            banner.classList.add('error');
            banner.innerHTML = `<span>❌</span> Falha na Análise: ${data.motivo || 'Erro interno.'}`;
        } else if (data.status_final === 'necessita_revisao') {
            banner.classList.add('warning');
            banner.innerHTML = `<span>⚠️</span> Necessita Revisão: ${data.motivo || 'Verifique os pontos pendentes.'}`;
        } else {
            banner.classList.add('success');
            banner.innerHTML = `<span>✅</span> Análise Concluída com Sucesso!`;
        }

        // Render Estrutura
        if (data.estrutura) {
            const card = document.createElement('div');
            card.className = 'result-card';
            
            let html = `<h4 class="icon-estrutura">Estrutura</h4><ul class="result-list">`;
            
            if (data.estrutura.status === 'erro') {
                html += `<li>Erro: <span class="result-val val-false">${data.estrutura.mensagem}</span></li>`;
            } else {
                html += renderListItem('Introdução', data.estrutura.introducao);
                html += renderListItem('Desenvolvimento', data.estrutura.desenvolvimento);
                html += renderListItem('Conclusão', data.estrutura.conclusao);
            }
            
            html += `</ul>`;
            card.innerHTML = html;
            resultsGrid.appendChild(card);
        }

        // Render Referencias
        if (data.referencias) {
            const card = document.createElement('div');
            card.className = 'result-card';
            
            let html = `<h4 class="icon-referencias">Referências Bibliográficas</h4><ul class="result-list">`;
            
            if (data.referencias.status === 'erro') {
                html += `<li>Erro: <span class="result-val val-false">${data.referencias.mensagem}</span></li>`;
            } else {
                const hasRef = data.referencias.quantidade > 0;
                html += renderListItem('Possui Referências?', hasRef);
                html += `<li>Quantidade: <span class="result-val">${data.referencias.quantidade}</span></li>`;
            }
            
            html += `</ul>`;
            card.innerHTML = html;
            resultsGrid.appendChild(card);
        }

        // Render Ortografia
        if (data.ortografia) {
            const card = document.createElement('div');
            card.className = 'result-card';
            
            let html = `<h4 class="icon-ortografia">Ortografia</h4><ul class="result-list">`;
            
            if (data.ortografia.status === 'erro') {
                html += `<li>Erro: <span class="result-val val-false">${data.ortografia.mensagem}</span></li>`;
            } else {
                const errorColorClass = data.ortografia.erros > 0 ? 'val-false' : 'val-true';
                html += `<li>Erros Identificados: <span class="result-val ${errorColorClass}">${data.ortografia.erros}</span></li>`;
            }
            
            html += `</ul>`;
            card.innerHTML = html;
            resultsGrid.appendChild(card);
        }
        
        // Scroll smoothly to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function renderListItem(label, booleanValue) {
        const text = booleanValue ? 'Encontrado' : 'Ausente';
        const cssClass = booleanValue ? 'val-true' : 'val-false';
        return `<li>${label}: <span class="result-val ${cssClass}">${text}</span></li>`;
    }
});
