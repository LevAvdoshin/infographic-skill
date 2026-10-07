---
name: infographic
description: Generate beautiful infographic slides as PNG from any text or data. Use whenever the user needs a visual slide, chart, or infographic - channel comparisons, KPI dashboards, trend lines, executive summaries, timelines, text-heavy slides. Output - 1400×800px PNG saved to ~/Desktop/<name>-<date>/. Stack - Claude writes HTML/CSS/Chart.js → Playwright screenshots → PNG. Completely free, no external API. Triggers on "сделай инфографику", "нарисуй слайд", "визуализируй", "make infographic", "build slides", "generate charts", "собери визуалы", "сделай слайд из этого".
---

# Infographic Skill

## Philosophy

One idea per slide. Big numbers. White space is free. Never cram — split into more slides.

The viewer should understand the point in **3 seconds** without reading the subtitle.

## Pipeline

```
Claude writes HTML → node scripts/render.js slide.html out.png → PNG opened
```

```bash
# Single slide
node ~/.claude/skills/infographic/scripts/render.js /tmp/slide.html ~/Desktop/out.png

# Batch deck (all HTML in a folder, alphabetically sorted)
node ~/.claude/skills/infographic/scripts/render-deck.js /tmp/my-deck/ ~/Desktop/MyDeck-2026-01-01/
```

Write HTML to `/tmp/` or `$CLAUDE_JOB_DIR/tmp/`. Render PNG to `~/Desktop/<Name>-<YYYY-MM-DD>/`. Then `open` the folder.

---

## Design System

```css
:root {
  --blue:   #2563EB;   /* primary data, bars */
  --lblue:  #93C5FD;   /* secondary, lighter */
  --orange: #F59E0B;   /* contrast channel */
  --green:  #10B981;   /* positive, growth */
  --red:    #EF4444;   /* negative, warning */
  --gray:   #6B7280;   /* labels, subtitles */
  --dark:   #111827;   /* titles, strong */
  --grid:   #F3F4F6;   /* chart grid */
  --bg:     #F9FAFB;   /* card backgrounds */
  --border: #E5E7EB;
}
```

| Use | Size | Weight |
|-----|------|--------|
| Eyebrow label | 12–13px | 700, uppercase, letter-spacing .07em |
| Slide title | 26–30px | 800, letter-spacing -.02em |
| Subtitle | 13–14px | 400, color `--gray` |
| Card heading | 14–15px | 700 |
| Body / notes | 12–13px | 400–500 |
| Big KPI number | 44–64px | 900, letter-spacing -.03em |
| Bar value labels | 14–18px | 700 |

Slide padding: `52px 64px 44px`. Card padding: `24px`. Card gap: `20px`. Border-radius: `16px` cards, `8px` bars.

---

## Base Slide Shell

Every slide. Never change `width/height`.

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { width:1400px; height:800px; overflow:hidden; background:#fff;
       font-family:'Inter',-apple-system,sans-serif; color:#111827; }
.slide { width:1400px; height:800px; padding:52px 64px 44px;
         display:flex; flex-direction:column; }
.eyebrow { font-size:13px; font-weight:700; letter-spacing:.07em;
           text-transform:uppercase; color:#93C5FD; margin-bottom:8px; }
.title   { font-size:28px; font-weight:800; letter-spacing:-.02em; line-height:1.2; }
.subtitle{ font-size:14px; color:#6B7280; margin-top:6px; }
.header  { margin-bottom:32px; }
.body    { flex:1; display:flex; gap:20px; }
.footer  { margin-top:auto; padding-top:14px; display:flex;
           justify-content:space-between; font-size:10px; color:#D1D5DB; }
.card    { background:#F9FAFB; border-radius:16px; padding:24px; border:1px solid #E5E7EB; }
</style>
</head>
<body>
<div class="slide">
  <div class="header">
    <div class="eyebrow">SECTION · context</div>
    <div class="title">Slide Title</div>
    <div class="subtitle">One supporting line</div>
  </div>
  <div class="body"><!-- content --></div>
  <div class="footer">
    <div>Source</div>
    <div>Context · date</div>
  </div>
</div>
</body>
</html>
```

---

## Slide Types

### 1. KPI Tiles — metrics side by side

Each tile: label → big number → CSS bar → channel name → insight note. Set bar heights as `%` of max value.

```html
<div class="body">
  <div class="card" style="flex:1;display:flex;flex-direction:column;position:relative;">
    <div style="position:absolute;top:16px;right:16px;font-size:11px;font-weight:700;
                padding:3px 10px;border-radius:20px;background:#D1FAE5;color:#065F46;">↓ -39%</div>
    <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;
                color:#9CA3AF;margin-bottom:16px;">Cost per Signup</div>
    <div style="display:flex;gap:12px;align-items:flex-end;flex:1;padding-bottom:8px;">
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:8px;">
        <div style="font-size:26px;font-weight:800;color:#2563EB;">$41</div>
        <div style="width:100%;display:flex;align-items:flex-end;height:120px;">
          <div style="width:100%;background:#2563EB;border-radius:8px 8px 0 0;height:100%;"></div>
        </div>
        <div style="font-size:11px;font-weight:600;color:#9CA3AF;text-transform:uppercase;">Meta</div>
      </div>
      <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:8px;">
        <div style="font-size:26px;font-weight:800;color:#F59E0B;">~$38</div>
        <div style="width:100%;display:flex;align-items:flex-end;height:120px;">
          <div style="width:100%;background:#F59E0B;border-radius:8px 8px 0 0;height:93%;"></div>
        </div>
        <div style="font-size:11px;font-weight:600;color:#9CA3AF;text-transform:uppercase;">ASA</div>
      </div>
    </div>
    <div style="border-top:1px solid #E5E7EB;padding-top:10px;font-size:12px;color:#6B7280;line-height:1.4;">
      Insight note
    </div>
  </div>
  <!-- repeat cards -->
</div>
```

---

### 2. Bar Chart (Chart.js)

```html
<div class="body"><div class="card" style="flex:1;display:flex;flex-direction:column;">
  <div style="font-weight:700;font-size:14px;margin-bottom:16px;">Chart Title</div>
  <div style="flex:1;position:relative;"><canvas id="c1"></canvas></div>
</div></div>
<script>
Chart.defaults.animation = false
new Chart(document.getElementById('c1'), {
  type: 'bar',
  data: {
    labels: ['8–14 Jun','15–21 Jun','22–28 Jun','29 Jun–5 Jul'],
    datasets: [{
      data: [38, 33, 26, 23],
      backgroundColor: ['#93C5FD','#93C5FD','#2563EB','#2563EB'],
      borderRadius: 8, borderSkipped: false,
    }]
  },
  plugins: [{
    id: 'labels',
    afterDatasetsDraw(chart) {
      const {ctx} = chart
      chart.getDatasetMeta(0).data.forEach((bar, i) => {
        const v = chart.data.datasets[0].data[i]
        ctx.save(); ctx.font = "700 16px 'Inter',sans-serif"
        ctx.fillStyle = '#111827'; ctx.textAlign = 'center'
        ctx.fillText('$'+v, bar.x, bar.y - 10); ctx.restore()
      })
    }
  }],
  options: {
    responsive: true, maintainAspectRatio: false,
    plugins: { legend:{display:false}, tooltip:{enabled:false} },
    scales: {
      x: { grid:{display:false}, border:{display:false},
           ticks:{font:{family:'Inter',size:12,weight:'500'},color:'#6B7280'} },
      y: { grid:{color:'#F3F4F6'}, border:{display:false},
           ticks:{font:{family:'Inter',size:11},color:'#9CA3AF',callback:v=>'$'+v} }
    },
    layout: { padding:{top:30} }
  }
})
</script>
```

**Grouped:** add second dataset, `barmode` is automatic. **Stacked:** add `stacked:true` to both axes.

---

### 3. Line Trend

```js
datasets: [{
  data: [54, 47, 37, 34],
  borderColor: '#2563EB', borderWidth: 3.5,
  pointBackgroundColor: '#2563EB', pointBorderColor: '#fff',
  pointBorderWidth: 2.5, pointRadius: 8, tension: 0.3,
  fill: { target:'origin', above:'rgba(37,99,235,0.06)' }
}]
```

**Dashed reference line plugin:**
```js
{
  id:'ref', afterDraw(chart) {
    const {ctx,chartArea,scales} = chart
    const y = scales.y.getPixelForValue(38)
    ctx.save(); ctx.strokeStyle='#F59E0B'; ctx.lineWidth=2; ctx.setLineDash([5,4])
    ctx.beginPath(); ctx.moveTo(chartArea.left,y); ctx.lineTo(chartArea.right,y); ctx.stroke()
    ctx.setLineDash([]); ctx.fillStyle='#F59E0B'
    ctx.font="600 11px 'Inter',sans-serif"; ctx.textAlign='right'
    ctx.fillText('ASA ~$38', chartArea.right-4, y-6); ctx.restore()
  }
}
```

**Fill between two lines (illusion vs reality):**
```js
// dataset 0 = reality, dataset 1 = illusion
// on dataset 0:
fill: { target: 1, above: 'rgba(239,68,68,0.10)' }
```

**Shaded zone (scale-up event):**
```js
// afterDraw plugin:
const x0 = scales.x.getPixelForValue(startIndex)
const x1 = scales.x.getPixelForValue(endIndex)
ctx.fillStyle = 'rgba(239,68,68,0.07)'
ctx.fillRect(x0, chartArea.top, x1-x0, chartArea.height)
```

---

### 4. Donut + Comparison Table

```html
<div class="body">
  <div style="width:340px;display:flex;flex-direction:column;align-items:center;justify-content:center;">
    <div style="position:relative;width:260px;height:260px;">
      <canvas id="donut"></canvas>
      <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;">
        <div style="font-size:38px;font-weight:900;">717</div>
        <div style="font-size:13px;color:#6B7280;margin-top:2px;">label</div>
      </div>
    </div>
    <!-- legend -->
    <div style="margin-top:20px;width:100%;display:flex;flex-direction:column;gap:8px;">
      <div style="display:flex;align-items:center;gap:10px;padding:10px 14px;background:#F9FAFB;border-radius:10px;">
        <div style="width:12px;height:12px;border-radius:3px;background:#2563EB;flex-shrink:0;"></div>
        <div style="font-size:12px;font-weight:500;flex:1;">Segment label</div>
        <div style="font-size:15px;font-weight:800;color:#2563EB;">236</div>
      </div>
    </div>
  </div>
  <div style="flex:1;display:flex;align-items:center;">
    <table style="width:100%;border-collapse:collapse;">
      <thead>
        <tr>
          <th style="text-align:left;font-size:11px;font-weight:700;color:#9CA3AF;text-transform:uppercase;letter-spacing:.06em;padding:0 16px 14px;border-bottom:2px solid #E5E7EB;">Metric</th>
          <th style="text-align:right;color:#6B7280;padding:0 16px 14px;border-bottom:2px solid #E5E7EB;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;">Column A</th>
          <th style="text-align:right;color:#2563EB;...">Column B</th>
        </tr>
      </thead>
      <tbody>
        <tr style="background:#EFF6FF;"> <!-- highlight row -->
          <td style="padding:13px 16px;font-weight:600;">Cost/Signup</td>
          <td style="padding:13px 16px;text-align:right;color:#9CA3AF;">$72</td>
          <td style="padding:13px 16px;text-align:right;font-weight:800;color:#2563EB;">$41</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
<script>
new Chart(document.getElementById('donut'), {
  type:'doughnut',
  data:{ datasets:[{ data:[236,171,310],
    backgroundColor:['#2563EB','#93C5FD','#F59E0B'],
    borderWidth:4, borderColor:'#fff', hoverOffset:0 }] },
  options:{ cutout:'62%', animation:false,
            plugins:{legend:{display:false},tooltip:{enabled:false}} }
})
</script>
```

---

### 5. Exec Summary / Text Findings

```html
<div class="body" style="flex-direction:column;gap:14px;">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;flex:1;">
    <!-- color = red/green/orange/blue/#374151 -->
    <div style="border:1px solid #E5E7EB;padding:18px 20px;background:#F9FAFB;border-radius:12px;">
      <div style="font-size:13px;font-weight:700;margin-bottom:4px;display:flex;align-items:center;gap:8px;"><span style="width:8px;height:8px;border-radius:50%;background:#EF4444;flex:none;"></span>Finding title</div>
      <div style="font-size:12px;color:#6B7280;line-height:1.5;">Detail. <strong>Key number</strong> in bold.</div>
    </div>
    <!-- repeat -->
  </div>
  <!-- bottom recommendation banner -->
  <div style="background:#EFF6FF;border-radius:12px;padding:16px 24px;display:flex;gap:16px;align-items:center;">
    <div style="font-size:13px;font-weight:700;color:#1D4ED8;white-space:nowrap;">РЕКОМЕНДАЦИЯ</div>
    <div style="font-size:13px;color:#1E40AF;">Recommendation text.</div>
  </div>
</div>
```

---

### 6. Title Slide

```html
<div class="slide" style="justify-content:center;position:relative;overflow:hidden;">
  <div style="position:absolute;top:-40px;right:20px;font-size:320px;font-weight:900;
              color:#F3F4F6;line-height:1;pointer-events:none;user-select:none;">01</div>
  <div style="position:relative;">
    <div style="font-size:16px;font-weight:700;color:#2563EB;letter-spacing:.04em;margin-bottom:16px;">
      COMPANY · PRODUCT
    </div>
    <div style="font-size:56px;font-weight:900;letter-spacing:-.03em;color:#111827;line-height:1.1;max-width:720px;">
      Deck Title Goes Here
    </div>
    <div style="font-size:18px;color:#6B7280;margin-top:16px;">Date range · plus context</div>
    <div style="margin-top:40px;">
      <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#9CA3AF;margin-bottom:8px;">Data sources</div>
      <div style="font-size:14px;color:#374151;">Source A · Source B · Source C</div>
    </div>
    <div style="margin-top:40px;font-size:13px;color:#9CA3AF;">Prepared by: Name · Date</div>
  </div>
</div>
```

---

### 7. Timeline

```html
<div class="body" style="flex-direction:column;justify-content:center;gap:0;">
  <div style="border-left:2px solid #E5E7EB;margin-left:32px;padding-left:32px;position:relative;padding-bottom:4px;">

    <!-- event dot + content -->
    <div style="position:relative;padding:18px 0;">
      <div style="position:absolute;left:-41px;top:24px;width:18px;height:18px;border-radius:50%;
                  background:#2563EB;border:3px solid #fff;box-shadow:0 0 0 2px #2563EB;"></div>
      <div style="display:flex;gap:20px;align-items:flex-start;">
        <div style="background:#EFF6FF;color:#1D4ED8;font-size:12px;font-weight:700;
                    padding:4px 14px;border-radius:20px;white-space:nowrap;flex-shrink:0;">30 июня</div>
        <div>
          <div style="font-size:15px;font-weight:700;margin-bottom:4px;">Event title</div>
          <div style="font-size:13px;color:#6B7280;line-height:1.5;">Event description</div>
        </div>
      </div>
    </div>

    <!-- red event -->
    <div style="position:relative;padding:18px 0;">
      <div style="position:absolute;left:-41px;top:24px;width:18px;height:18px;border-radius:50%;
                  background:#EF4444;border:3px solid #fff;box-shadow:0 0 0 2px #EF4444;"></div>
      <div style="display:flex;gap:20px;align-items:flex-start;">
        <div style="background:#FEF2F2;color:#B91C1C;font-size:12px;font-weight:700;
                    padding:4px 14px;border-radius:20px;white-space:nowrap;flex-shrink:0;">1–7 июля</div>
        <div>
          <div style="font-size:15px;font-weight:700;margin-bottom:4px;">Bad event</div>
          <div style="font-size:13px;color:#6B7280;line-height:1.5;">Details</div>
        </div>
      </div>
    </div>

  </div>
  <!-- callout -->
  <div style="margin-left:32px;margin-top:20px;background:#EFF6FF;border-radius:12px;padding:16px 24px;">
    <div style="font-size:13px;font-weight:700;color:#1D4ED8;margin-bottom:4px;">Вывод</div>
    <div style="font-size:13px;color:#1E40AF;line-height:1.5;">Callout text here.</div>
  </div>
</div>
```

---

## Quality Checklist

- [ ] `animation: false` on every Chart.js instance (Playwright screenshots mid-animation otherwise)
- [ ] `maintainAspectRatio: false` + parent div has explicit height for canvas
- [ ] `layout: { padding: { top: 30 } }` so value labels don't clip
- [ ] Inter font loaded from Google Fonts
- [ ] Footer on every slide: source + date
- [ ] `overflow:hidden` on body — nothing bleeds outside 1400×800
- [ ] One idea per slide — if cramped, split
