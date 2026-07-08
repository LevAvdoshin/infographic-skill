#!/usr/bin/env node
// Renders an HTML slide → PNG via Playwright (Chromium)
// Usage: node render.js <slide.html> <output.png>
// Viewport: 1400×800 (16:9 slide). scale=1 (HTML already sized for pixel-perfect output)

const { chromium } = require('playwright')
const fs = require('fs')
const path = require('path')

const [,, htmlFile, outPng] = process.argv
if (!htmlFile || !outPng) {
  console.error('Usage: node render.js <slide.html> <output.png>')
  process.exit(1)
}

;(async () => {
  const browser = await chromium.launch()
  const page = await browser.newPage()
  await page.setViewportSize({ width: 1400, height: 800 })

  const content = fs.readFileSync(path.resolve(htmlFile), 'utf8')
  await page.setContent(content, { waitUntil: 'networkidle' })
  await page.waitForTimeout(600) // let Chart.js and fonts settle

  await page.screenshot({ path: outPng })
  await browser.close()

  console.log('✓', path.basename(outPng))
})()
