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
  console.log(req.file)
  var temp_path = req.file.path;
  var originalnameSplit = req.file.originalname.split('.');
  var ext = '.' + originalnameSplit[originalnameSplit.length - 1];
  var target_path = req.file.path + ext;
  var _filename = req.file.filename + ext;
  var filePath = req.file.destination + _filename;
  console.log("Uploading: " + _filename);
  var cmd = `unzip ${filePath} -d ${req.file.destination + req.file.filename}`
  fs.rename(temp_path, target_path, function(err,data) {
    // cb(null, { file_path: filePath });
      exec(cmd, function (error, stdout, stderr) {
        console.log(error);
        console.log(stdout);
      })
  });
  res.send(_filename);
})

app.post('/file-upload-single', upload.single('file'), function (req, res) {
  console.log(req.file)
  var temp_path = req.file.path;
  var originalnameSplit = req.file.originalname.split('.');
  var ext = '.' + originalnameSplit[originalnameSplit.length - 1];
  var target_path = req.file.path + ext;
  var _filename = req.file.filename + ext;
  var filePath = req.file.destination + _filename;
  console.log(req.file.destination);
  console.log(req.file.filename);
  console.log("Uploading: " + _filename);
  var cmd = `unzip ${filePath} -d ${req.file.destination + req.file.filename}`
  fs.readFile(req.file.path, function (err, data) {
    fs.writeFile(req.file.destination + req.file.filename + ext, data, function (err) {
      if (err) {
        console.log(err)
      } else {
        res.send(_filename);
      }
    })
  })
})

app.get('/run', function (req, res) {
  var filename = req.query.filename.split('.')[0] + '/';
  var filepath = path.join(__dirname, '../public/upload/');
  var pythonpath = path.join(__dirname, './python/model.py');
  var cmd = `python3 ${pythonpath} ${filepath + filename}`
  exec(cmd, function (error, stdout, stderr) {
    if (error) {
      console.log(error);
      res.send('error');
    } else {
      console.log(stdout);
      res.send('ok');
    }
  })
})

app.get('/run-single', function (req, res) {
  var filename = req.query.filename.split('.')[0];
  var frame = req.query.fs;
  var ext = '.txt'
  var filepath = path.join(__dirname, '../public/upload/');
  var pythonpath = path.join(__dirname, './python-single/model_2.py');
  var cmd = `python3 ${pythonpath} ${filepath + filename + ext} ${frame}`;
  exec(cmd, function (error, stdout, stderr) {
    if (error) {
      console.log(error);
      res.send('error');
    } else {
      stdout = stdout.substring(0, stdout.length - 1)
      console.log('----------')
      console.log(stdout + '|');
      console.log('----------------')
      if (stdout == 'Normal') {
        res.send('normal');
      } else if (stdout == 'AFIB') {
        res.send('af')
      } else if (stdout == 'Suspected AFIB') {
        res.send('su_af')
      } else {
        res.send('noisy')
      }
    }
  })
})

app.get('/file-download', function (req, res) {
  var filename = req.query.filename.split('.')[0] + '-Statistics' + '.xls'
  source = path.join(__dirname, '../public/download/')
  res.download(source + filename)
})

var server = app.listen(3000, function () {
  var host = server.address().address;
  var port = server.address().port;

  console.log('Example app listening at http://%s:%s', host, port);
});
