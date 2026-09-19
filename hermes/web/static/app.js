document.addEventListener('DOMContentLoaded', async () => {
  const hwStatus = document.getElementById('hw-status');
  const chatBox = document.getElementById('chat-box');
  const chatForm = document.getElementById('chat-form');
  const userInput = document.getElementById('user-input');

  // Load Status
  try {
    const res = await fetch('/api/status');
    if (res.ok) {
      const data = await res.json();
      hwStatus.textContent = `${data.hardware.system_type} • ${data.hardware.cpu_count} CPUs • ${data.hardware.total_ram_gb}GB RAM`;
    }
  } catch (e) {
    hwStatus.textContent = 'Standalone Mode Active';
  }

  // Handle Chat
  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = userInput.value.trim();
    if (!text) return;

    // Add user message
    appendMsg('Operator', text, 'user');
    userInput.value = '';

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      if (res.ok) {
        const data = await res.json();
        appendMsg('Hermes', data.reply, 'assistant');
      } else {
        appendMsg('Hermes', 'Error generating response.', 'assistant');
      }
    } catch (err) {
      appendMsg('Hermes', 'Failed to connect to backend.', 'assistant');
    }
  });

  function appendMsg(sender, text, type) {
    const msgEl = document.createElement('div');
    msgEl.className = `message ${type}`;
    msgEl.innerHTML = `<div class="sender">${sender}</div><div class="bubble">${escapeHtml(text)}</div>`;
    chatBox.appendChild(msgEl);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
});
