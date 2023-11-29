const puppeteer = require('puppeteer');
const fs = require('fs');

const links = fs.readFileSync('./an-links').toString().trimEnd().split('\n');

const scrape = async (link) => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  await page.goto(link);
  
  const titleSelector = '.entry-title';
  await page.waitForSelector(titleSelector);

  const leadingParagraphSelector = 'p';
  await page.waitForSelector(leadingParagraphSelector);

  // extract data
  const [title, leadingParagraph] = await page.evaluate((titleSelector, leadingParagraphSelector) => {
    const title = document.querySelector(titleSelector).textContent;
    const leadingParagraph = document.querySelector(leadingParagraphSelector).textContent;

    return [title, leadingParagraph];
  }, titleSelector, leadingParagraphSelector);

  console.log(`${title};${leadingParagraph}`);

  await browser.close();
};

(async () => {
  for (let i = 0; i < links.length; i++) {
    await scrape(links[i]);
  }
})();
