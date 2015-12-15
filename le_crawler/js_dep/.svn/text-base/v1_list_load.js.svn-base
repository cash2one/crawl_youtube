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

page.onConsoleMessage = function (msg) {
  console.log('Page title is ' + msg);
};

var first_load = 0;

page.open(url, function () {
  // Checks for bottom div and scrolls down from time to time
  window.setInterval(function() {
    var pc = page.evaluate(function() {
      return document.documentElement.innerHTML;
    });

    if (first_load < 100){
      page.evaluate(function() {
        window.document.body.scrollTop = document.body.scrollHeight;

        function click(el){
          var ev = document.createEvent("MouseEvent");
          ev.initMouseEvent(
            "click",
            true /* bubble */, true /* cancelable */,
            window, null,
            0, 0, 0, 0, /* coordinates */
            false, false, false, false, /* modifier keys */
            0 /*left*/, null
          );
          el.dispatchEvent(ev);
        }

        var elements = window.document.getElementsByTagName("div");
        for(var i=0;i<elements.length;i++){
          if(elements[i].className=='ch_page')
	    console.log('click ---------------------')
            click(elements[i]);
        }
        window.document.body.scrollTop = document.body.scrollHeight;
      });

      first_load += 1;
    } else {
      system.stdout.writeLine(pc);
      phantom.exit();
    } 
  }, 1000); // Number of milliseconds to wait between scrolls
});

