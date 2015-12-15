var div=document.createElement("div");
var arr=[0];
div.setAttribute('id','showBox');
div.style.display='none';
document.body.appendChild(div);
function start(){
  console.log("start up succeed!");
  var i=1;
  var t=setInterval(function(){
    div.innerHTML+=arr[i].innerHTML;
    i++;
    if(i==arr.length){
      clearInterval(t);
    }},100);
}
var countList1= 1,index= 1;
+function () {
  for(var i=0;i<document.querySelector(".mod_types ul").childNodes.length;i++){
    if(document.querySelector(".mod_types ul").childNodes[i].nodeType==1){
      countList1++;}
  }
  var timer0=setInterval(function(){
    var timer1=setTimeout(function () {
      var e1 = document.createEvent("MouseEvents");
      e1.initEvent("click", true, true);
      document.querySelector(".mod_types ul li:nth-child("+index+")").dispatchEvent(e1);
      index++;
      var timer2=setTimeout(function () {
        var countList2=0;
        var timer3=setInterval(function () {
          if(countList2==document.querySelector(".team_list").childNodes.length){
            clearInterval(timer3);
            if(index==countList1){start();}
          }
          else if(document.querySelector(".team_list").childNodes[countList2].nodeType==1){
            var e2 = document.createEvent("MouseEvents");
            e2.initEvent("click", true, true);
            document.querySelector(".team_list").childNodes[countList2].dispatchEvent(e2);
            var timer4=setTimeout(function(){if(document.querySelectorAll(".schedule_r .figures_list").length>0){
              for(var i=0;i<document.querySelectorAll(".schedule_r .figures_list").length;i++){
                arr.push(document.querySelectorAll(".schedule_r .figures_list")[i]);
              }
            }},100);}
          countList2++;
        },50);
      },50);
    },400);
    if(index==(countList1-1)){
      clearInterval(timer0);}
},5000)
}();
