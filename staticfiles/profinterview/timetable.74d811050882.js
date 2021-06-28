$(document).ready(function(){


  
console.log("Entered");


// code to put type for time input, since we were not able to get change from forms.py
    $("#id_time").attr("type",'time');

    $('#addd').click( function() {

    console.log('triggered');

    $('#invisible').append('<h5 style=" border-top: 1px dashed red;" ></p>'+
      '<p>DAY</p>'+
      '<select name="day" class="input100" id="id_day">'+
      '<option value="MON">MON</option><option value="TUE">TUE</option><option value="WED">WED</option><option value="THU">THU</option><option value="FRI">FRI</option><option value="SAT">SAT</option><option value="SUN">SUN</option>'+
      '</select>'+
      '<span class="focus-input100"><br><br>'+				
      '</span>'+
      '<span class="symbol-input100"><i class="" aria-hidden="true"></i></span>'+
      '<div class="wrap-input100 " >'+
      '<!-- <input class="input100" type="date" name="con-pass" placeholder="Confirm Password"> -->'+
      '<span class="focus-input100"><br><br>'+		
      '</span>'+
      '<span class="symbol-input100">'+
          '<i class="" aria-hidden="true"></i>'+
        '<!-- <i class="fa fa-lock" aria-hidden="true"></i> -->'+
      '</span>'+
    '</div>'+
    '<p><label for="id_time">Time:</label></p>'+

    '<input type="time" name="time" class="input100" id="id_time">'+
    '<span class="focus-input100"><br><br>'+				
    '</span><span class="symbol-input100">'+
        '<i class="" aria-hidden="true"></i></span> <br>');


});




});

  
  console.log("Startedsssssss");