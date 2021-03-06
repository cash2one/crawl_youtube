// Copyright 2014 letv Inc. All Rights Reserved.
// Author: guoxiaohe@letv.com

var page = require('webpage').create()
var system = require('system');
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
page.open(url, function(status) {
  if (status !== 'success') {
    //console.log('Unable to access network');
    system.stderr.writeLine('Unable to access network')
    phantom.exit(1);
  } else {
    page.render('/tmp/login.png')
    //var ua = page.evaluate(function() {
    //  return document.documentElement.innerHTML;
    //});
    //system.stdout.writeLine(ua)
    phantom.exit(0);
    //console.log(ua);
  }
});
