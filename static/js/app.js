document.addEventListener('DOMContentLoaded', () => {
  const reveals = document.querySelectorAll('.reveal');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('visible'); });
  }, { threshold: 0.12 });
  reveals.forEach(el => observer.observe(el));

  document.querySelectorAll('[data-count]').forEach(el => {
    const target = Number(el.dataset.count || 0); let current = 0;
    const step = Math.max(1, Math.ceil(target / 60));
    const timer = setInterval(() => { current += step; if (current >= target) { current = target; clearInterval(timer); } el.textContent = current.toLocaleString('vi-VN'); }, 18);
  });

  const chartDefaults = () => {
    if (!window.Chart) return;
    Chart.defaults.color = '#d1d5db';
    Chart.defaults.borderColor = 'rgba(148,163,184,.18)';
    Chart.defaults.font.family = 'Inter';
  };
  chartDefaults();
  const makeChart = (id, type, labels, data) => {
    const node = document.getElementById(id); if (!node || !window.Chart) return;
    new Chart(node, { type, data: { labels, datasets: [{ label: id, data, borderWidth: 2, tension: .4, fill: type === 'line' || type === 'radar' }] }, options: { responsive: true, plugins: { legend: { display: false } }, scales: type === 'doughnut' || type === 'pie' ? {} : { y: { beginAtZero: true } } } });
  };
  makeChart('assetStatusChart', 'doughnut', ['Hoạt động','Bảo trì','Lỗi'], [112,9,7]);
  makeChart('maintenanceTrendChart', 'line', ['T2','T3','T4','T5','T6','T7'], [8,12,10,18,14,20]);
  makeChart('inventoryChart', 'bar', ['Dầu','Bearing','Sensor','Motor','Belt'], [86,12,0,22,41]);
  makeChart('utilChart', 'line', ['Jan','Feb','Mar','Apr','May','Jun'], [72,76,81,79,84,87]);
  makeChart('failureChart', 'pie', ['Hoạt động','Hỏng hóc','Bảo trì'], [87,5,8]);
  makeChart('stockLevelChart', 'bar', ['Kho A','Kho B','Kho C','Kho D'], [420,260,180,310]);
  makeChart('topMaterialChart', 'bar', ['LUB-220','BRG-KIT','SEN-IR','MOTOR','BELT'], [64,41,37,22,18]);
});
