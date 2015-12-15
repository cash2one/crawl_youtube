// Copyright 2014 letv Inc. All Rights Reserved.
// Author: guoxiaohe@letv.com

var page = require('webpage').create()
var system = require('system');

console.log(system.args.length)
if (system.args.length < 2) {
  //console.log('Usage: get_html.js <some URL> <some USER_AGENT>');
  system.stderr.writeLine('Usage: get_html.js <some URL> <some USER_AGENT>')
  phantom.exit(1);
}
url = system.args[1]
if (system.args.length == 3) {
  page.settings.userAgent = system.args[2]
} else {
    //console.log('The default user agent is ' + page.settings.userAgent);
    system.stderr.writeLine('The default user agent is ' + page.settings.userAgent);
}
//console.log('The default user agent is ' + page.settings.userAgent);

var timeout = 1000 * 15;

setTimeout(function() {
   system.stderr.writeLine('Timeout for url:' + url);
   phantom.exit(1);
}, timeout);


var first_load = 0;

page.open(url, function(status) {
  window.setInterval(function() {
    if(first_load < 1){
      page.evaluate(function() {
        window.document.body.scrollTop = document.body.scrollHeight;
      });
      first_load += 1;
    }
    else if (status !== 'success') {
      system.stderr.writeLine('Unable to access network');
      phantom.exit(1);
    } else {
      var ua = page.evaluate(function() {
        return document.documentElement.innerHTML;
      });
      var ru = page.evaluate(function() {
        return 'redirected url: ' + window.location.href + '\n';
      });
      system.stdout.writeLine(ua)
      system.stderr.writeLine(ru)
      phantom.exit(0);
    }
  }, 1000); // Number of milliseconds to wait between scrolls

});
