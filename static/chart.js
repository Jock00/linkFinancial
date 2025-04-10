// chart.js

function drawBuySellTrend(data) {
  const dates = [...new Set(data.map(item => item.date))].sort();
  const symbols = [...new Set(data.map(item => item.symbol))];

  const datasets = [];

  symbols.forEach(symbol => {
    const buyData = dates.map(date => {
      const entry = data.find(d => d.symbol === symbol && d.date === date && d.side === 'BUY');
      return entry ? entry.volume : 0;
    });

    const sellData = dates.map(date => {
      const entry = data.find(d => d.symbol === symbol && d.date === date && d.side === 'SELL');
      return entry ? entry.volume : 0;
    });

    datasets.push({
      label: `${symbol} BUY`,
      data: buyData,
      borderColor: 'blue',
      backgroundColor: 'blue',
      fill: false,
      tension: 0.2
    });

    datasets.push({
      label: `${symbol} SELL`,
      data: sellData,
      borderColor: 'red',
      backgroundColor: 'red',
      fill: false,
      borderDash: [5, 5],
      tension: 0.2
    });
  });

  const ctx = document.getElementById('buySellChart').getContext('2d');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: dates,
      datasets: datasets
    },
    options: {
      responsive: true,
      interaction: {
        mode: 'nearest',
        intersect: false
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function fetchAndRender() {
  fetch("/api/buy_sell_trend")
    .then(res => res.json())
    .then(data => drawBuySellTrend(data));
}

window.onload = fetchAndRender;
