var js = 10;
var css = js * 2;
var html = js * 3;
var java = js * 4;
var sql = js * 5;
var hibernate = js * 6;
var time = "";
var temp = js+1; 
window.setInterval(update, 1000);
function update(){
  // setInterval(update, 1000);
  if (js > 0){
    js = js-0.5;
    minutes = parseInt(js / 60, 10);  
    seconds = parseInt(js % 60, 10);  
    minutes = minutes < 10 ? "0" + minutes : minutes; 
    seconds = seconds < 10 ? "0" + seconds : seconds; 
    time = minutes + ":" + seconds ;  
    document.getElementById("JS1").innerHTML="JS:"+time;
    if(js == 0){
      document.getElementById("JS1").innerHTML="JS";
      document.getElementById("JS1").style.color = "rgba(128, 128, 128, 0.3)";
    }
  }
  if (css > 0){
    css = css-0.5;
    minutes = parseInt(css / 60, 10);  
    seconds = parseInt(css % 60, 10);  
    minutes = minutes < 10 ? "0" + minutes : minutes; 
    seconds = seconds < 10 ? "0" + seconds : seconds; 
    time = minutes + ":" + seconds ;
    if (css < temp) {
      document.getElementById("CSS1").innerHTML="CSS:"+time;
    }
    if(css == 0){
      document.getElementById("CSS1").innerHTML="CSS";
      document.getElementById("CSS1").style.color = "rgba(128, 128, 128, 0.3)";
    }
  }
  if (html > 0){
    html = html-0.5;
    minutes = parseInt(html / 60, 10);  
    seconds = parseInt(html % 60, 10);  
    minutes = minutes < 10 ? "0" + minutes : minutes; 
    seconds = seconds < 10 ? "0" + seconds : seconds; 
    time = minutes + ":" + seconds ;
    if (html < temp) {
    document.getElementById("Html1").innerHTML="Html:"+time;
    }
    if(html == 0){
      document.getElementById("Html1").innerHTML="Html";
      document.getElementById("Html1").style.color = "rgba(128, 128, 128, 0.3)";
    }
  }
  if (java > 0){
    java = java-0.5;
    minutes = parseInt(java / 60, 10);  
    seconds = parseInt(java % 60, 10);  
    minutes = minutes < 10 ? "0" + minutes : minutes; 
    seconds = seconds < 10 ? "0" + seconds : seconds; 
    time = minutes + ":" + seconds ;
    if (java < temp) {
    document.getElementById("Java1").innerHTML="Java:"+time;
    }
    if(java == 0){
      document.getElementById("Java1").innerHTML="Java";
      document.getElementById("Java1").style.color = "rgba(128, 128, 128, 0.3)";
    }
  }
  if (sql > 0){
    sql = sql-0.5;
    minutes = parseInt(sql / 60, 10);  
    seconds = parseInt(sql % 60, 10);  
    minutes = minutes < 10 ? "0" + minutes : minutes; 
    seconds = seconds < 10 ? "0" + seconds : seconds; 
    time = minutes + ":" + seconds ;
    if (sql < temp) {
    document.getElementById("SQL1").innerHTML="SQL:"+time;
    }
    if(sql == 0){
      document.getElementById("SQL1").innerHTML="SQL";
      document.getElementById("SQL1").style.color = "rgba(128, 128, 128, 0.3)";
    }
  }
  if (hibernate > 0){
    hibernate = hibernate-0.5;
    minutes = parseInt(hibernate / 60, 10);  
    seconds = parseInt(hibernate % 60, 10);  
    minutes = minutes < 10 ? "0" + minutes : minutes; 
    seconds = seconds < 10 ? "0" + seconds : seconds; 
    time = minutes + ":" + seconds ;
    if (hibernate < temp) {
    document.getElementById("Hibernate1").innerHTML="Hibernate:"+time;
    }
    if(hibernate == 0){
      document.getElementById("Hibernate1").innerHTML="Hibernate";
      document.getElementById("Hibernate1").style.color = "rgba(128, 128, 128, 0.3)";
    }
  }
}