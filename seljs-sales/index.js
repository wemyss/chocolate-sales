require('chromedriver');
const fetch = require('node-fetch');
const selenium = require('selenium-webdriver');
const data = require('../items.json');

const driver = new selenium.Builder()
    .withCapabilities(selenium.Capabilities.chrome())
    .build();

const delay = ms => new Promise(res => setTimeout(res, ms));

async function getPriceColes(url) {
  driver.get(url);
  let text = 'Loading';
  while (text.startsWith('Loading')) {
    await delay(1000);
    const element = driver.findElement(selenium.By.tagName('body'));
    text = await element.getText();
  }

  const res = JSON.parse(text);
  const price = res.catalogEntryView[0].p1.o;
  return parseFloat(price);
}


async function getPriceWoolworths(url) {
  driver.get(url)
  return fetch(url)
    .then(data => data.json())
    .then(data => data.Product.Price)
    .catch(err => console.log(err));
}


async function testColes() {
  const { coles_url_prefix, woolworths_url_prefix } = data;
  const prices = [];
  for (const item of data.items) {
    const { name, coles_url, woolworths_url } = item;
    const itemPriceDetails = {
      name,
      coles: coles_url && await getPriceColes(coles_url_prefix + coles_url),
      woolworths: woolworths_url && await getPriceWoolworths(woolworths_url_prefix + woolworths_url),
    };
    prices.push(itemPriceDetails);
  }
  console.log(prices)
  driver.quit();
}
testColes()
