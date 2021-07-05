var script = document.createElement('script');
script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js';


async function clock()
{
    // error_mssg
   window.stop = 0;
   document.getElementById('dynamic').innerHTML = '';
    // await fetch().then(
        fetch("/email/otp/resend").then((response) => {
            if (response.ok) {
                document.getElementById('dynamic').innerHTML = '<p>Email OTP re-sent successfully</p>';
   
            } else {
              console.log(response.status);
              document.getElementById('error_mssg').innerHTML = 'You have crossed otp limits,Please contact Support.'
                window.stop = 1;
            }
          })
      

    for (let i = 1; i < 30; i++) 
{
    setTimeout(function timer() 
        {
            if(window.stop == 1)
            {
                document.getElementById('dynamic').innerHTML = '';
 
            }
            else 
            {
                // console.log(Math.floor(i/60),'minutes',i%60,'seconds');
                if(i > 4)
                {
                    document.getElementById('dynamic').innerHTML = 'Wait '+(5-Math.floor(i/60))+':'+(60-(i%60))+' to resend OTP.'
                }
                if(i == 60)
                {
                    document.getElementById('dynamic').innerHTML = '<button class="login100-form-btn" onclick="clock()">Rsend OTP</button>';
                    console.log('Ended');
                }
            }
       
        }, i * 1000);

    
}
}


document.getElementById('dynamic').innerHTML = '<button class="login100-form-btn" onclick="clock()">Resend OTP </button>'