// chart.js

function drawVolumeChart(data) {
  const labels = data.map(item => item.symbol);
  const volumes = data.map(item => item.total_volume);

  const ctx = document.getElementById('volumeChart').getContext('2d');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Total Volume',
        data: volumes,
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function fetchAndRender() {
  fetch("/api/summary")
    .then(res => res.json())
    .then(data => drawVolumeChart(data))
    .catch(err => console.error("Error loading chart data:", err));
}

window.onload = fetchAndRender;
