import { test, Browser, Page } from '@playwright/test';
import { chromium } from 'playwright';
import * as fs from 'fs';
import * as path from 'path';

test('basic test', async ({}) => {
    const browser: Browser = await chromium.launch({ headless: false, channel: 'chrome' });
    const page: Page = await browser.newPage();
    await page.goto('https://assessmentonline.naac.gov.in/public/index.php/hei_dashboard');
    
    
    await page.waitForSelector('select[name="state"]');
    await page.selectOption('select[name="state"]', '99');
    await page.click('button[id="showbtn"]');
    await page.locator('//*[@id="details_table_length"]/label/select').selectOption('100');
    await page.getByRole('link' , {name: 'view'}).nth(0).click()
    
    const [download] = await Promise.all([
      page.waitForEvent('download'),
      page.click('div[class="col-md-3"] a[href*= "https://assessmentonline.naac.gov.in/public/index.php/ssr_report/"]'),
    ]);
    const suggestedName = await download.suggestedFilename();
    download.saveAs(suggestedName);
    await page.waitForSelector('div[id="modal_box"]');
    await page.click('button[class="close"]');
    
   
})