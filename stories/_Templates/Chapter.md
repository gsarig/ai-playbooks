<%*
const folderPath = tp.file.folder(true);
const existingChapters = app.vault.getFiles().filter(f => f.path.startsWith(folderPath) && f.name.startsWith("ch-")).length;
const chNum = existingChapters + 1;
const padded = String(chNum).padStart(2, "0");
const chTitle = await tp.system.prompt("Chapter title", "ch-" + padded + " - Your_title_here");
await tp.file.rename(chTitle);
_%>---
chapter: <% chNum %>
title: "<% chTitle %>"
status: draft
edit_pass: 0
wordcount:
pov:
timeline_events: []
locations: []
characters: []
tags:
  - chapter
cssclasses:
  - chapter
---
