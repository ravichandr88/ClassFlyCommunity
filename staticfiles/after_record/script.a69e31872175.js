// Create a code to check whether the .mp4 is avaible in s3 or not.
//Check every 15 seconds.

$(document).ready(function(){

console.log('Very Good');

$('#submit').hide();


});


var check_interval = 10000; // 10 seconds before we call the rest api agian.



async function file_exists()
{

  // meeting_status/<int:aid>/<int:mid>/<int:pfmid>
  const res = await fetch('/spot_file/' + pfmid)
    .then(res => res.json());
    if (res.message == 'success')
    { 
      document.getElementById('dynamic').innerHTML = 'Completed, We will email when done';
      
      $('#submit').show();

      $('#submit').click(function(){
        window.location = '/f_dashh';
      });

    //call the status function again and again to know the status of the video uploaded
      
    }
    else{

      // the code wont connect when person is rejected for some reason
      console.log('failed',res.message);
      alert(res.message);
     

    }
    
  setTimeout(file_exists, check_interval);


}

setTimeout(file_exists, check_interval);


//code to check the status of the video again and agian 
//after sucesful of uploading to the VDO


// async function file_uploaded_status()
// {

//   // meeting_status/<int:aid>/<int:mid>/<int:pfmid>
//   const res = await fetch('/spot_file/' + pfmid)
//     .then(res => res.json());
//     if (res.message == 'success')
//     { 
      
//     //call the status function again and again to know the status of the video uploaded
      
//     }
//     else{

//       // the code wont connect when person is rejected for some reason
//       console.log('failed',res.message);
//       alert(res.message);
     

//     }
    
//   setTimeout(file_exists, check_interval);


// }

// setTimeout(file_exists, check_interval);



