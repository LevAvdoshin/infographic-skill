---
name: infographic
description: Generate beautiful infographic slides as PNG from text + data. Use when the user wants to turn metrics, comparisons, channel economics, or any data into beautiful 1400x800px PNG slides. Approach: Claude writes HTML/CSS/Chart.js → Playwright screenshots to PNG → saves to ~/Desktop/<name>-<date>/. Free, local, no API. Triggers on "сделай инфографику", "нарисуй слайд", "визуализируй данные", "make infographic", "generate slides", "собери визуалы", "сделай слайд".
---

# Infographic Skill

Turns text/data into beautiful PNG slides. Stack: HTML + Chart.js + Playwright.

## Approach

1. **Write HTML slide** → clean card layout, Inter font, Chart.js for charts
2. **Screenshot with Playwright** via `scripts/render.js`
3. **Save PNG** to `~/Desktop/<name>-<date>/`
4. **Open folder**: `open ~/Desktop/<name>-<date>/`

## Render script

```bash
node ~/.claude/skills/infographic/scripts/render.js <slide.html> <out.png>
```

Always render at 1400×800 viewport (16:9). Script is at `scripts/render.js`.

## Design system

```css
/* Palette */
--blue:   #2563EB;   /* primary data, bars */
--lblue:  #93C5FD;   /* secondary, lighter */
--orange: #F59E0B;   /* contrast channel */
--green:  #10B981;   /* positive, growth */
--red:    #EF4444;   /* negative, warning */
--gray:   #6B7280;   /* labels, subtitles */
--dark:   #111827;   /* titles, strong text */
--grid:   #F3F4F6;   /* chart grid lines */
--bg:     #F9FAFB;   /* card backgrounds */

/* Font */
font-family: 'Inter', -apple-system, sans-serif;
/* Load via: <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet"> */
```

## Slide HTML template

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { width: 1400px; height: 800px; overflow: hidden; background: #fff;
       font-family: 'Inter', -apple-system, sans-serif; color: #111827; }
.slide { width: 1400px; height: 800px; padding: 52px 64px 44px;
         display: flex; flex-direction: column; }
.eyebrow { font-size: 13px; font-weight: 700; letter-spacing: .08em;
           color: #93C5FD; text-transform: uppercase; margin-bottom: 8px; }
.title   { font-size: 28px; font-weight: 800; letter-spacing: -.02em; }
.subtitle{ font-size: 14px; color: #6B7280; margin-top: 6px; }
.header  { margin-bottom: 32px; }
.footer  { margin-top: auto; padding-top: 16px; display: flex;
           justify-content: space-between; font-size: 10px; color: #D1D5DB; }
/* Cards */
.card { background: #F9FAFB; border-radius: 16px; padding: 24px 24px;
        border: 1px solid #F3F4F6; }
</style>
</head>
<body>
<div class="slide">
  <div class="header">
    <div class="eyebrow">SLIDE LABEL · context</div>
    <div class="title">Main Title</div>
    <div class="subtitle">One line of supporting context</div>
  </div>

  <!-- CONTENT HERE -->

  <div class="footer">
    <div>Source: ...</div>
    <div>Context · date</div>
  </div>
</div>
</body>
</html>
```

## Chart patterns (Chart.js)

### Bar comparison
```js
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Meta', 'ASA'],
    datasets: [{ data: [41, 38], backgroundColor: ['#2563EB', '#F59E0B'],
                 borderRadius: 8, borderSkipped: false }]
  },
  options: {
    animation: false,
    plugins: { legend: { display: false }, tooltip: { enabled: false } },
    scales: {
      x: { grid: { display: false }, border: { display: false } },
      y: { grid: { color: '#F3F4F6' }, border: { display: false },
           ticks: { callback: v => '$' + v } }
    }
  }
})
```

### Line trend
```js
datasets: [{
  data: values,
  borderColor: '#10B981', borderWidth: 3.5,
  pointBackgroundColor: '#10B981', pointBorderColor: '#fff',
  pointBorderWidth: 2.5, pointRadius: 8,
  tension: 0.3, fill: { target: 'origin', above: 'rgba(16,185,129,0.06)' }
}]
```

### Stacked bars
```js
datasets: [
  { label: 'Meta', data: metaVals, backgroundColor: '#2563EB', borderRadius: [4,4,0,0] },
  { label: 'ASA',  data: asaVals,  backgroundColor: '#F59E0B' }
],
options: { scales: { x: { stacked: true }, y: { stacked: true } } }
```

### Donut
```js
new Chart(ctx, {
  type: 'doughnut',
  data: { datasets: [{ data: vals, backgroundColor: ['#2563EB','#93C5FD','#F59E0B'],
                       borderWidth: 4, borderColor: '#fff' }] },
  options: { cutout: '62%', animation: false,
             plugins: { legend: { display: false }, tooltip: { enabled: false } } }
})
```

## Value labels (custom plugin)
```js
plugins: [{
  id: 'labels',
  afterDatasetsDraw(chart) {
    const { ctx } = chart
    chart.getDatasetMeta(0).data.forEach((bar, i) => {
      const v = chart.data.datasets[0].data[i]
      ctx.save()
      ctx.font = "700 16px 'Inter', sans-serif"
      ctx.fillStyle = '#111827'
      ctx.textAlign = 'center'
      ctx.fillText('$' + v, bar.x, bar.y - 10)
      ctx.restore()
    })
  }
}]
```

## KPI card pattern (no chart)
```html
<div style="display:flex; gap:20px; flex:1;">
  <div class="card" style="flex:1; display:flex; flex-direction:column; gap:8px;">
    <div style="font-size:11px;font-weight:700;color:#9CA3AF;text-transform:uppercase;letter-spacing:.06em">Metric name</div>
    <div style="font-size:48px;font-weight:900;color:#2563EB;letter-spacing:-.03em">$41</div>
    <div style="font-size:13px;color:#6B7280">Supporting note</div>
  </div>
</div>
```

## Multi-slide workflow

```bash
#!/bin/bash
OUT=~/Desktop/MyDeck-$(date +%Y-%m-%d)
mkdir -p $OUT
RENDER=~/.claude/skills/infographic/scripts/render.js

node $RENDER /tmp/slide01.html $OUT/01_title.png
node $RENDER /tmp/slide02.html $OUT/02_economics.png
# ... etc

open $OUT
```

## Text-heavy slides (exec summary, bullets)

Use flex column with colored left-border cards:
```html
<div style="display:flex; flex-direction:column; gap:12px; flex:1;">
  <div style="border-left:4px solid #EF4444; padding:16px 20px; background:#F9FAFB; border-radius:0 12px 12px 0;">
    <div style="font-size:14px;font-weight:700;color:#111827">Finding title</div>
    <div style="font-size:12px;color:#6B7280;margin-top:4px">Supporting detail</div>
  </div>
</div>
```
