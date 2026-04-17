#!/usr/bin/env node
/**
 * Batch convert HTML slides to PPTX
 */

const pptxgen = require('pptxgenjs');
const html2pptx = require('./html2pptx.js');
const path = require('path');
const fs = require('fs');

async function buildPPTX(htmlDir, outputFile) {
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_16x9';

  // Get all HTML files sorted by number
  const files = fs.readdirSync(htmlDir)
    .filter(f => f.endsWith('.html'))
    .sort((a, b) => {
      const numA = parseInt(a.match(/\d+/)[0]);
      const numB = parseInt(b.match(/\d+/)[0]);
      return numA - numB;
    });

  console.log(`Found ${files.length} slides to process...`);

  for (const file of files) {
    const htmlPath = path.join(htmlDir, file);
    console.log(`Processing: ${file}...`);

    try {
      await html2pptx(htmlPath, pres, { ignoreValidation: true });
    } catch (error) {
      console.error(`Error processing ${file}:`, error.message);
      // Continue with next file
    }
  }

  await pres.writeFile({ fileName: outputFile });
  console.log(`\nPPTX generated: ${outputFile}`);
}

// Run - support command line args or use temp_slides
const args = process.argv.slice(2);
const htmlDir = args[0] ? path.resolve(args[0]) : path.resolve(__dirname, '../temp_slides');
const outputFile = args[1] ? path.resolve(args[1]) : path.resolve(__dirname, '../temp_slides/openclaw-deploy-guide.pptx');

buildPPTX(htmlDir, outputFile).catch(console.error);
