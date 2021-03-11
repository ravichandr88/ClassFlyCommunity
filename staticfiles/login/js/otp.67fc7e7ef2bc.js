function clock()
{
    fetch("/resend_otp");
for (let i = 1; i < 300; i++) 
{

    setTimeout(function timer() 
        {
        console.log(Math.floor(i/60),'minutes',i%60,'seconds');
        }, i * 1000);
    if(i == 300)
    {
        
    }
}
}