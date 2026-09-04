const form = document.getElementById('unitForm');
const tableBody = document.getElementById('unitTableBody');
const formTitle = document.getElementById('formTitle');
const unitIdField = document.getElementById('unitId');

async function loadDropdowns() {
    const donors = await apiGet('/donors/');
    const donorSelect = document.getElementById('donorId');
    donors.forEach(d => {
        const opt = document.createElement('option');
        opt.value = d.donor_id;
        opt.textContent = `${d.name} (${d.blood_group})`;
        donorSelect.appendChild(opt);
    });

    const banks = await apiGet('/banks/');
    const bankSelect = document.getElementById('bankId');
    banks.forEach(b => {
        const opt = document.createElement('option');
        opt.value = b.bank_id;
        opt.textContent = b.name;
        bankSelect.appendChild(opt);
    });
}

async function loadUnits() {
    const units = await apiGet('/units/');
    tableBody.innerHTML = '';
    units.forEach(unit => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${unit.unit_id}</td>
            <td>${unit.donor_name || unit.donor}</td>
            <td>${unit.bank_name || unit.bank}</td>
            <td>${unit.blood_group}</td>
            <td>${unit.collection_date}</td>
            <td>${unit.expiry_date}</td>
            <td>${unit.status}</td>
            <td class="actions">
                <button onclick="editUnit(${unit.unit_id})">Edit</button>
                <button class="btn-delete" onclick="deleteUnit(${unit.unit_id})">Delete</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

function getFormData() {
    return {
        donor: document.getElementById('donorId').value,
        bank: document.getElementById('bankId').value,
        blood_group: document.getElementById('bloodGroup').value,
        collection_date: document.getElementById('collectionDate').value,
        expiry_date: document.getElementById('expiryDate').value,
        status: document.getElementById('status').value,
    };
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = getFormData();
    const id = unitIdField.value;
    try {
        if (id) {
            await apiPut(`/units/${id}/`, data);
        } else {
            await apiPost('/units/', data);
        }
        resetForm();
        loadUnits();
    } catch (err) {
        alert('Error saving unit: ' + err.message);
    }
});

async function editUnit(id) {
    const unit = await apiGet(`/units/${id}/`);
    unitIdField.value = unit.unit_id;
    document.getElementById('donorId').value = unit.donor;
    document.getElementById('bankId').value = unit.bank;
    document.getElementById('bloodGroup').value = unit.blood_group;
    document.getElementById('collectionDate').value = unit.collection_date;
    document.getElementById('expiryDate').value = unit.expiry_date;
    document.getElementById('status').value = unit.status;
    formTitle.textContent = 'Edit Blood Unit';
}

async function deleteUnit(id) {
    if (!confirm('Delete this blood unit?')) return;
    try {
        await apiDelete(`/units/${id}/`);
        loadUnits();
    } catch (err) {
        alert('Error deleting unit: ' + err.message);
    }
}

function resetForm() {
    form.reset();
    unitIdField.value = '';
    formTitle.textContent = 'Add New Blood Unit';
}

loadDropdowns();
loadUnits();