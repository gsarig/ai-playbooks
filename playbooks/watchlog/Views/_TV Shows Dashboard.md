---
cssclasses:
  - dashboard
---

# TV Shows Dashboard

## Active Seasons

```dataviewjs
const NL = String.fromCharCode(10);
const today = dv.date("today");

const PLACEHOLDER = 'data:image/svg+xml;base64,' + btoa(
  '<svg xmlns="http://www.w3.org/2000/svg" width="36" height="52" viewBox="0 0 36 52">' +
  '<rect width="36" height="52" rx="3" fill="#1e1e1e"/>' +
  '<rect x="3" y="3" width="4" height="4" rx="1" fill="#2e2e2e"/>' +
  '<rect x="10" y="3" width="4" height="4" rx="1" fill="#2e2e2e"/>' +
  '<rect x="17" y="3" width="4" height="4" rx="1" fill="#2e2e2e"/>' +
  '<rect x="24" y="3" width="4" height="4" rx="1" fill="#2e2e2e"/>' +
  '<rect x="3" y="45" width="4" height="4" rx="1" fill="#2e2e2e"/>' +
  '<rect x="10" y="45" width="4" height="4" rx="1" fill="#2e2e2e"/>' +
  '<rect x="17" y="45" width="4" height="4" rx="1" fill="#2e2e2e"/>' +
  '<rect x="24" y="45" width="4" height="4" rx="1" fill="#2e2e2e"/>' +
  '<polygon points="13,20 13,32 24,26" fill="#2e2e2e"/>' +
  '</svg>'
);

function toDateStr(d) {
  if (!d) return "";
  return String(d).slice(0, 10);
}

function fmtDate(d) {
  return toDateStr(d) || "–";
}

async function writeField(filePath, key, value) {
  const tfile = app.vault.getAbstractFileByPath(filePath);
  if (!tfile) return;
  let content = await app.vault.read(tfile);
  const pattern = new RegExp("^(" + key + ":[ \\t]*).*$", "m");
  if (pattern.test(content)) {
    content = content.replace(pattern, "$1" + value);
  } else {
    content = content.replace(NL + "---" + NL, NL + key + ": " + value + NL + "---" + NL);
  }
  await app.vault.modify(tfile, content);
}

const shows = dv.pages('"TV Shows"')
  .where(p => {
    if (!p.imdb_id || p.following === false) return false;
    if (!p.next_season_date) return false;
    const lw = toDateStr(p.last_season_watched);
    const ss = toDateStr(p.next_season_start);
    return !(lw && lw === ss);
  })
  .sort(p => p.next_season_date, "asc")
  .array();

if (shows.length === 0) {
  dv.el("p", "No active seasons right now.");
} else {
  const table = dv.el("table", "", { cls: "active-seasons-table" });
  const thead = table.createEl("thead");
  const hr = thead.createEl("tr");
  ["", "Show", "Season", "Ends", "Following", "Watched"].forEach(h => hr.createEl("th", { text: h }));
  const tbody = table.createEl("tbody");

  const todayStr = toDateStr(today);
  let separatorInserted = false;

  for (const p of shows) {
    if (!separatorInserted && toDateStr(p.next_season_date) >= todayStr) {
      separatorInserted = true;
      const sepRow = tbody.createEl("tr");
      const sepTd = sepRow.createEl("td");
      sepTd.colSpan = 6;
      sepTd.style.padding = "0";
      sepTd.style.height = "2px";
      sepTd.style.background = "var(--color-accent, #7c6af7)";
      sepTd.style.opacity = "0.5";
    }

    const tr = tbody.createEl("tr");

    const tdPoster = tr.createEl("td");
    tdPoster.style.width = "40px";
    tdPoster.style.padding = "2px 4px";
    const img = tdPoster.createEl("img");
    img.src = p.poster ? String(p.poster) : PLACEHOLDER;
    img.style.height = "52px";
    img.style.width = "36px";
    img.style.objectFit = "cover";
    img.style.borderRadius = "3px";
    img.style.display = "block";
    img.onerror = () => { img.onerror = null; img.src = PLACEHOLDER; };

    const tdShow = tr.createEl("td");
    const link = tdShow.createEl("a", { text: p.title || p.file.name, cls: "internal-link" });
    link.dataset.href = p.file.path;
    link.href = p.file.path;

    tdShow.createEl("br");

    if (p.imdb_url) {
      const a = tdShow.createEl("a");
      a.href = String(p.imdb_url);
      a.target = "_blank";
      a.rel = "noopener";
      a.title = "IMDb";
      a.style.marginRight = "4px";
      a.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="#f5c518" xmlns="http://www.w3.org/2000/svg" style="vertical-align:middle"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>'
        + (p.imdb_rating ? '<span style="font-size:11px;vertical-align:middle;margin-left:2px;color:var(--text-muted)">' + p.imdb_rating + '</span>' : '');
    }

    if (p.tvmaze_id) {
      const a = tdShow.createEl("a");
      a.href = "https://www.tvmaze.com/shows/" + String(p.tvmaze_id);
      a.target = "_blank";
      a.rel = "noopener";
      a.title = "TVmaze";
      a.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" xmlns="http://www.w3.org/2000/svg" style="vertical-align:middle"><rect x="2" y="7" width="20" height="13" rx="2"/><path d="M16 2l-4 5-4-5"/></svg>';
    }

    tr.createEl("td", { text: p.current_season ? String(p.current_season) : "–" });
    tr.createEl("td", { text: fmtDate(p.next_season_date) });

    const tdFollow = tr.createEl("td");
    const followCb = tdFollow.createEl("input");
    followCb.type = "checkbox";
    followCb.checked = true;
    followCb.addEventListener("change", async () => {
      await writeField(p.file.path, "following", "false");
    });

    const tdWatched = tr.createEl("td");
    const watchedCb = tdWatched.createEl("input");
    watchedCb.type = "checkbox";
    watchedCb.checked = false;
    watchedCb.addEventListener("change", async () => {
      if (watchedCb.checked) {
        await writeField(p.file.path, "last_season_watched", toDateStr(p.next_season_start));
      }
    });
  }
}
```

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
