$(document).ready(function(){
// example.php will be used to send the data to the sever database
$('#example-1').Tabledit({
url: 'example',
editButton: false,
deleteButton: false,
hideIdentifier: true,
columns: {
identifier: [0, 'id'],
editable: [[2, 'first'], [3, 'last'],[3, 'nickname']]
},


});

});



function updateInput(value){
    /*update the value to server*/
    console.log(value);
}






// var wage = document;
// console.log(wage) ;

// wage.addEventListener("keydown", function (e) {
//     console.log('called enter');
//     if (e.key === 13) {  //checks whether the pressed key is "Enter"
//     console.log('enter pressed');    
//     called();
//     }
// });

function enter(event,id)
{
    // document.getElementById('title').innerHTML = document.getElementById('good').value;  
    
    // console.log(document.getElementById('title').innerHTML);

    if (event.key === 'Enter') {  //checks whether the pressed key is "Enter"
    const value = event.target.value;
    // console.log(event.target.value);
    clean(value,id);
    console.log('enter'+id);
    }
   
   
}



//gloabl variable

var title = '';



//clean the link and get the youtube id
function clean(str,id)
{
console.log(str);
var youtubeid;
var link;
var regExp = /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
var match = str.match(regExp);
if (match && match[2].length == 11) {
    youtubeid =  match[2];
} else {
 alert('Sorry, not a valid youtube');
}



var link = '<iframe width="250" height="150" src="https://www.youtube.com/embed/' + youtubeid +'" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>';
document.getElementById('video'+id).innerHTML=link;

document.getElementById('youtube'+id).innerHTML = youtubeid;

//function to get title of the video using youtube id
getitle(youtubeid,id);


}

{/* <td><img src='https://img.youtube.com/vi/L1bumGTCsxk/hqdefault.jpg'></td> */}


function getitle(youtubeid,id)
{
    
var url = 'https://www.youtube.com/watch?v=' + youtubeid;

var f = $.getJSON('https://noembed.com/embed',
    {format: 'json', url: url}, function (data) {
     console.log(data.title);
       
        window.title =  data.title;
        document.getElementById('title'+id).innerHTML=data.title;
});

return window.title;
}

var row_count = 1;


//function to new row
function add_row()
{ 
    console.log('called'+window.row_count);
    window.row_count += 1;

    div = ' <tr id="head'+window.row_count+'" >'+
    '<th scope="row" style="display: none;">'+window.row_count+'</th>'+
    '<td class="tabledit-view-mode"  style="cursor: pointer;"   onkeypress="enter(event,'+window.row_count+')"><span  class="tabledit-span" id="title'+window.row_count+'">ClassFly Community'+
       ' </span><input class="tabledit-input form-control input-sm"  type="text" name="First Name" value="" id="good'+window.row_count+'" style="display: none;" disabled=""></td>'+
   
    '</tr><tr id="body'+window.row_count+'">'+
        '<th scope="row" style="display: none;">'+window.row_count+'</th>'+
   ' <td id="video'+window.row_count+'"><iframe width="250" height="150" src="https://www.youtube.com/embed/nUPAbWOcwb4" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></td>'+
  
'</tr>'+
'<tr id="tail'+window.row_count+'">'+
'<th scope="row" style="display: none;">1</th>'+
'<td> '+
'<p id="youtube'+window.row_count+'"></p><button  onclick="del('+window.row_count+')">delete</button>  </td>'+
'</tr>';



    // document.getElementById('rowj').innerHTML  = document.getElementById('rowj').innerHTML  + div;
    document.getElementById('rowj').insertAdjacentHTML('beforeend', div);

}


//final submit function
function load_all()
{
    console.log(window.row_count);
    var id_link= [];
    for (var x = 1; x <= window.row_count;x++)
    {
        id_link[x-1] = document.getElementById("youtube"+x).innerHTML
        // id_link.push(document.getElementById("youtube"+x).innerHTML);
    }
    console.log(id_link);

    $.ajax({
        type: "POST",
        url: 'playlist',
        data: {'id_list':JSON.stringify(id_link),
                'subject':document.getElementById('subject').value,
                'playlist':document.getElementById('header').innerHTML},
        success:  function( data ) {
        console.log(data);
        window.location = 'videoslist';
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            console.log(errorThrown)
        }
      });
}

//to delete that rows with given id
function del(id)
{
    document.getElementById('head'+id).remove();
    document.getElementById('body'+id).remove();
    document.getElementById('tail'+id).remove();
    window.row_count -=1;
}


function update()
{
    document.getElementById('header').innerHTML=document.getElementById('headline').value ;
   console.log(document.getElementById('subject').value);
}



