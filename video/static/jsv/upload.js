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



function god()
{
    var inpt = document.getElementById('good').value;
    console.log(inpt);
    document.getElementById('title').value = inpt;
    console.log(document.getElementById('title').value)

    
    clean(inpt);
}




var wage = document;
console.log(wage) ;

wage.addEventListener("keydown", function (e) {
    console.log('called enter');
    if (e.key === 13) {  //checks whether the pressed key is "Enter"
    console.log('enter pressed');    
    called();
    }
});

function enter(event)
{
    if (event.key === 'Enter') {  //checks whether the pressed key is "Enter"
    const value = event.target.value;
    console.log(event.target.id);
    clean(value);
    }
   
   
}



//gloabl variable

var title = '';


//clean the link and get the youtube id
function clean(str)
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
document.getElementById('video').innerHTML=link;

//function to get title of the video using youtube id
getitle(youtubeid);


}

{/* <td><img src='https://img.youtube.com/vi/L1bumGTCsxk/hqdefault.jpg'></td> */}


function getitle(youtubeid)
{
    
var url = 'https://www.youtube.com/watch?v=' + youtubeid;

var f = $.getJSON('https://noembed.com/embed',
    {format: 'json', url: url}, function (data) {
     console.log(data.title);
       
        window.title =  data.title;
});

return window.title;
}




