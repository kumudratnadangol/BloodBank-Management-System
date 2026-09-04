const form = document.getElementById('requestForm');
const tableBody = document.getElementById('requestTableBody');
const formTitle = document.getElementById('formTitle');
const requestIdField = document.getElementById('requestId');

async function loadHospitalDropdown() {
    const hospitals = await apiGet('/hospitals/');
    const select = document.getElementById('hospitalId');
    hospitals.forEach(h => {
        const opt = document.createElement('option');
        opt.value = h.hospital_id;
        opt.textContent = h.name;
        select.appendChild(opt);
    });
}

async function loadRequests() {
    const requests = await apiGet('/requests/');
    tableBody.innerHTML = '';
    requests.forEach(req => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${req.request_id}</td>
            <td>${req.hospital_name || req.hospital}</td>
            <td>${req.blood_group}</td>
            <td>${req.units_requested}</td>
            <td>${req.status}</td>
            <td>${req.request_date}</td>
            <td class="actions">
                <button onclick="editRequest(${req.request_id})">Edit</button>
                <button class="btn-delete" onclick="deleteRequest(${req.request_id})">Delete</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

function getFormData() {
    return {
        hospital: document.getElementById('hospitalId').value,
        blood_group: document.getElementById('bloodGroup').value,
        units_requested: document.getElementById('unitsRequested').value,
        status: document.getElementById('status').value,
    };
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = getFormData();
    const id = requestIdField.value;
    try {
        if (id) {
            await apiPut(`/requests/${id}/`, data);
        } else {
            await apiPost('/requests/', data);
        }
        resetForm();
        loadRequests();
    } catch (err) {
        alert('Error saving request: ' + err.message);
    }
});

async function editRequest(id) {
    const req = await apiGet(`/requests/${id}/`);
    requestIdField.value = req.request_id;
    document.getElementById('hospitalId').value = req.hospital;
    document.getElementById('bloodGroup').value = req.blood_group;
    document.getElementById('unitsRequested').value = req.units_requested;
    document.getElementById('status').value = req.status;
    formTitle.textContent = 'Edit Request';
}

async function deleteRequest(id) {
    if (!confirm('Delete this request?')) return;
    try {
        await apiDelete(`/requests/${id}/`);
        loadRequests();
    } catch (err) {
        alert('Error deleting request: ' + err.message);
    }
}

function resetForm() {
    form.reset();
    requestIdField.value = '';
    formTitle.textContent = 'Add New Request';
}

loadHospitalDropdown();
loadRequests();