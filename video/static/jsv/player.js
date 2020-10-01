function chng_window(sub,id)
{
    console.log('sub:'+sub+'Chaptrid :'+id);
    window.location = id;
  
}

function get(list)
{
    list = list.replace(/&#39;/g, '"')
    list = list.replace("[",'')
    list = list.replace("]",'');
    list = list.split(',')

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
    $.ajax({
        url: 'https://noembed.com/embed?url='+'https://www.youtube.com/watch?v=' + str,
        crossDomain:true,
        async:true, 
        type: 'GET',
        dataType : 'jsonp',
        success: function(data){
        document.getElementById(str).innerHTML=data.title;
        // console.log(data.title);
      }});
}



function change(varsize)
{   
    //change the pargrah contrent to 'Playing'
    console.log(varsize);
    document.getElementById('im'+varsize).innerHTML = 'Playing...';
    
    // //change the old pragrah content to empty
    var old_id = $('#ytVideo').attr('name');
    console.log(old_id);
    document.getElementById('im'+old_id).innerHTML = '';

    $('#ytVideo').attr('name', varsize);


    //now to chnage the embed video

    document.getElementById('video-responsive').innerHTML = '<iframe width="780" height="439" id="ytVideo" name="'+ varsize +'" src="https://www.youtube.com/embed/'+ varsize+'" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

}

//function to add content for initla play card
$(document).ready(function(){
   
    var old_id = $('#ytVideo').attr('name');
    console.log(old_id);
    if(old_id == '')
    return;
    document.getElementById('im'+old_id).innerHTML = 'Playing...';
    // document.getElementByID()
    console.log(document.getElementById('im'+old_id));

    $.ajax({
        url: 'https://noembed.com/embed?url='+'https://www.youtube.com/watch?v=' + old_id,
        crossDomain:true,
        async:true, 
        type: 'GET',
        dataType : 'jsonp',
        success: function(data){
            
      document.getElementById('first_title').innerHTML =  data.title;
        console.log(data.title);
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) { 
        document.getElementById('first_title').innerHTML =  'ClassFly Community';
    }  
    });

});

