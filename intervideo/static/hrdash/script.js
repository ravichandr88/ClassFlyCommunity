
// code for the expansion of the answers by the applicants
function answer(id)
{
//    document.getElementById(id).innerHTML = answers[id];

$('[name=row-hidden]').hide();
$('#'+id).show();
}

// function to close answers division in the page
function close(id)
{
    $('#'+id).hide(); 
}


// code to shorlist select option fot the candidates

function change_status(id, status)
{
    $(document).ready(function(){
    $.get("/change/status/"+id.slice(6,)+'/'+status, function(data, status_code){

    if(data.message == 'success')
    {

    if( status == 'short')
    {
        document.getElementById(id).innerHTML =   '<i class="fa fa-dot-circle-o text-info" ></i>Shortlist '
    }
    else if (status == 'select')
    {
        document.getElementById(id).innerHTML = '<i class="fa fa-dot-circle-o text-success"></i>Select';
    }
    else 
    {
        document.getElementById(id).innerHTML = '<i class="fa fa-dot-circle-o text-danger"></i> Reject';
    }

}
else{
    alert('Not Upadated');
}
});
});
    
}




// function to filter the applicants using the skills from HRDASHboard
function search()
{
   var skills =  document.getElementById('skill_input').value;

   if (skills == '')
    {
skills = 'not';
    }
   window.location = '/hr_dash/' + job_id + '/' + skills;
   console.log(skills);
}


function clear()
{
    console.log('Very Good');
    window.location = '/hr_dash/' + job_id ;
}
























//download the resume code
function download(url)
{
    window.open(url, '_blank').focus();
}


$(document).ready(function(){

    $('[name=skill_button]').click(function () {
        if($(this).css("background-color") == 'rgb(255, 133, 26)')
        $(this).css("background-color", "rgb(168, 50, 50)");
        else
        $(this).css("background-color", "rgb(255, 133, 26)");
    });
});


//Function to invite an applicant to the Job posted by the HR
function invite(id,fid,)
{
    // invite/<int:fid>/<int:jobid>
    $(document).ready(function(){
        $.get("/invite/" + fid + "/" + job_id, function(data, status_code){
    
        if(data.message == 'success')
        {   
                document.getElementById(id).innerHTML =   '<i class="fa fa-dot-circle-o text-success" ></i>Invited'
        }

        else
        {
            alert('Error');
        }
});
    });

}


var g_skills       = []
var g_stream       = []
var g_exp_min   = -1
var g_exp_max   = -1
var g_city         = []


//filter for skills
function skillfilter(skill)
{
    
// first check whether the skill is in the gloabl skills list or not
// var g_skills = window.skills;


//update gloabl skill list
if(g_skills.includes(skill))
 {
     //removing the skill from glaobl skills list, if already present
    
     const index = g_skills.indexOf(skill);
     if (index > -1) {
       g_skills.splice(index, 1);
     }
  
 }
 else{
    g_skills.push(skill)
 }

console.log(g_skills)
 global_filter();
 return 

}



function exp_filter(exp)
{
    
if(exp != -1)
{
g_exp_min = exp*12; //just converting uears into months
g_exp_max = (exp+1)*12; //maximum months is year + 1 * 12 months
}
else
{
    g_exp_max = -1;
    g_exp_min = -1;
}



// console.log('g-min',g_exp_min,'---g-maxx',g_exp_max);
global_filter();
return;   

}



function stream_filter(stream)
{
    console.log(stream, g_stream);

    //update gloabl skill list
    if(g_stream.includes(stream))
{
    //removing the skill from glaobl skills list, if already present
    const index = g_stream.indexOf(stream);
     if (index > -1) {
        g_stream.splice(index, 1);
     }
}

else{
    g_stream.push(stream);    //i f the experience is not presernt in the list push it to list
}

global_filter();

return;   

}


//City filter function
function city_filter(city)
{

    //update gloabl skill list
    if(g_city.includes(city))
{
    //removing the skill from glaobl skills list, if already present
    const index = g_city.indexOf(city);
     if (index > -1) {
        g_city.splice(index, 1);
     }
}

else{
    g_city.push(city);    //i f the experience is not presernt in the list push it to list
}
global_filter();
console.log(g_city);

return;   

}


function global_filter()
{
    //first get all the table rows ,
    //hide all the rows,
    //show the row onliy if it matches with all the keys
    //query with respect to skills
    //query with city
    //query with  experience
    //query with stream


    //get all the table rows
    
    $('[name=applicant-rows]').hide();
    $('[name=row-hidden]').hide();



    var skill_elements = document.getElementsByName("skills")
    
    for( var x = 0; x < skill_elements.length; x++)
    {
    skills = skill_elements[x].innerHTML;   //get the skills listed in the name element
    var show = true;

    // id of the applicant object
    var id = skill_elements[x].id;
        id = id.slice(5,);
    

    //city element value
    var city_element = document.getElementById("city"+id);

    //stream element value
    var stream = document.getElementById("branch"+id) ;

    //experience element value
    var exp  = parseInt(document.getElementById("exp"+id).innerHTML);
    
    //for loop checks whether the "skills" are present or not
    for(var i = 0; i < g_skills.length ; i++)
        {
        if(!skills.includes(g_skills[i]))
            {
            show = false;
            }
        } 

    //condition to check whether the "city" is present or not
    if(!g_city.includes(city_element.innerHTML) && g_city.length > 0)
        {
            show = false;
        }

        // console.log(stream.innerHTML);

    //condition to check based on "stream/branch" 
    if(!g_stream.includes(stream.innerHTML) && g_stream.length > 0)
    {
        show = false;
    }

    //code to filter with "Experience"
    console.log(exp,(exp < g_exp_min || exp > g_exp_max));
    if((exp <= g_exp_min || exp >= g_exp_max) && g_exp_max != -1)
    {
        show = false;
    }
    

    //code to show the candidate if the "show" boolean is true
    if(show)
    {
        $('#row'+id).show();
    }
    }

}

