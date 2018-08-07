var express = require('express');
var app = express();

var path = require('path');
var multer = require('multer');
var fs = require('fs');
var upload = multer({ dest: path.join(__dirname, '../public/upload/') });

var exec = require('child_process').exec;

app.get('/', function (req, res) {
  res.send('Hello World!');
});

app.post('/', function (req, res) {
  res.send('Hi!');
})

app.post('/file-upload', upload.single('file'), function (req, res) {
  // console.log(req.file)
  var temp_path = req.file.path;
  var originalnameSplit = req.file.originalname.split('.');
  var ext = '.' + originalnameSplit[originalnameSplit.length - 1];
  var target_path = req.file.path + ext;
  var _filename = req.file.filename + ext;
  var filePath = '/upload/' + _filename;
  console.log("Uploading: " + _filename);
  var cmd = `python ./python/test.py ${_filename}`
  fs.rename(temp_path, target_path, function(err,data) {
    // cb(null, { file_path: filePath });
      exec(cmd, function (error, stdout, stderr) {
        console.log(error);
        console.log(stdout);
      })
  });
})

app.get('/file-download', function (req, res) {
  var filename = req.query.filename
  source = path.join(__dirname, '../public/download/')
  res.download(source + filename)
})

var server = app.listen(3000, function () {
  var host = server.address().address;
  var port = server.address().port;

  console.log('Example app listening at http://%s:%s', host, port);
});