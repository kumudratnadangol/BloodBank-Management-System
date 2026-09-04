const form = document.getElementById('bankForm');
const tableBody = document.getElementById('bankTableBody');
const formTitle = document.getElementById('formTitle');
const bankIdField = document.getElementById('bankId');

async function loadBanks() {
    const banks = await apiGet('/banks/');
    tableBody.innerHTML = '';
    banks.forEach(bank => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${bank.bank_id}</td>
            <td>${bank.name}</td>
            <td>${bank.location}</td>
            <td>${bank.contact}</td>
            <td class="actions">
                <button onclick="editBank(${bank.bank_id})">Edit</button>
                <button class="btn-delete" onclick="deleteBank(${bank.bank_id})">Delete</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

function getFormData() {
    return {
        name: document.getElementById('name').value,
        location: document.getElementById('location').value,
        contact: document.getElementById('contact').value
    };
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = getFormData();
    const id = bankIdField.value;

    try {
        if (id) {
            await apiPut(`/banks/${id}/`, data);
        } else {
            await apiPost('/banks/', data);
        }
        resetForm();
        loadBanks();
    } catch (err) {
        alert('Error saving blood bank: ' + err.message);
    }
});

async function editBank(id) {
    const bank = await apiGet(`/banks/${id}/`);
    bankIdField.value = bank.bank_id;
    document.getElementById('name').value = bank.name;
    document.getElementById('location').value = bank.location;
    document.getElementById('contact').value = bank.contact;
    formTitle.textContent = 'Edit Blood Bank';
}

async function deleteBank(id) {
    if (!confirm('Delete this blood bank?')) return;
    try {
        await apiDelete(`/banks/${id}/`);
        loadBanks();
    } catch (err) {
        alert('Error deleting blood bank: ' + err.message);
    }
}

function resetForm() {
    form.reset();
    bankIdField.value = '';
    formTitle.textContent = 'Add New Blood Bank';
}

loadBanks();