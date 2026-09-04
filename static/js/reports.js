const traceForm = document.getElementById('traceForm');
const inventoryForm = document.getElementById('inventoryForm');
const expireBtn = document.getElementById('expireBtn');

traceForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const hospitalId = document.getElementById('hospitalTraceId').value;
    try {
        const data = await apiGet(`/reports/hospital/${hospitalId}/trace/`);
        const tbody = document.getElementById('traceTableBody');
        tbody.innerHTML = '';
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5">No fulfillments found for this hospital.</td></tr>';
        } else {
            data.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.request_id}</td>
                    <td>${item.donor_name}</td>
                    <td>${item.donor_blood_group}</td>
                    <td>${item.unit_id}</td>
                    <td>${item.fulfilled_date}</td>
                `;
                tbody.appendChild(row);
            });
        }
        document.getElementById('traceTable').style.display = 'table';
    } catch (err) {
        alert('Error running trace: ' + err.message);
    }
});

inventoryForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    try {
        const data = await apiGet('/reports/bank-inventory/');
        const tbody = document.getElementById('inventoryTableBody');
        tbody.innerHTML = '';
        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.bank_id}</td>
                <td>${item.bank_name}</td>
                <td>${item.total_units}</td>
                <td>${item.available_units}</td>
                <td>${item.reserved_for_requests}</td>
            `;
            tbody.appendChild(row);
        });
        document.getElementById('inventoryTable').style.display = 'table';
    } catch (err) {
        alert('Error loading inventory: ' + err.message);
    }
});

expireBtn.addEventListener('click', async () => {
    try {
        const response = await fetch('/api/tasks/expire-units/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const data = await response.json();
        document.getElementById('expireMsg').textContent = data.message;
    } catch (err) {
        alert('Error triggering task: ' + err.message);
    }
});