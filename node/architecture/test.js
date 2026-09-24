const assert = require("assert");
const { json } = require("stream/consumers");
describe("Testing JSON reader", () => {
  it("should read JSON file correctly", () => {
    const jsonReader = require("./jsonReader");
    assert.equal(typeof jsonReader, "object");
    assert.equal(typeof jsonReader.readJSON, "function");
    done();
  });
});
