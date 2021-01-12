// function to change chapter window
function chng_window(sub,id)
{
    console.log('sub:'+sub+'Chaptrid :'+id);
    window.location = id;
  
}


function get(list)
{
    list = list.replace(/&#39;/g, '"');
    list = list.replace("[",'');
    list = list.replace("]",'');
    list = list.split(',');

    //first call the current playing video id and fill the title


    $.each(list, function( index, value ) {
    {
   
    str = value;
    str = str.replace(/"/g,'');
    str = str.replace(' ','');
    
       
    
    call(str)
    }

});
}   


function call(str)
{
    let apiKey = 'AIzaSyCkWKAEdLX7FJ9SQ7DWtBSDW2S6TXbJBQw';
    let url = 'https://www.googleapis.com/youtube/v3/videos?id=' + "n4Zb0Y4hXIA" + '&part=snippet&key=' + apiKey;
    $.getJSON(url, function(data){
        if (data && data.items && data.items[0]) {

            // $(node).text(data.items[0].snippet.title);
            var myEle = document.getElementById('o'+str);
            if(myEle){
                document.getElementById('o'+str).innerHTML=data.items[0].snippet.title;//'o' represents the title in the desktop videos list
            }
            else{
                document.getElementById(str).innerHTML=data.items[0].snippet.title;
            }
            } else {
            console.log('video not exists');
        }
    });

    // $.ajax({
    //     url: 'https://noembed.com/embed?url='+'https://www.youtube.com/watch?v=' + str,
    //     crossDomain:true,
    //     async:true, 
    //     type: 'GET',
    //     dataType : 'jsonp',
    //     success: function(data){
    //         var myEle = document.getElementById('o'+str);
    //         if(myEle){
    //             document.getElementById('o'+str).innerHTML=data.title;//'o' represents the title in the desktop videos list
    //         }
           
    //             document.getElementById(str).innerHTML=data.title;
          
    //   }});




}

function close_panel()
{
    document.getElementById('close_panel').click();
    console.log('clicked');
}

function change(videoid)
{   
    //change the pargrah contrent to 'Playing'
    console.log(videoid);
    var old_id = $('#ytVideo').attr('name');
    console.log(old_id);
    
    document.getElementById('ime'+old_id).innerHTML = '';
    document.getElementById('ime'+videoid).innerHTML = 'Playing...';
    
    // // //change the old pragrah content to empty
    

    // $('#ytVideo').attr('name', varsize);


    // //now to chnage the embed video
    

    document.getElementById('frist').innerHTML = '';
    
    document.getElementById('frist').innerHTML = '<div  onclick="play()" class="llyv" data-id="'+ videoid +'" id="ytVideo" name="'+ videoid +'"><div  onclick="play()" class="llyv-play-btn" ></div><img  onclick="play()" src="https://img.youtube.com/vi/'+ videoid +'/hqdefault.jpg"></div><h5 id="first_title"></h5>';
  

    // <div class="llyv" data-id="f6aGTY0CgZs" id="ytVideo" name="f6aGTY0CgZs">
    // <div class="llyv-play-btn"></div>
    // <img src="https://img.youtube.com/vi/f6aGTY0CgZs/hqdefault.jpg">
    // <div class="llyv-play-btn"></div>
    // <img src="https://img.youtube.com/vi/f6aGTY0CgZs/hqdefault.jpg"></div>
    // <h5 id="first_title"></h5>
  
    /*

  {% if cf %}
 
    <div class="llyv" data-id="{{first_video}}" id="ytVideo"  name="{{first_video | default:'f6aGTY0CgZs' }}"></div>
    <h5 id="first_title" >ClassFly Community<br><br></h5>
  </div>
  {% else %}
  <div id='frist'>
      <div class="llyv" data-id="{{first_video.0}}" id="ytVideo"  name="{{first_video.0 | default:'f6aGTY0CgZs' }}" ></div>
      <h5 id='first_title'>{{first_video.1}}<br><br></h5>
    </div>
  {% endif %}

    */



    // $('#ytVideo').attr('data-id',videoid);
    
    // $( "#ytVideo" ).load(window.location.href + " #ytVideo" );
    // $( "#first" ).load(window.location.href + " #first" );
    
    // $( "#huj" ).load(window.location.href + " #huj" );
    // console.log($('#ytVideo').attr('data-id'));
   
   
}

function play()
{
    console.log('playing');
   document.getElementById('ytVideo').innerHTML = '<iframe src="https://www.youtube.com/embed/'+ $('#ytVideo').attr('name') +'?rel=0&amp;showinfo=0&amp;autoplay=1" allowfullscreen="" allow="autoplay" frameborder="0"></iframe>';
}



//function to add content for initla play card
$(document).ready(function(){

    close_notes();
    
   console.log("checked");
    var old_id = $('#ytVideo').attr('name');
    console.log(old_id);
    if(old_id == '')
    return;
    var myEle = document.getElementById('ime'+old_id);
    if(myEle){
        document.getElementById('ime'+old_id).innerHTML='Playing...';
    }
    // document.getElementByID()
    // console.log(document.getElementById('im'+old_id));
 
    // $.ajax({
    //     url: 'https://noembed.com/embed?url='+'https://www.youtube.com/watch?v=' + old_id,
    //     crossDomain:true,
    //     async:true, 
    //     type: 'GET',
    //     dataType : 'jsonp',
    //     success: function(data){
            
    //   document.getElementById('first_title').innerHTML =  data.title;
    //     console.log(data.title);
    //   }, 
    //   error: function(XMLHttpRequest, textStatus, errorThrown) { 
    //     document.getElementById('first_title').innerHTML =  'ClassFly Community';
    // }  
    // });



    let apiKey = 'AIzaSyCkWKAEdLX7FJ9SQ7DWtBSDW2S6TXbJBQw';
    let url = 'https://www.googleapis.com/youtube/v3/videos?id=' + old_id + '&part=snippet&key=' + apiKey;
    $.getJSON(url, function(data){
        if (data && data.items && data.items[0]) {
            console.log()
            document.getElementById('first_title').innerHTML = data.items[0].snippet.title
            // $(node).text();
        } else {
            document.getElementById('first_title').innerHTML =  'ClassFly Community';
        }
    });

});



// hide the notes after closing
function close_notes()
{
    for(var x = 1; x < 10; x++)
    {
        // console.log(document.getElementById("#note"+x).innerHTML);
   var e = document.getElementById("note"+x);
   if(e)
   {
   
    $("#note"+x).hide();
   }
  
}

}




function open_notes(id)
{
    close_notes();
$('#note'+id).show();
}