var path = require('path');
var apidoc = require('apidoc');

var baseDir = path.resolve(`..${path.sep}`);

// Edit to import more apps
var apiPath = ["Common", "Login", "Payment", "Project", "Upload", "User", "Share", "Statistics"];

var doc = apidoc.createDoc({
    src: apiPath.map((item) => path.join(baseDir, item)),
    dest: path.join(baseDir, 'DOC', 'apidoc'),
    config: path.join(baseDir,'Apidoc', 'apidoc.json'),
    silent: true
});

if (typeof doc !== 'boolean') {
  // Documentation was generated!
  // console.log(doc.data) // the parsed api documentation object
  console.log(doc.project) // the project information
}
