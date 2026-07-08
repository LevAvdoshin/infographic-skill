#!/usr/bin/env node
// Batch-render all HTML files in a folder to PNG
// Usage: node render-deck.js <folder-with-htmls/> <output-folder/>
// Output PNGs are named after the HTML files (e.g. 01_title.html → 01_title.png)
const { chromium } = require('playwright')
const fs = require('fs')
const path = require('path')

const [,, srcDir, outDir] = process.argv
if (!srcDir || !outDir) {
  console.error('Usage: node render-deck.js <src-folder> <out-folder>')
  process.exit(1)
}

fs.mkdirSync(outDir, { recursive: true })

const htmlFiles = fs.readdirSync(srcDir)
  .filter(f => f.endsWith('.html'))
  .sort()

if (!htmlFiles.length) {
  console.error('No .html files found in', srcDir)
  process.exit(1)
}

;(async () => {
  const browser = await chromium.launch()
  for (const f of htmlFiles) {
    const page = await browser.newPage()
    await page.setViewportSize({ width: 1400, height: 800 })
    const content = fs.readFileSync(path.join(srcDir, f), 'utf8')
    await page.setContent(content, { waitUntil: 'networkidle' })
    await page.waitForTimeout(600)
    const outPng = path.join(outDir, f.replace('.html', '.png'))
    await page.screenshot({ path: outPng })
    await page.close()
    console.log('✓', path.basename(outPng))
  }
  await browser.close()
  console.log(`\nDone — ${htmlFiles.length} slides → ${outDir}`)
})()
