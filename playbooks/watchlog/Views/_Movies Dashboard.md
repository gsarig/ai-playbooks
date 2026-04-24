---
cssclasses:
  - dashboard
---

# Movies Dashboard

## Stats

```dataviewjs
const movies    = dv.pages('"Movies"').where(p => p.imdb_id && p.status === "watched");
const toWatch   = dv.pages('"Movies"').where(p => p.imdb_id && p.status === "to-watch");
const toRewatch = dv.pages('"Movies"').where(p => p.imdb_id && p.status === "to-rewatch");

const avg = pages => {
  const ratings = pages.map(p => Number(p.my_rating)).filter(r => r >= 1 && r <= 10).array();
  return ratings.length ? (ratings.reduce((a, b) => a + b, 0) / ratings.length).toFixed(1) : "–";
};

const runtimes  = movies.map(p => Number(p.runtime)).filter(r => r > 0).array();
const totalMins = runtimes.reduce((a, b) => a + b, 0);
const hours     = Math.floor(totalMins / 60);
const mins      = totalMins % 60;

dv.table(["Stat", "Value"], [
  ["Watched",       movies.length],
  ["To watch",      toWatch.length],
  ["To rewatch",    toRewatch.length],
  ["Avg rating",    avg(movies)],
  ["Total runtime", hours + "h " + mins + "m"],
]);
```

## Ratings Distribution

```dataviewjs
const topLabelsPlugin = {
  id: "mRatings",
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

const movies = dv.pages('"Movies"').where(p => p.imdb_id && p.my_rating && p.status === "watched");
const counts = Array(10).fill(0);
for (const p of movies) {
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
  id: "mYearWatched",
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

const movies = dv.pages('"Movies"').where(p => p.imdb_id && p.date_watched && p.status === "watched");
const byYear = {};
for (const p of movies) {
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
      label: "Movies watched",
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
  id: "mGenres",
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

const movies = dv.pages('"Movies"').where(p => p.imdb_id && p.genres && p.status === "watched");
const counts = {};
for (const p of movies) {
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

## Top Directors

```dataviewjs
const topLabelsPlugin = {
  id: "mDirectors",
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

const movies = dv.pages('"Movies"').where(p => p.imdb_id && p.directors && p.status === "watched");
const counts = {};
for (const p of movies) {
  const directors = Array.isArray(p.directors) ? p.directors : (p.directors ? [p.directors] : []);
  for (const d of directors) {
    const label = String(d).trim();
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

## Runtime Distribution

```dataviewjs
const topLabelsPlugin = {
  id: "mRuntime",
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

const movies = dv.pages('"Movies"').where(p => p.imdb_id && p.runtime && p.status === "watched");
const buckets = { "Under 80m": 0, "80-100m": 0, "100-120m": 0, "120-150m": 0, "150m+": 0 };
for (const p of movies) {
  const r = Number(p.runtime);
  if (!r) continue;
  if (r < 80)       buckets["Under 80m"]++;
  else if (r < 100) buckets["80-100m"]++;
  else if (r < 120) buckets["100-120m"]++;
  else if (r < 150) buckets["120-150m"]++;
  else              buckets["150m+"]++;
}
const labels = Object.keys(buckets);
const data   = Object.values(buckets);

const el = dv.el("div", "");
window.renderChart({
  type: "bar",
  data: {
    labels,
    datasets: [{
      label: "Movies",
      data,
      backgroundColor: "rgba(255,99,132,0.7)",
      borderColor: "rgba(255,99,132,1)",
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
  id: "mReleaseYear",
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

const movies = dv.pages('"Movies"').where(p => p.imdb_id && p.year && p.status === "watched");
const byYear = {};
for (const p of movies) {
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
      label: "Movies watched",
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
