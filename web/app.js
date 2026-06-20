const dashboardEl = document.getElementById('dashboard');
const eventsEl = document.getElementById('events');
const statusEl = document.getElementById('status');
const memoryStatusEl = document.getElementById('memory-status');
const form = document.getElementById('identity-form');
const memoryForm = document.getElementById('memory-form');
const searchInput = document.getElementById('search-input');
const identitiesBody = document.getElementById('identities-body');
const submitBtn = document.getElementById('identity-submit');

let allIdentities = [];
let currentEditId = null;

async function fetchJson(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`${response.status}: ${response.statusText}`);
  }
  return response.json();
}

function showStatus(msg, isError = false) {
  statusEl.textContent = msg;
  statusEl.className = isError ? 'status error' : 'status success';
  statusEl.style.display = 'block';
  setTimeout(() => { statusEl.style.display = 'none'; }, 3000);
}

function showMemoryStatus(msg, isError = false) {
  memoryStatusEl.textContent = msg;
  memoryStatusEl.className = isError ? 'status error' : 'status success';
  memoryStatusEl.style.display = 'block';
  setTimeout(() => { memoryStatusEl.style.display = 'none'; }, 3000);
}

async function loadDashboard() {
  const data = await fetchJson('/dashboard');
  dashboardEl.textContent = JSON.stringify(data, null, 2);
}

async function loadIdentities() {
  allIdentities = await fetchJson('/identities');
  renderIdentities(allIdentities);
}

function renderIdentities(identities) {
  if (identities.length === 0) {
    identitiesBody.innerHTML = '<tr><td colspan="4">No identities found</td></tr>';
    return;
  }

  identitiesBody.innerHTML = identities.map(identity => `
    <tr>
      <td>${identity.id}</td>
      <td>${identity.name}</td>
      <td>${identity.email}</td>
      <td>
        <div class="action-row">
          <button onclick="editIdentity('${identity.id}', '${identity.name}', '${identity.email}')">Edit</button>
          <button class="danger" onclick="deleteIdentity('${identity.id}')">Delete</button>
        </div>
      </td>
    </tr>
  `).join('');
}

function editIdentity(id, name, email) {
  currentEditId = id;
  document.querySelector('input[name="id"]').value = id;
  document.querySelector('input[name="id"]').disabled = true;
  document.querySelector('input[name="name"]').value = name;
  document.querySelector('input[name="email"]').value = email;
  submitBtn.textContent = 'Update identity';
  window.scrollTo(0, 0);
}

async function deleteIdentity(id) {
  if (!confirm(`Delete identity ${id}?`)) return;
  try {
    await fetchJson(`/identity/${id}`, { method: 'DELETE' });
    showStatus(`Deleted identity ${id}`);
    await refreshAll();
  } catch (error) {
    showStatus(`Error: ${error.message}`, true);
  }
}

async function loadMemory() {
  const events = await fetchJson('/memory');
  eventsEl.textContent = JSON.stringify(events, null, 2);
}

async function submitIdentity(event) {
  event.preventDefault();
  const formData = new FormData(form);
  const identity = {
    id: formData.get('id'),
    name: formData.get('name'),
    email: formData.get('email'),
  };

  try {
    let url = '/identity';
    let method = 'POST';

    if (currentEditId) {
      url = `/identity/${currentEditId}`;
      method = 'PUT';
    }

    const result = await fetchJson(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(identity),
    });

    const action = currentEditId ? 'Updated' : 'Created';
    showStatus(`${action} identity ${result.identity.id}`);
    await refreshAll();
    form.reset();
    document.querySelector('input[name="id"]').disabled = false;
    submitBtn.textContent = 'Create identity';
    currentEditId = null;
  } catch (error) {
    showStatus(`Error: ${error.message}`, true);
  }
}

async function submitMemory(event) {
  event.preventDefault();
  const formData = new FormData(memoryForm);
  const payloadText = formData.get('payload')?.trim() || '{}';
  let payload;

  try {
    payload = JSON.parse(payloadText);
  } catch (error) {
    showMemoryStatus('Payload must be valid JSON', true);
    return;
  }

  const body = {
    event: formData.get('event'),
    payload,
  };

  try {
    const result = await fetchJson('/memory', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    showMemoryStatus(`Recorded ${result.memory.event}`);
    await refreshAll();
    memoryForm.reset();
  } catch (error) {
    showMemoryStatus(`Error: ${error.message}`, true);
  }
}

function handleSearch() {
  const searchTerm = searchInput.value.toLowerCase();
  const filtered = allIdentities.filter(i =>
    i.name.toLowerCase().includes(searchTerm) ||
    i.email.toLowerCase().includes(searchTerm)
  );
  renderIdentities(filtered);
}

async function refreshAll() {
  await Promise.all([loadDashboard(), loadIdentities(), loadMemory()]);
}

form.addEventListener('submit', submitIdentity);
memoryForm.addEventListener('submit', submitMemory);
searchInput.addEventListener('input', handleSearch);

refreshAll();
