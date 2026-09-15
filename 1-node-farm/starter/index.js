const fs = require('fs')
const http = require('http')
const url = require('url')
const slugify = require('slugify')

const replaceTemplate = require('./modules/replaceTemplate')

// FILES
// Blocking, synchronous way
// const textIn = fs.readFileSync('./txt/input.txt', 'utf-8')
// console.log(textIn)

// const textOut =
//   'This is what we know about the avocado: ' +
//   textIn +
//   '.\nCreated on ' +
//   Date.now()
// fs.writeFileSync('./txt/output.txt', textOut)
// console.log('File written!')

// Reading a file asynchronously with a callback
// fs.readFile('./start.txt', 'utf-8', (err, data) => {
//   if (err) console.log('ERROR!     💥')
//   console.log(data)
// })

// console.log('This prints BEFORE the file content!')

// Non-blocking, asynchronous way
// fs.readFile('./txt/start.txt', 'utf-8', (err, data1) => {
//   if (err) return console.log('ERROR!     💥')
//   console.log(data1)
//   fs.readFile(`./txt/${data1}.txt`, 'utf-8', (err, data2) => {
//     console.log(data2)
//     fs.readFile(`./txt/append.txt`, 'utf-8', (err, data3) => {
//       console.log(data3)

//       fs.writeFile('./txt/final.txt', `${data2}\n${data3}`, 'utf-8', (err) => {
//         console.log('Your file has been written!     ✅')
//       })
//     })
//   })
// })

const tempOverview = fs.readFileSync(
  `${__dirname}/templates/template-overview.html`,
  'utf-8',
)
//const tempCard = fs.readFileSync(`${__dirname}/templates/template-card.html`, 'utf-8')
const tempProduct = fs.readFileSync(
  `${__dirname}/templates/template-product.html`,
  'utf-8',
)
const tempCard = fs.readFileSync(
  `${__dirname}/templates/template-card.html`,
  'utf-8',
)

const data = fs.readFileSync(`${__dirname}/dev-data/data.json`, 'utf-8')
const dataObj = JSON.parse(data)

const server = http.createServer((req, res) => {
  const host = req.headers.host || '127.0.0.1:8000'
  const baseUrl = `http://${host}`
  const myUrl = new URL(req.url, baseUrl)
  const pathname = myUrl.pathname
  const query = Object.fromEntries(myUrl.searchParams)

  if (pathname === '/' || pathname === '/overview') {
    res.writeHead(200, {
      'Content-type': 'text/html',
    })
    const cardsHtml = dataObj
      .map((el) => replaceTemplate(tempCard, el))
      .join('')
    const tempOverviewWithCards = tempOverview.replace(
      '{%PRODUCT_CARDS%}',
      cardsHtml,
    )
    //console.log('check object dataObj: ', dataObj)
    //res.end('<h1>Overview</h1>')
    res.end(tempOverviewWithCards)
  } else if (pathname === '/product') {
    res.writeHead(200, {
      'Content-type': 'text/html',
    })
    const product = dataObj[query.id]
    const productHtml = replaceTemplate(tempProduct, product)
    res.end(productHtml)
  } else if (pathname === '/api') {
    res.writeHead(200, {
      'Content-type': 'application/json',
    })
    res.end(JSON.stringify(dataObj))
  } else {
    res.writeHead(404, {
      'Content-type': 'text/html',
      'my-own-header': 'hello-world',
    })
    res.end('<h1>Page not found!</h1>')
  }
})

server.listen(8000, '127.0.0.1', () => {
  const url = `http://127.0.0.1:8000`
  const clickableUrl = `\x1b[34m${url}\x1b[0m` // ANSI escape code for blue color
  console.log(`Listening for requests on port 8000 at ${clickableUrl}`)
})
