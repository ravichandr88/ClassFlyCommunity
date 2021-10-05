skills 
var total_seconds = (skills.length * 600) + 1;
var temp_seconds = 0;
var time = "";
var past_id = 0; 
var id  = 0;
window.setInterval(update, 1000);

function update(){
  // setInterval(update, 1000);
  id = skills.length - parseInt(total_seconds / 600 ) - 1;
  total_seconds -= 1;
  if (total_seconds > 0){
    total_seconds = total_seconds-1;
    minutes = parseInt( ( total_seconds - (skills.length-id - 1) * 600) / 60, 10);  
    seconds = parseInt(( total_seconds - (skills.length-id - 1) * 600) % 60, 10);  
    console.log(total_seconds,skills.length-id - 1,( total_seconds - (skills.length-id - 1) * 600))
    minutes = minutes < 10 ? "0" + minutes : minutes; 
    seconds = seconds < 10 ? "0" + seconds : seconds; 
    time = minutes + ":" + seconds ;  
    document.getElementById("skill"+id).innerHTML = skills[id] + ":"+time;
    console.log('id',id,'pastid',past_id,tmp);
    if(id > 0 && id != past_id){
      
      var tmp = past_id;
      past_id = id ;
      while(tmp >= 0)
      {
      document.getElementById("skill"+tmp).innerHTML=skills[tmp] ;
      document.getElementById("skill"+tmp).style.color = "rgba(128, 128, 128, 0.3)";
      tmp = tmp -  1;  
    }
    } 
  }
  else{
    document.getElementById("skill"+id).innerHTML=skills[id] ;
      document.getElementById("skill"+id).style.color = "rgba(128, 128, 128, 0.3)";
      
  }
  
}