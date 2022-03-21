var path = require('path');
var apidoc = require('apidoc');

var baseDir = path.resolve(`.${path.sep}`);
console.log(baseDir)

var doc = apidoc.createDoc({
    src: baseDir,
    dest: path.join(baseDir, 'DOC', 'apidoc'),
    config: path.join(baseDir,'Apidoc', 'apidoc.json')
});

if (typeof doc !== 'boolean') {
  // Documentation was generated!
  // console.log(doc.data) // the parsed api documentation object
  console.log(doc.project) // the project information
}
