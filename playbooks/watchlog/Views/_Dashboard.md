---
cssclasses:
  - dashboard
---

# Dashboard

## Stats

```dataviewjs
const movies   = dv.pages('"Movies"').where(p => p.imdb_id && p.status === "watched");
const tv       = dv.pages('"TV Shows"').where(p => p.imdb_id && p.status === "watched");
const toWatch  = dv.pages('"Movies" or "TV Shows"').where(p => p.imdb_id && p.status === "to-watch");
const toRewatch = dv.pages('"Movies" or "TV Shows"').where(p => p.imdb_id && p.status === "to-rewatch");

const avg = pages => {
  const ratings = pages.map(p => Number(p.my_rating)).filter(r => r >= 1 && r <= 10).array();
  return ratings.length ? (ratings.reduce((a, b) => a + b, 0) / ratings.length).toFixed(1) : "–";
};

dv.table(["Stat", "Value"], [
  ["Movies watched",   movies.length],
  ["TV shows watched", tv.length],
  ["To watch",         toWatch.length],
  ["To rewatch",       toRewatch.length],
  ["Avg movie rating", avg(movies)],
  ["Avg TV rating",    avg(tv)],
]);
```

## Ratings Distribution

```dataviewjs
const segLabelsPlugin = {
  id: "segLabels1",
  afterDatasetsDraw(chart) {
    const ctx = chart.ctx;
    ctx.save();
    ctx.font = "bold 11px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    chart.data.datasets.forEach((ds, di) => {
      const meta = chart.getDatasetMeta(di);
      if (meta.hidden) return;
      ds.data.forEach((val, i) => {
        if (!val) return;
        const bar = meta.data[i];
        if (!bar) return;
        if (Math.abs(bar.y - bar.base) < 16) return;
        ctx.fillStyle = "#fff";
        ctx.fillText(String(val), bar.x, (bar.y + bar.base) / 2);
      });
    });
    ctx.restore();
  },
  afterDraw(chart) {
    const ctx = chart.ctx;
    ctx.save();
    ctx.font = "bold 11px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "bottom";
    ctx.fillStyle = "#666";
    const n = chart.data.labels.length;
    for (let i = 0; i < n; i++) {
      let total = 0, topY = Infinity, x = null;
      chart.data.datasets.forEach((ds, di) => {
        const meta = chart.getDatasetMeta(di);
        if (meta.hidden) return;
        const bar = meta.data[i];
        if (!bar) return;
        total += ds.data[i] || 0;
        if (bar.y < topY) { topY = bar.y; x = bar.x; }
      });
      if (total > 0 && x !== null) ctx.fillText(String(total), x, topY - 3);
    }
    ctx.restore();
  }
};

const movies = dv.pages('"Movies"').where(p => p.imdb_id && p.my_rating);
const tv     = dv.pages('"TV Shows"').where(p => p.imdb_id && p.my_rating);

const movieCounts = Array(10).fill(0);
const tvCounts    = Array(10).fill(0);

for (const p of movies) {
  const r = Number(p.my_rating);
  if (r >= 1 && r <= 10) movieCounts[r - 1]++;
}
for (const p of tv) {
  const r = Number(p.my_rating);
  if (r >= 1 && r <= 10) tvCounts[r - 1]++;
}

dv.header(4, "All ratings (movies + TV)");
const el1 = dv.el("div", "");
window.renderChart({
  type: "bar",
  data: {
    labels: ["1","2","3","4","5","6","7","8","9","10"],
    datasets: [
      {
        label: "Movies",
        data: movieCounts,
        backgroundColor: "rgba(54,162,235,0.85)",
        borderColor: "rgba(54,162,235,1)",
        borderWidth: 1
      },
      {
        label: "TV Shows",
        data: tvCounts,
        backgroundColor: "rgba(255,99,132,0.85)",
        borderColor: "rgba(255,99,132,1)",
        borderWidth: 1
      }
    ]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: true } },
    scales: {
      x: { stacked: true },
      y: { beginAtZero: true, stacked: true }
    },
    layout: { padding: { top: 20 } }
  },
  plugins: [segLabelsPlugin]
}, el1);
```

## Watch Activity by Year

```dataviewjs
const segLabelsPlugin = {
  id: "segLabels2",
  afterDatasetsDraw(chart) {
    const ctx = chart.ctx;
    ctx.save();
    ctx.font = "bold 11px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    chart.data.datasets.forEach((ds, di) => {
      const meta = chart.getDatasetMeta(di);
      if (meta.hidden) return;
      ds.data.forEach((val, i) => {
        if (!val) return;
        const bar = meta.data[i];
        if (!bar) return;
        if (Math.abs(bar.y - bar.base) < 16) return;
        ctx.fillStyle = "#fff";
        ctx.fillText(String(val), bar.x, (bar.y + bar.base) / 2);
      });
    });
    ctx.restore();
  },
  afterDraw(chart) {
    const ctx = chart.ctx;
    ctx.save();
    ctx.font = "bold 11px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "bottom";
    ctx.fillStyle = "#666";
    const n = chart.data.labels.length;
    for (let i = 0; i < n; i++) {
      let total = 0, topY = Infinity, x = null;
      chart.data.datasets.forEach((ds, di) => {
        const meta = chart.getDatasetMeta(di);
        if (meta.hidden) return;
        const bar = meta.data[i];
        if (!bar) return;
        total += ds.data[i] || 0;
        if (bar.y < topY) { topY = bar.y; x = bar.x; }
      });
      if (total > 0 && x !== null) ctx.fillText(String(total), x, topY - 3);
    }
    ctx.restore();
  }
};

const watchedMovies = dv.pages('"Movies"').where(p => p.imdb_id && p.date_watched && p.status === "watched");
const watchedTV     = dv.pages('"TV Shows"').where(p => p.imdb_id && p.date_watched && p.status === "watched");

const byYearMovies = {};
const byYearTV     = {};

for (const p of watchedMovies) {
  const d = p.date_watched;
  const year = d && d.year ? String(d.year) : (d ? String(d).slice(0, 4) : null);
  if (year && /^\d{4}$/.test(year)) byYearMovies[year] = (byYearMovies[year] || 0) + 1;
}
for (const p of watchedTV) {
  const d = p.date_watched;
  const year = d && d.year ? String(d.year) : (d ? String(d).slice(0, 4) : null);
  if (year && /^\d{4}$/.test(year)) byYearTV[year] = (byYearTV[year] || 0) + 1;
}

const years       = [...new Set([...Object.keys(byYearMovies), ...Object.keys(byYearTV)])].sort();
const movieCounts = years.map(y => byYearMovies[y] || 0);
const tvCounts    = years.map(y => byYearTV[y]     || 0);

const el2 = dv.el("div", "");
window.renderChart({
  type: "bar",
  data: {
    labels: years,
    datasets: [
      {
        label: "Movies",
        data: movieCounts,
        backgroundColor: "rgba(54,162,235,0.85)",
        borderColor: "rgba(54,162,235,1)",
        borderWidth: 1
      },
      {
        label: "TV Shows",
        data: tvCounts,
        backgroundColor: "rgba(255,99,132,0.85)",
        borderColor: "rgba(255,99,132,1)",
        borderWidth: 1
      }
    ]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: true } },
    scales: {
      x: { stacked: true },
      y: { beginAtZero: true, stacked: true }
    },
    layout: { padding: { top: 20 } }
  },
  plugins: [segLabelsPlugin]
}, el2);
```

## Top Genres

```dataviewjs
const segLabelsPlugin = {
  id: "segLabels3",
  afterDatasetsDraw(chart) {
    const ctx = chart.ctx;
    ctx.save();
    ctx.font = "bold 11px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    chart.data.datasets.forEach((ds, di) => {
      const meta = chart.getDatasetMeta(di);
      if (meta.hidden) return;
      ds.data.forEach((val, i) => {
        if (!val) return;
        const bar = meta.data[i];
        if (!bar) return;
        if (Math.abs(bar.y - bar.base) < 16) return;
        ctx.fillStyle = "#fff";
        ctx.fillText(String(val), bar.x, (bar.y + bar.base) / 2);
      });
    });
    ctx.restore();
  },
  afterDraw(chart) {
    const ctx = chart.ctx;
    ctx.save();
    ctx.font = "bold 11px sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "bottom";
    ctx.fillStyle = "#666";
    const n = chart.data.labels.length;
    for (let i = 0; i < n; i++) {
      let total = 0, topY = Infinity, x = null;
      chart.data.datasets.forEach((ds, di) => {
        const meta = chart.getDatasetMeta(di);
        if (meta.hidden) return;
        const bar = meta.data[i];
        if (!bar) return;
        total += ds.data[i] || 0;
        if (bar.y < topY) { topY = bar.y; x = bar.x; }
      });
      if (total > 0 && x !== null) ctx.fillText(String(total), x, topY - 3);
    }
    ctx.restore();
  }
};

const watchedMovies = dv.pages('"Movies"').where(p => p.imdb_id && p.genres && p.status === "watched");
const watchedTV     = dv.pages('"TV Shows"').where(p => p.imdb_id && p.genres && p.status === "watched");

const movieGenres = {};
const tvGenres    = {};

for (const p of watchedMovies) {
  const genres = Array.isArray(p.genres) ? p.genres : (p.genres ? [p.genres] : []);
  for (const g of genres) {
    const label = String(g).trim();
    if (label) movieGenres[label] = (movieGenres[label] || 0) + 1;
  }
}
for (const p of watchedTV) {
  const genres = Array.isArray(p.genres) ? p.genres : (p.genres ? [p.genres] : []);
  for (const g of genres) {
    const label = String(g).trim();
    if (label) tvGenres[label] = (tvGenres[label] || 0) + 1;
  }
}

const allGenres = [...new Set([...Object.keys(movieGenres), ...Object.keys(tvGenres)])];
const sorted    = allGenres
  .map(g => [g, (movieGenres[g] || 0) + (tvGenres[g] || 0)])
  .sort((a, b) => b[1] - a[1])
  .slice(0, 15);

const labels    = sorted.map(e => e[0]);
const movieData = labels.map(g => movieGenres[g] || 0);
const tvData    = labels.map(g => tvGenres[g]    || 0);

const el3 = dv.el("div", "");
window.renderChart({
  type: "bar",
  data: {
    labels,
    datasets: [
      {
        label: "Movies",
        data: movieData,
        backgroundColor: "rgba(54,162,235,0.85)",
        borderColor: "rgba(54,162,235,1)",
        borderWidth: 1
      },
      {
        label: "TV Shows",
        data: tvData,
        backgroundColor: "rgba(255,99,132,0.85)",
        borderColor: "rgba(255,99,132,1)",
        borderWidth: 1
      }
    ]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: true } },
    scales: {
      x: { stacked: true },
      y: { beginAtZero: true, stacked: true }
    },
    layout: { padding: { top: 20 } }
  },
  plugins: [segLabelsPlugin]
}, el3);
```
