import { expect, test } from '@jupyterlab/galata';

test('ActivateCellButton should appear and function correctly', async ({
  page
}) => {
  console.log('Starting test...');

  // Create a new notebook
  console.log('Creating new notebook...');
  await page.menu.clickMenuItem('File>New Notebook');

  // Wait for the notebook to be ready
  console.log('Waiting for notebook to be ready...');
  await page.waitForSelector('.jp-Notebook', { timeout: 30000 });

  // Add a markdown cell
  console.log('Adding markdown cell...');
  await page.keyboard.press('b');
  await page.keyboard.type('# Markdown Cell');

  // Add a code cell
  console.log('Adding code cell...');
  await page.keyboard.press('b');
  await page.keyboard.type('print("hello")');

  // Focus on the markdown cell
  console.log('Focusing on markdown cell...');
  await page.click('.jp-MarkdownCell');

  // Wait for and verify the button appears with correct text
  console.log('Waiting for markdown button...');
  const markdownButton = await page.waitForSelector(
    '.jv-cell-ai-button-container',
    { timeout: 10000 }
  );
  console.log('Markdown button found, checking text...');
  const markdownText = await markdownButton.textContent();
  console.log('Markdown button text:', markdownText);
  expect(markdownText).toContain('Generate code');

  // Focus on the code cell
  console.log('Focusing on code cell...');
  await page.click('.jp-CodeCell');

  // Wait for and verify the button appears with correct text
  console.log('Waiting for code button...');
  const codeButton = await page.waitForSelector(
    '.jv-cell-ai-button-container',
    { timeout: 10000 }
  );
  console.log('Code button found, checking text...');
  const codeText = await codeButton.textContent();
  console.log('Code button text:', codeText);
  expect(codeText).toContain('Change code');

  // Verify only one button exists at a time
  console.log('Verifying button count...');
  const buttons = await page.$$('.jv-cell-ai-button-container');
  console.log('Button count:', buttons.length);
  expect(buttons.length).toBe(1);
});
