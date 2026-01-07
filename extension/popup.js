// Popup script
document.getElementById('organizeBtn').addEventListener('click', async () => {
  const statusDiv = document.getElementById('status');
  statusDiv.textContent = '⏳ Organizando...';
  statusDiv.className = '';
  statusDiv.style.display = 'block';
  
  try {
    const result = await chrome.runtime.sendMessage({action: 'organize'});
    statusDiv.textContent = `✅ ${result.message}`;
    statusDiv.className = 'success';
  } catch (error) {
    statusDiv.textContent = `❌ Error: ${error.message}`;
    statusDiv.className = 'error';
  }
});

document.getElementById('removeDuplicatesBtn').addEventListener('click', async () => {
  const statusDiv = document.getElementById('status');
  statusDiv.textContent = '⏳ Eliminando duplicados...';
  statusDiv.className = '';
  statusDiv.style.display = 'block';
  
  try {
    const result = await chrome.runtime.sendMessage({action: 'removeDuplicates'});
    statusDiv.textContent = `✅ ${result.message}`;
    statusDiv.className = 'success';
  } catch (error) {
    statusDiv.textContent = `❌ Error: ${error.message}`;
    statusDiv.className = 'error';
  }
});

document.getElementById('checkLinksBtn').addEventListener('click', async () => {
  const statusDiv = document.getElementById('status');
  statusDiv.textContent = '⏳ Verificando links (puede tomar un momento)...';
  statusDiv.className = '';
  statusDiv.style.display = 'block';
  
  try {
    const result = await chrome.runtime.sendMessage({action: 'checkLinks'});
    statusDiv.textContent = result.message;
    statusDiv.className = result.broken > 0 ? 'error' : 'success';
  } catch (error) {
    statusDiv.textContent = `❌ Error: ${error.message}`;
    statusDiv.className = 'error';
  }
});

document.getElementById('reportBtn').addEventListener('click', async () => {
  const statusDiv = document.getElementById('status');
  statusDiv.textContent = '⏳ Generando reporte...';
  statusDiv.className = '';
  statusDiv.style.display = 'block';
  
  try {
    const result = await chrome.runtime.sendMessage({action: 'report'});
    statusDiv.textContent = result.message;
    statusDiv.className = 'success';
  } catch (error) {
    statusDiv.textContent = `❌ Error: ${error.message}`;
    statusDiv.className = 'error';
  }
});
