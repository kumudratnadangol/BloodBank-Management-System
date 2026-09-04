const form = document.getElementById('donorForm');
const tableBody = document.getElementById('donorTableBody');
const formTitle = document.getElementById('formTitle');
const donorIdField = document.getElementById('donorId');

async function loadDonors() {
    const donors = await apiGet('/donors/');
    tableBody.innerHTML = '';
    donors.forEach(donor => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${donor.donor_id}</td>
            <td>${donor.name}</td>
            <td>${donor.blood_group}</td>
            <td>${donor.contact}</td>
            <td>${donor.last_donation_date || '-'}</td>
            <td class="actions">
                <button onclick="editDonor(${donor.donor_id})">Edit</button>
                <button class="btn-delete" onclick="deleteDonor(${donor.donor_id})">Delete</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

function getFormData() {
    return {
        name: document.getElementById('name').value,
        blood_group: document.getElementById('bloodGroup').value,
        dob: document.getElementById('dob').value,
        contact: document.getElementById('contact').value,
        address: document.getElementById('address').value || null,
        last_donation_date: document.getElementById('lastDonationDate').value || null
    };
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = getFormData();
    const id = donorIdField.value;

    try {
        if (id) {
            await apiPut(`/donors/${id}/`, data);
        } else {
            await apiPost('/donors/', data);
        }
        resetForm();
        loadDonors();
    } catch (err) {
        alert('Error saving donor: ' + err.message);
    }
});

async function editDonor(id) {
    const donor = await apiGet(`/donors/${id}/`);
    donorIdField.value = donor.donor_id;
    document.getElementById('name').value = donor.name;
    document.getElementById('bloodGroup').value = donor.blood_group;
    document.getElementById('dob').value = donor.dob;
    document.getElementById('contact').value = donor.contact;
    document.getElementById('address').value = donor.address || '';
    document.getElementById('lastDonationDate').value = donor.last_donation_date || '';
    formTitle.textContent = 'Edit Donor';
}

async function deleteDonor(id) {
    if (!confirm('Delete this donor?')) return;
    try {
        await apiDelete(`/donors/${id}/`);
        loadDonors();
    } catch (err) {
        alert('Error deleting donor: ' + err.message);
    }
}

function resetForm() {
    form.reset();
    donorIdField.value = '';
    formTitle.textContent = 'Add New Donor';
}

loadDonors();