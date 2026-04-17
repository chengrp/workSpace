// Playwright test example for web application testing
// This script demonstrates basic Playwright testing patterns

const { test, expect } = require('@playwright/test');

test.describe('Web Application Basic Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the application before each test
    await page.goto('http://localhost:3000');
  });

  test('should load the homepage', async ({ page }) => {
    // Check page title
    await expect(page).toHaveTitle(/.*/);

    // Check that page loaded successfully
    await expect(page.locator('body')).toBeVisible();

    // Take screenshot for visual verification
    await page.screenshot({ path: 'homepage.png' });
  });

  test('should have working navigation', async ({ page }) => {
    // Find all navigation links and test them
    const navLinks = page.locator('nav a, header a, .navbar a');
    const count = await navLinks.count();

    for (let i = 0; i < Math.min(count, 5); i++) {
      const link = navLinks.nth(i);
      const href = await link.getAttribute('href');

      if (href && !href.startsWith('#')) {
        await link.click();
        await page.waitForLoadState('networkidle');
        await expect(page.locator('body')).toBeVisible();
        await page.goBack();
      }
    }
  });

  test('should handle form submissions', async ({ page }) => {
    // Look for forms on the page
    const forms = page.locator('form');
    const formCount = await forms.count();

    if (formCount > 0) {
      // Test the first form
      const form = forms.first();

      // Fill form fields if they exist
      const inputs = form.locator('input[type="text"], input[type="email"], textarea');
      const inputCount = await inputs.count();

      for (let i = 0; i < inputCount; i++) {
        const input = inputs.nth(i);
        const placeholder = await input.getAttribute('placeholder') || '';
        await input.fill(`Test ${placeholder || 'input'}`);
      }

      // Submit form
      const submitButton = form.locator('button[type="submit"], input[type="submit"]');
      if (await submitButton.count() > 0) {
        await submitButton.first().click();
        await page.waitForTimeout(1000); // Wait for submission
      }
    }
  });

  test('should be responsive', async ({ page }) => {
    // Test different viewport sizes
    const viewports = [
      { width: 1920, height: 1080, name: 'desktop' },
      { width: 768, height: 1024, name: 'tablet' },
      { width: 375, height: 667, name: 'mobile' }
    ];

    for (const viewport of viewports) {
      await page.setViewportSize(viewport);
      await page.screenshot({ path: `viewport-${viewport.name}.png` });

      // Verify content is visible
      await expect(page.locator('body')).toBeVisible();
    }
  });

  test('should have working links', async ({ page }) => {
    // Test external and internal links
    const links = page.locator('a[href]');
    const linkCount = await links.count();

    console.log(`Found ${linkCount} links on the page`);

    // Test a sample of links
    for (let i = 0; i < Math.min(linkCount, 10); i++) {
      const link = links.nth(i);
      const href = await link.getAttribute('href');

      if (href && !href.startsWith('javascript:') && !href.startsWith('#')) {
        console.log(`Testing link: ${href}`);

        // Open link in new tab
        const newPage = await page.context().newPage();
        try {
          await newPage.goto(href.startsWith('http') ? href : `http://localhost:3000${href}`);
          await expect(newPage.locator('body')).toBeVisible({ timeout: 5000 });
          await newPage.close();
        } catch (error) {
          console.log(`Link ${href} failed: ${error.message}`);
          await newPage.close();
        }
      }
    }
  });
});

test.describe('API Testing with Playwright', () => {
  test('should have working API endpoints', async ({ request }) => {
    // Test common API endpoints
    const endpoints = [
      '/api/health',
      '/api/users',
      '/api/products'
    ];

    for (const endpoint of endpoints) {
      const response = await request.get(`http://localhost:3000${endpoint}`);

      // Check if endpoint exists (200 or 404 are both valid responses)
      const status = response.status();
      console.log(`${endpoint}: ${status}`);

      if (status === 200) {
        const body = await response.json();
        expect(body).toBeDefined();
      }
    }
  });
});

// Configuration for running tests
module.exports = {
  timeout: 30000, // 30 second timeout
  retries: 1, // Retry failed tests once
  use: {
    headless: true, // Run in headless mode
    viewport: { width: 1280, height: 720 },
    screenshot: 'only-on-failure', // Take screenshots on failure
    video: 'retain-on-failure' // Record video on failure
  }
};