---
cssclasses:
  - dashboard
---

# TV Shows Dashboard

## Stats

```dataviewjs
const tv        = dv.pages('"TV Shows"').where(p => p.imdb_id && p.status === "watched");
const toWatch   = dv.pages('"TV Shows"').where(p => p.imdb_id && p.status === "to-watch");
const toRewatch = dv.pages('"TV Shows"').where(p => p.imdb_id && p.status === "to-rewatch");
const running   = dv.pages('"TV Shows"').where(p => p.imdb_id && p.series_status === "Running");

const avg = pages => {
  const ratings = pages.map(p => Number(p.my_rating)).filter(r => r >= 1 && r <= 10).array();
  return ratings.length ? (ratings.reduce((a, b) => a + b, 0) / ratings.length).toFixed(1) : "–";
};

dv.table(["Stat", "Value"], [
  ["Watched",          tv.length],
  ["To watch",         toWatch.length],
  ["To rewatch",       toRewatch.length],
  ["Currently airing", running.length],
  ["Avg rating",       avg(tv)],
]);
```

## Ratings Distribution

```dataviewjs
const topLabelsPlugin = {
  id: "tvRatings",
  afterDatasetsDraw(chart) {
    const ctx = chart.ctx;
    ctx.save();
    ctx.font = "bold 11px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "bottom";
    chart.data.datasets.forEach((ds, di) => {
      const meta = chart.getDatasetMeta(di);
      if (meta.hidden) return;
      ds.data.forEach((val, i) => {
        if (!val) return;
        const bar = meta.data[i];
        if (!bar) return;
        ctx.fillStyle = "#666";
        ctx.fillText(String(val), bar.x, bar.y - 3);
      });
    });
    ctx.restore();
  }
};

const tv = dv.pages('"TV Shows"').where(p => p.imdb_id && p.my_rating && p.status === "watched");
const counts = Array(10).fill(0);
for (const p of tv) {
  const r = Number(p.my_rating);
  if (r >= 1 && r <= 10) counts[r - 1]++;
}

const el = dv.el("div", "");
window.renderChart({
  type: "bar",
  data: {
    labels: ["1","2","3","4","5","6","7","8","9","10"],
    datasets: [{
      label: "Count",
      data: counts,
      backgroundColor: "rgba(54,162,235,0.7)",
      borderColor: "rgba(54,162,235,1)",
      borderWidth: 1
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true } },
    layout: { padding: { top: 20 } }
  },
  plugins: [topLabelsPlugin]
}, el);
```

## Watch Activity by Year

```dataviewjs
const topLabelsPlugin = {
  id: "tvYearWatched",
  afterDatasetsDraw(chart) {
    const ctx = chart.ctx;
    ctx.save();
    ctx.font = "bold 11px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "bottom";
    chart.data.datasets.forEach((ds, di) => {
      const meta = chart.getDatasetMeta(di);
      if (meta.hidden) return;
      ds.data.forEach((val, i) => {
        if (!val) return;
        const bar = meta.data[i];
        if (!bar) return;
        ctx.fillStyle = "#666";
        ctx.fillText(String(val), bar.x, bar.y - 3);
      });
    });
    ctx.restore();
  }
};

const tv = dv.pages('"TV Shows"').where(p => p.imdb_id && p.date_watched && p.status === "watched");
const byYear = {};
for (const p of tv) {
  const d = p.date_watched;
  const year = d && d.year ? String(d.year) : (d ? String(d).slice(0, 4) : null);
  if (year && /^\d{4}$/.test(year)) byYear[year] = (byYear[year] || 0) + 1;
}
const years  = Object.keys(byYear).sort();
const counts = years.map(y => byYear[y]);

const el = dv.el("div", "");
window.renderChart({
  type: "bar",
  data: {
    labels: years,
    datasets: [{
      label: "Shows watched",
      data: counts,
      backgroundColor: "rgba(255,159,64,0.7)",
      borderColor: "rgba(255,159,64,1)",
      borderWidth: 1
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true } },
    layout: { padding: { top: 20 } }
  },
  plugins: [topLabelsPlugin]
}, el);
```

## Top Genres

```dataviewjs
const topLabelsPlugin = {
  id: "tvGenres",
  afterDatasetsDraw(chart) {
    const ctx = chart.ctx;
    ctx.save();
    ctx.font = "bold 11px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "bottom";
    chart.data.datasets.forEach((ds, di) => {
      const meta = chart.getDatasetMeta(di);
      if (meta.hidden) return;
      ds.data.forEach((val, i) => {
        if (!val) return;
        const bar = meta.data[i];
        if (!bar) return;
        ctx.fillStyle = "#666";
        ctx.fillText(String(val), bar.x, bar.y - 3);
      });
    });
    ctx.restore();
  }
};

const tv = dv.pages('"TV Shows"').where(p => p.imdb_id && p.genres && p.status === "watched");
const counts = {};
for (const p of tv) {
  const genres = Array.isArray(p.genres) ? p.genres : (p.genres ? [p.genres] : []);
  for (const g of genres) {
    const label = String(g).trim();
    if (label) counts[label] = (counts[label] || 0) + 1;
  }
}
const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 15);
const labels = sorted.map(e => e[0]);
const data   = sorted.map(e => e[1]);

const el = dv.el("div", "");
window.renderChart({
  type: "bar",
  data: {
    labels,
    datasets: [{
      label: "Count",
      data,
      backgroundColor: "rgba(153,102,255,0.7)",
      borderColor: "rgba(153,102,255,1)",
      borderWidth: 1
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true } },
    layout: { padding: { top: 20 } }
  },
  plugins: [topLabelsPlugin]
}, el);
```

## Series Status

```dataviewjs
const topLabelsPlugin = {
  id: "tvStatus",
  afterDatasetsDraw(chart) {
    const ctx = chart.ctx;
    ctx.save();
    ctx.font = "bold 11px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "bottom";
    chart.data.datasets.forEach((ds, di) => {
      const meta = chart.getDatasetMeta(di);
      if (meta.hidden) return;
      ds.data.forEach((val, i) => {
        if (!val) return;
        const bar = meta.data[i];
        if (!bar) return;
        ctx.fillStyle = "#666";
        ctx.fillText(String(val), bar.x, bar.y - 3);
      });
    });
    ctx.restore();
  }
};

const tv = dv.pages('"TV Shows"').where(p => p.imdb_id && p.series_status);
const counts = {};
for (const p of tv) {
  const s = String(p.series_status).trim();
  if (s) counts[s] = (counts[s] || 0) + 1;
}
const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);
const labels = sorted.map(e => e[0]);
const data   = sorted.map(e => e[1]);

const el = dv.el("div", "");
window.renderChart({
  type: "bar",
  data: {
    labels,
    datasets: [{
      label: "Shows",
      data,
      backgroundColor: "rgba(75,192,192,0.7)",
      borderColor: "rgba(75,192,192,1)",
      borderWidth: 1
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true } },
    layout: { padding: { top: 20 } }
  },
  plugins: [topLabelsPlugin]
}, el);
```

## By Release Year

```dataviewjs
const topLabelsPlugin = {
  id: "tvReleaseYear",
  afterDatasetsDraw(chart) {
    const ctx = chart.ctx;
    ctx.save();
    ctx.font = "bold 11px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "bottom";
    chart.data.datasets.forEach((ds, di) => {
      const meta = chart.getDatasetMeta(di);
      if (meta.hidden) return;
      ds.data.forEach((val, i) => {
        if (!val) return;
        const bar = meta.data[i];
        if (!bar) return;
        ctx.fillStyle = "#666";
        ctx.fillText(String(val), bar.x, bar.y - 3);
      });
    });
    ctx.restore();
  }
};

const tv = dv.pages('"TV Shows"').where(p => p.imdb_id && p.year && p.status === "watched");
const byYear = {};
for (const p of tv) {
  const year = String(p.year);
  if (/^\d{4}$/.test(year)) byYear[year] = (byYear[year] || 0) + 1;
}
const years  = Object.keys(byYear).sort();
const counts = years.map(y => byYear[y]);

const el = dv.el("div", "");
window.renderChart({
  type: "bar",
  data: {
    labels: years,
    datasets: [{
      label: "Shows watched",
      data: counts,
      backgroundColor: "rgba(255,205,86,0.7)",
      borderColor: "rgba(255,205,86,1)",
      borderWidth: 1
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true } },
    layout: { padding: { top: 20 } }
  },
  plugins: [topLabelsPlugin]
}, el);
```
