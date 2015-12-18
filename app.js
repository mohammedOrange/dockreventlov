#!/usr/bin/env node

var youtubedl = require('youtube-dl');
var devnull = require('dev-null');

var url = 'https://www.youtube.com/watch?v=aqz-KE-bpKQ';

var startTime = new Date();
var video = youtubedl(url, ['-o -', '-f best']);

video.on('info', function(info) {
   size = info.size;
   
   video.pipe(devnull());

});

var pos = 0;
video.on('data', function(data) {
   pos += data.length;

   if (size) {
      var percent = (pos/size * 100).toFixed(2);
      process.stdout.cursorTo(0);
      process.stdout.clearLine(1);
      process.stdout.write(percent + '%');
   }
});

video.on('end', function() {
   console.log('Streaming finished');
   var endTime = new Date();

   var delay = endTime - startTime;
   console.log('delay ' + delay.format("%H:%M:%S"));
});
