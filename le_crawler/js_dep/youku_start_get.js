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

var timeout = 1000 * 160;

setTimeout(function() {
   system.stderr.writeLine('Timeout for url:' + url);
   var pc = page.evaluate(function() {
     return document.documentElement.innerHTML;
   });
   system.stdout.writeLine(pc);
   phantom.exit();
}, timeout);

page.open(url, function () {
  // Checks for bottom div and scrolls down from time to time
  window.setInterval(function() {
    var need_scroll = page.evaluate(function() {
      var workscoll = $("div._lazyload:visible");
      var table = workscoll.find("table");
      var lastTr = table.find("tr:last");  
      if(lastTr[0]){
        if("f" == lastTr.attr("needRequest")) {
          return false;
        }
      }
      return true;
    });
    if(need_scroll) { // Didn't find
      page.evaluate(function() {
      window.document.body.scrollTop = document.body.scrollHeight;
      });
    } else { // Found
      var pc = page.evaluate(function() {
        return document.documentElement.innerHTML;
      });
      system.stdout.writeLine(pc);
      phantom.exit();
    }
  }, 100); // Number of milliseconds to wait between scrolls
});

