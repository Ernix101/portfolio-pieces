// ! chart JS code

const ctx = document.getElementById('dosageChart');

if (ctx) {
    const labels = JSON.parse(ctx.dataset.labels);
    const data = JSON.parse(ctx.dataset.data);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Records Prescribed',
                data: data,
                borderColor: '#855d33',
                backgroundColor: 'rgba(133, 93, 51, 0.1)',
                borderWidth: 2,
                pointBackgroundColor: '#855d33',
                tension: 0.4,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { ticks: { color: '#aab' }, grid: { color: '#0d1a26' }},
                y: { ticks: { color: '#aab', stepSize: 1 }, grid: { color: '#0d1a26' }, beginAtZero: true },
            }
        }
    });
}

// ! Reports charts code
// * Monthly dosage-chart
const monthlyCtx = document.getElementById('monthlyChart');
if (monthlyCtx) {
    const monthlyLabels = JSON.parse(monthlyCtx.dataset.labels);
    const monthlyData = JSON.parse(monthlyCtx.dataset.data);

    new Chart(monthlyCtx, {
        type: 'line',
        data: {
            labels: monthlyLabels,
            datasets: [{
                label: 'Records Prescribed',
                data: monthlyData,
                borderColor: '#855d33',
                backgroundColor: 'rgba(133, 93, 51, 0.1)',
                borderWidth: 2,
                pointBackgroundColor: '#855d33',
                tension: 0.4,
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: '#aab' }, grid: { color: '#0d1a26' }},
                y: { ticks: { color: '#aab', stepSize: 1 }, grid: { color: '#0d1a26' }, beginAtZero: true },
            }
        }
    });
}

// * Expiry Breakdown bar chart - Reports Page
const expiryCtx = document.getElementById('expiryChart');
if (expiryCtx) {
    const expiryLabels = JSON.parse(expiryCtx.dataset.labels);
    const expiryData = JSON.parse(expiryCtx.dataset.data);

    new Chart(expiryCtx, {
        type: 'bar',
        data: {
            labels: expiryLabels,
            datasets: [{
                label: 'Medications',
                data: expiryData,
                backgroundColor: ['#e05555', '#c4a035', '#4caf7d'],
                borderRadius: 6,
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false }},
            scales: {
                x: { ticks: { color: '#aab' }, grid: { color: '#0d1a26' }},
                y: { ticks: { color: '#aab', stepSize: 1 }, grid: { color: '#0d1a26' }, beginAtZero: true },
            }
        } 
    })
}