var http = require("http");
var book = require("./book");
book.read();
var server = http.createServer(function (req, res) {
  if (req.url === "/") {
    res.write("Hello World");

    res.end();
  }
});
server.listen(3000, "127.0.0.1", function () {
  console.log("Listening to request on port 3000");
});
