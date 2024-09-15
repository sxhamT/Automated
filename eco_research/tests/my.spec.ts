import {test, expect, Browser, Page, Locator, FrameLocator} from '@playwright/test'
import { doesNotThrow, strict } from 'assert';
import * as fs from 'fs';
import * as path from 'path';
import { time } from 'console';
import { webkit, firefox, chromium } from 'playwright'
import { TIMEOUT } from 'dns';


test('basic test', async ({ }) => {
     
    const outputPath = path.join(__dirname, 'bruh.pdf' );
    const browser:Browser = await chromium.launch({ headless: false, channel: 'chrome'})
    const context = await browser.newContext()
    const page:Page = await context.newPage()
    

      // Enable request interception
    await context.route('**/*', async (route) => {
    const response = await route.fetch();
    const headers = response.headers();
    const contentType = headers['content-type'];
    const contentDisposition = headers['content-disposition'];

    if (contentType?.includes('application/pdf') || contentDisposition?.includes('filename=')) {
         const buffer = await response.body();
         route.continue()
         fs.writeFileSync(outputPath, buffer);
         console.log(`PDF downloaded to: ${outputPath}`);
         
        } else {
      route.continue();
        }
     });



    await page.goto('https://assessmentonline.naac.gov.in/public/index.php/hei_dashboard' , {waitUntil: 'networkidle'})
    
    
    await page.waitForSelector('select[name="state"]')
    await page.selectOption('select[name="state"]', '99')
    await page.click('button[id="showbtn"]')
    await page.locator('//*[@id="details_table_length"]/label/select').selectOption('100')
    
    // change i=1 to 100 when ready 
    for (let i = 0; i <=2; i++) {
        if (i == null)
        break 
        
        if(i < 2){
            if (page.getByRole('link' , {name: 'view'}).nth(i) != null) 
                {   
                    await page.getByRole('link' , {name: 'view'}).nth(i).click()
                    await page.waitForSelector('div[id="modal_box"]')
                    const pagePromise = context.waitForEvent('page')
                    await page.click('div[class="col-md-3"] a[href*= "https://assessmentonline.naac.gov.in/public/index.php/ssr_report/"]')
                    const newPage = await pagePromise;
                    await newPage.waitForLoadState()
                    console.log(`New tab opened with URL: ${newPage.url()}`);
                    await newPage.bringToFront();
                    await page.waitForTimeout(5000)
                    
                    await page.waitForSelector('div[id="modal_box"]')
                    await page.click('button[class="close"]')
                    continue
                }
            else
                break
                    

        }
        
        if (i == 2) 
            {
               
                await page.getByRole('link' , {name: 'Next'}).click() 
                
                i=-1
                continue
            }
    }
  
})  

