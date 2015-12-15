// Copyright 2014 letv Inc. All Rights Reserved.
// Author: guoxiaohe@letv.com
var system = require('system');
if (system.args.length < 2) {
  //console.log('Usage: get_html.js <some URL> <some USER_AGENT>');
  system.stderr.writeLine('Usage: get_html.js <some URL> <some USER_AGENT>')
  phantom.exit(1);
}
url = system.args[1]
var page = require('webpage').create()
if (system.args.length == 3) {
  page.settings.userAgent = system.args[2]
} else {
    //console.log('The default user agent is ' + page.settings.userAgent);
    system.stderr.writeLine('The default user agent is ' + page.settings.userAgent);
}

var timeout = 1000 * 60 * 4;

setTimeout(function() {
   system.stderr.writeLine('Timeout for url:' + url);
   phantom.exit(1);
}, timeout);

page.onConsoleMessage = function (msg) {
  console.log('Page title is ' + msg);
};

page.open(url, function () {
  // Checks for bottom div and scrolls down from time to time
  window.setInterval(function() {
    var has_loading_more = page.evaluate(function() {
      var loadingElement = window.document.getElementById('loading');
      if (loadingElement.className == 'sq-loading hidden')
        return false;
      else
        return true;
    });
    if(has_loading_more) { // Didn't find
      page.evaluate(function() {
      window.document.body.scrollTop = document.body.scrollHeight;
      });
      console.log('set window.document.body.scrollTop = document.body.scrollHeight');
    } else { // Found
      var pc = page.evaluate(function() {
        return document.documentElement.innerHTML;
      });
      system.stdout.writeLine(pc);
      phantom.exit();
    }
  }, 100); // Number of milliseconds to wait between scrolls
});

