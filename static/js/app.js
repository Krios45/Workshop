document.addEventListener('DOMContentLoaded', () => {
  const themeKey = 'assetwms-theme';
  const charts = [];

  const getTheme = () => (
    document.documentElement.dataset.theme === 'light' ? 'light' : 'dark'
  );

  const setTheme = (theme) => {
    const nextTheme = theme === 'light' ? 'light' : 'dark';
    document.documentElement.dataset.theme = nextTheme;
    try {
      localStorage.setItem(themeKey, nextTheme);
    } catch (error) {
      // Theme persistence is optional when storage is blocked.
    }
    syncThemeButtons();
    window.dispatchEvent(new CustomEvent('assetwms:themechange', {
      detail: { theme: nextTheme },
    }));
  };

  const syncThemeButtons = () => {
    const nextLabel = getTheme() === 'light' ? 'Tối' : 'Sáng';
    document.querySelectorAll('[data-theme-toggle]').forEach((button) => {
      button.textContent = nextLabel;
      button.setAttribute('title', `Chuyển sang giao diện ${nextLabel.toLowerCase()}`);
    });
  };

  document.querySelectorAll('[data-theme-toggle]').forEach((button) => {
    button.addEventListener('click', () => {
      setTheme(getTheme() === 'light' ? 'dark' : 'light');
    });
  });
  syncThemeButtons();

  const reveals = document.querySelectorAll('.reveal');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) entry.target.classList.add('visible');
    });
  }, { threshold: 0.12 });
  reveals.forEach(el => observer.observe(el));

  document.querySelectorAll('[data-count]').forEach(el => {
    const target = Number(el.dataset.count || 0);
    let current = 0;
    const step = Math.max(1, Math.ceil(target / 60));
    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      el.textContent = current.toLocaleString('vi-VN');
    }, 18);
  });

  const hexToRgba = (hex, alpha) => {
    const value = hex.replace('#', '');
    const int = Number.parseInt(value, 16);
    const red = (int >> 16) & 255;
    const green = (int >> 8) & 255;
    const blue = int & 255;
    return `rgba(${red}, ${green}, ${blue}, ${alpha})`;
  };

  const chartColors = () => {
    const light = getTheme() === 'light';
    return {
      text: light ? '#1f2937' : '#e5edf6',
      muted: light ? '#64748b' : '#aab8cf',
      grid: light ? 'rgba(30, 41, 59, .12)' : 'rgba(148, 163, 184, .22)',
      surface: light ? '#ffffff' : '#111827',
      tooltipBg: light ? 'rgba(15, 23, 42, .94)' : 'rgba(2, 6, 23, .94)',
      palette: ['#00b8d9', '#2563eb', '#f59e0b', '#10b981', '#e11d48', '#8b5cf6'],
    };
  };

  const chartDefaults = () => {
    if (!window.Chart) return;
    const colors = chartColors();
    Chart.defaults.color = colors.text;
    Chart.defaults.borderColor = colors.grid;
    Chart.defaults.font.family = 'Inter';
    Chart.defaults.plugins.tooltip.backgroundColor = colors.tooltipBg;
    Chart.defaults.plugins.tooltip.titleColor = '#ffffff';
    Chart.defaults.plugins.tooltip.bodyColor = '#ffffff';
  };

  const datasetFor = (type, id, data) => {
    const colors = chartColors();
    const palette = colors.palette;

    if (type === 'doughnut' || type === 'pie') {
      return {
        label: id,
        data,
        backgroundColor: palette.map(color => hexToRgba(color, .86)),
        borderColor: colors.surface,
        hoverBackgroundColor: palette,
        hoverBorderColor: colors.surface,
        borderWidth: 3,
        hoverOffset: 8,
      };
    }

    if (type === 'bar') {
      return {
        label: id,
        data,
        backgroundColor: palette.map(color => hexToRgba(color, .72)),
        borderColor: palette,
        borderWidth: 2,
        borderRadius: 8,
        maxBarThickness: 58,
      };
    }

    return {
      label: id,
      data,
      borderColor: palette[1],
      backgroundColor: hexToRgba(palette[0], getTheme() === 'light' ? .18 : .22),
      pointBackgroundColor: palette[2],
      pointBorderColor: colors.surface,
      pointBorderWidth: 2,
      pointRadius: 4,
      pointHoverRadius: 6,
      borderWidth: 3,
      tension: .38,
      fill: true,
    };
  };

  const chartOptions = (type) => {
    const colors = chartColors();
    const circular = type === 'doughnut' || type === 'pie';

    return {
      responsive: true,
      maintainAspectRatio: false,
      cutout: type === 'doughnut' ? '58%' : undefined,
      plugins: {
        legend: {
          display: circular,
          position: 'bottom',
          labels: {
            color: colors.text,
            usePointStyle: true,
            boxWidth: 10,
            padding: 18,
          },
        },
      },
      scales: circular ? {} : {
        x: {
          grid: { color: colors.grid },
          ticks: { color: colors.muted },
        },
        y: {
          beginAtZero: true,
          grid: { color: colors.grid },
          ticks: { color: colors.muted },
        },
      },
    };
  };

  const updateChartTheme = (chart) => {
    const type = chart.config.type;
    const meta = chart.$assetwms || {};
    chart.data.datasets = [datasetFor(type, meta.id || chart.id, meta.data || [])];
    chart.options = chartOptions(type);
    chart.update();
  };

  const makeChart = (id, type, labels, data) => {
    const node = document.getElementById(id);
    if (!node || !window.Chart) return;

    const chart = new Chart(node, {
      type,
      data: {
        labels,
        datasets: [datasetFor(type, id, data)],
      },
      options: chartOptions(type),
    });
    chart.$assetwms = { id, data };
    charts.push(chart);
  };

  chartDefaults();
  makeChart('assetStatusChart', 'doughnut', ['Hoạt động', 'Bảo trì', 'Lỗi'], [112, 9, 7]);
  makeChart('maintenanceTrendChart', 'line', ['T2', 'T3', 'T4', 'T5', 'T6', 'T7'], [8, 12, 10, 18, 14, 20]);
  makeChart('inventoryChart', 'bar', ['Dầu', 'Bearing', 'Sensor', 'Motor', 'Belt'], [86, 12, 0, 22, 41]);
  makeChart('utilChart', 'line', ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], [72, 76, 81, 79, 84, 87]);
  makeChart('failureChart', 'pie', ['Hoạt động', 'Hỏng hóc', 'Bảo trì'], [87, 5, 8]);
  makeChart('stockLevelChart', 'bar', ['Kho A', 'Kho B', 'Kho C', 'Kho D'], [420, 260, 180, 310]);
  makeChart('topMaterialChart', 'bar', ['LUB-220', 'BRG-KIT', 'SEN-IR', 'MOTOR', 'BELT'], [64, 41, 37, 22, 18]);

  window.addEventListener('assetwms:themechange', () => {
    chartDefaults();
    charts.forEach(updateChartTheme);
  });
});
