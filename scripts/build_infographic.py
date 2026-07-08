#!/usr/bin/env python3
"""
Template: channel-economics infographic deck (4 slides).
Copy this file, replace DATA section, run with ~/.venvs/analysis/bin/python.
"""

import os, datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── CONFIG ──────────────────────────────────────────────────────────────────
NAME   = 'MyTruv-ASA'
CONTEXT = 'MyTruv iOS · ASA/Meta audit'
OUT    = os.path.expanduser(f'~/Desktop/{NAME}-Infographic-{datetime.date.today()}')
os.makedirs(OUT, exist_ok=True)

# ── PALETTE ─────────────────────────────────────────────────────────────────
BLUE   = '#2563EB'
LBLUE  = '#93C5FD'
ORANGE = '#F59E0B'
GREEN  = '#10B981'
RED    = '#EF4444'
GRAY   = '#6B7280'
DARK   = '#111827'
GRID   = '#F3F4F6'
FONT   = 'Inter, -apple-system, sans-serif'

LAYOUT = dict(
    paper_bgcolor='white', plot_bgcolor='white',
    font=dict(family=FONT, color=DARK),
    margin=dict(l=70, r=70, t=130, b=80),
    showlegend=True,
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=12), x=0.01, y=0.99),
    xaxis=dict(gridcolor=GRID, linecolor='#E5E7EB', tickfont=dict(size=12)),
    yaxis=dict(gridcolor=GRID, linecolor='#E5E7EB', tickfont=dict(size=12), zeroline=False),
)


def header(fig, title, subtitle=''):
    fig.add_annotation(text=f'<b>{title}</b>',
        xref='paper', yref='paper', x=0, y=1.16, xanchor='left',
        font=dict(size=24, color=DARK, family=FONT), showarrow=False)
    if subtitle:
        fig.add_annotation(text=subtitle,
            xref='paper', yref='paper', x=0, y=1.08, xanchor='left',
            font=dict(size=13, color=GRAY, family=FONT), showarrow=False)
    fig.add_annotation(text=f'{CONTEXT} · {datetime.date.today()}',
        xref='paper', yref='paper', x=1, y=-0.12, xanchor='right',
        font=dict(size=9, color='#C0C4CC', family=FONT), showarrow=False)


def save(fig, slug, w=1400, h=800):
    path = f'{OUT}/{slug}.png'
    fig.write_image(path, width=w, height=h, scale=2)
    print(f'  ✓ {slug}.png')


# ── DATA (replace for your deck) ────────────────────────────────────────────
# Slide 1: Channel economics comparison (4 metrics)
metrics      = ['CPI / CPD', 'Signup CR %', 'Cost per Signup', 'Cost per Install']
meta_vals    = [29, 70, 41, 29]   # adjust
asa_vals     = [12, 32, 38, 12]
meta_labels  = ['$29', '70%', '$41', '$29']
asa_labels   = ['$12', '32%', '$38', '$12']

# Slide 2: Meta weekly trend (4 weeks)
weeks        = ['8–14 июн', '15–21 июн', '22–28 июн', '29 июн–5 июл']
meta_cpi     = [38, 33, 26, 23]
meta_cps     = [54, 47, 37, 34]
asa_cps_line = 38  # flat reference

# Slide 3: Install breakdown (pie)
pie_labels   = ['Meta атрибуцировано', 'Meta неатрибуц.', 'ASA downloads']
pie_vals     = [236, 171, 310]
pie_colors   = [BLUE, LBLUE, ORANGE]

# Slide 4: Signup CR trend
cr_weeks     = ['27 апр', '4 май', '11 май', '18 май', '25 май',
                '1 июн', '8 июн', '15 июн', '22 июн', '29 июн', '6 июл']
cr_vals      = [None, 70, 65, 42, 30, None, 75, 70, 68, 45, 35]
cr_vals      = [v for v in cr_vals if v is not None]
cr_weeks_f   = [w for w, v in zip(cr_weeks, [None, 70, 65, 42, 30, None, 75, 70, 68, 45, 35]) if v is not None]


# ── SLIDE 1: Channel economics ───────────────────────────────────────────────
print('Building slide 1 — channel economics...')
fig = make_subplots(rows=1, cols=4,
    subplot_titles=['<b>CPI / CPD</b>', '<b>Signup CR</b>', '<b>Cost per Signup</b>', '<b>Cost per Install</b>'],
    horizontal_spacing=0.08)

for col, (mv, av, ml, al) in enumerate(zip(meta_vals, asa_vals, meta_labels, asa_labels), 1):
    fig.add_trace(go.Bar(
        x=['Meta', 'ASA'], y=[mv, av],
        marker_color=[BLUE, ORANGE],
        text=[ml, al], textposition='outside',
        textfont=dict(size=18, color=DARK, family=FONT),
        width=0.5,
        showlegend=(col == 1),
        name='Meta' if col == 1 else 'ASA',
    ), row=1, col=col)

fig.update_layout(**LAYOUT)
for i in range(1, 5):
    fig.update_yaxes(gridcolor=GRID, zeroline=False, showgrid=True, row=1, col=i)
    fig.update_xaxes(gridcolor='rgba(0,0,0,0)', row=1, col=i)

fig.update_annotations(font=dict(size=15, color=DARK))
header(fig, 'Экономика каналов: по цене signup — сопоставимо',
       'Разница в механике: ASA = дешёвая установка, Meta = высокая конверсия')
save(fig, '01_channel_economics')


# ── SLIDE 2: Meta weekly progress ────────────────────────────────────────────
print('Building slide 2 — Meta weekly progress...')
x = list(range(4))
fig = make_subplots(rows=1, cols=2, subplot_titles=['<b>CPI (реальный)</b>', '<b>Cost per Signup</b>'],
    horizontal_spacing=0.12)

fig.add_trace(go.Bar(x=weeks, y=meta_cpi, marker_color=BLUE, width=0.5,
    text=[f'${v}' for v in meta_cpi], textposition='outside',
    textfont=dict(size=15, color=BLUE, family=FONT),
    name='Meta CPI', showlegend=True), row=1, col=1)

fig.add_trace(go.Bar(x=weeks, y=meta_cps, marker_color=BLUE, width=0.5,
    text=[f'${v}' for v in meta_cps], textposition='outside',
    textfont=dict(size=15, color=BLUE, family=FONT),
    name='Meta Cost/Signup', showlegend=True), row=1, col=2)

# ASA reference line
fig.add_hline(y=asa_cps_line, line_dash='dash', line_color=ORANGE, line_width=2,
    annotation_text=f'ASA ~${asa_cps_line}', annotation_position='right',
    annotation_font=dict(color=ORANGE, size=12), row=1, col=2)

# Trend arrows / delta
fig.add_annotation(text='<b>-39%</b>', x=weeks[-1], y=meta_cpi[-1]+6,
    font=dict(size=14, color=GREEN), showarrow=False, row=1, col=1, xref='x1', yref='y1')
fig.add_annotation(text='<b>-36%</b>', x=weeks[-1], y=meta_cps[-1]+6,
    font=dict(size=14, color=GREEN), showarrow=False, row=1, col=2, xref='x2', yref='y2')

fig.update_layout(**LAYOUT)
header(fig, 'Meta прогрессирует: CPI −39%, Cost/Signup −36% за месяц',
       'Свой канал, полный контроль: CR стабильно 70%, цена падает 4 недели подряд')
save(fig, '02_meta_weekly_progress')


# ── SLIDE 3: Attribution breakdown ───────────────────────────────────────────
print('Building slide 3 — attribution breakdown...')
fig = make_subplots(rows=1, cols=2,
    specs=[[{'type': 'pie'}, {'type': 'xy'}]],
    column_widths=[0.45, 0.55])

fig.add_trace(go.Pie(
    labels=pie_labels, values=pie_vals, hole=0.42,
    marker=dict(colors=pie_colors, line=dict(color='white', width=3)),
    textfont=dict(size=13, family=FONT),
    textinfo='label+percent',
    insidetextorientation='radial',
    showlegend=False,
), row=1, col=1)

# Table on right
rows_data = [
    ['',              'Атрибуц.',  'Реальная', 'ASA'],
    ['Installs',      '236',       '407',      '310'],
    ['Spend',         '$11,903',   '$11,903',  '$3,775'],
    ['CPI',           '$50',       '$29',      '$12'],
    ['Signups',       '165',       '~289',     '~98'],
    ['Signup CR',     '70%',       '70%',      '~32%'],
    ['Cost/Signup',   '$72',       '$41',      '~$38'],
]
col_colors = [GRAY, GRAY, BLUE, ORANGE]
for ri, row in enumerate(rows_data):
    for ci, cell in enumerate(row):
        is_header = ri == 0
        is_key_row = ri in (3, 6)
        fig.add_annotation(
            text=f'<b>{cell}</b>' if (is_header or ci == 0 or is_key_row) else cell,
            xref='x2', yref='paper',
            x=0.04 + ci * 0.22, y=0.92 - ri * 0.13,
            xanchor='left',
            font=dict(size=12, color=col_colors[ci] if ci > 0 and ri > 0 else DARK,
                      family=FONT),
            showarrow=False,
        )

fig.update_layout(**LAYOUT)
fig.update_xaxes(visible=False, row=1, col=2)
fig.update_yaxes(visible=False, row=1, col=2)
header(fig, 'Реатрибуция: из чего состоят 717 установок',
       'Неатрибуцированные установки минус ASA = недосчитанная Meta (171)')
save(fig, '03_attribution_breakdown')


# ── SLIDE 4: CR longterm ─────────────────────────────────────────────────────
print('Building slide 4 — CR longterm...')
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=cr_weeks_f, y=cr_vals, mode='lines+markers+text',
    line=dict(color=GREEN, width=3.5),
    marker=dict(size=10, color=GREEN, line=dict(color='white', width=2)),
    text=[f'{v}%' for v in cr_vals], textposition='top center',
    textfont=dict(size=11, color=GREEN, family=FONT),
    name='Signup CR',
))

# Shade meta-scale zone
fig.add_vrect(x0='11 май', x1='25 май', fillcolor=RED, opacity=0.08,
    annotation_text='Meta x4<br>CR 65→30%<br>(ASA нет)',
    annotation_position='top left',
    annotation_font=dict(color=RED, size=11))
fig.add_vrect(x0='29 июн', x1='6 июл', fillcolor=ORANGE, opacity=0.08,
    annotation_text='ASA x4<br>CR 68→35%',
    annotation_position='top right',
    annotation_font=dict(color=ORANGE, size=11))

fig.update_layout(**LAYOUT,
    yaxis=dict(range=[0, 90], ticksuffix='%', gridcolor=GRID, zeroline=False),
    showlegend=False)
header(fig, 'Signup CR с мая: масштаб роняет CR на любом канале',
       'Май: Meta одна, ASA не существовало — тот же провал. Проблема — темп, не канал.')
save(fig, '04_cr_longterm')


print(f'\n✅ Done — {OUT}')
os.system(f'open "{OUT}"')
