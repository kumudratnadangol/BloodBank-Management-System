const form = document.getElementById('hospitalForm');
const tableBody = document.getElementById('hospitalTableBody');
const formTitle = document.getElementById('formTitle');
const hospitalIdField = document.getElementById('hospitalId');

async function loadHospitals() {
    const hospitals = await apiGet('/hospitals/');
    tableBody.innerHTML = '';
    hospitals.forEach(hospital => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${hospital.hospital_id}</td>
            <td>${hospital.name}</td>
            <td>${hospital.location}</td>
            <td>${hospital.contact}</td>
            <td class="actions">
                <button onclick="editHospital(${hospital.hospital_id})">Edit</button>
                <button class="btn-delete" onclick="deleteHospital(${hospital.hospital_id})">Delete</button>
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
    const id = hospitalIdField.value;

    try {
        if (id) {
            await apiPut(`/hospitals/${id}/`, data);
        } else {
            await apiPost('/hospitals/', data);
        }
        resetForm();
        loadHospitals();
    } catch (err) {
        alert('Error saving hospital: ' + err.message);
    }
});

async function editHospital(id) {
    const hospital = await apiGet(`/hospitals/${id}/`);
    hospitalIdField.value = hospital.hospital_id;
    document.getElementById('name').value = hospital.name;
    document.getElementById('location').value = hospital.location;
    document.getElementById('contact').value = hospital.contact;
    formTitle.textContent = 'Edit Hospital';
}

async function deleteHospital(id) {
    if (!confirm('Delete this hospital?')) return;
    try {
        await apiDelete(`/hospitals/${id}/`);
        loadHospitals();
    } catch (err) {
        alert('Error deleting hospital: ' + err.message);
    }
}

function resetForm() {
    form.reset();
    hospitalIdField.value = '';
    formTitle.textContent = 'Add New Hospital';
}

loadHospitals();