
/*
 *  These procedures use Agora Video Call SDK for Web to enable local and remote
 *  users to join and leave a Video Call channel managed by Agora Platform.
 */

/*
 *  Create an {@link https://docs.agora.io/en/Video/API%20Reference/web_ng/interfaces/iagorartcclient.html|AgoraRTCClient} instance.
 *
 * @param {string} mode - The {@link https://docs.agora.io/en/Voice/API%20Reference/web_ng/interfaces/clientconfig.html#mode| streaming algorithm} used by Agora SDK.
 * @param  {string} codec - The {@link https://docs.agora.io/en/Voice/API%20Reference/web_ng/interfaces/clientconfig.html#codec| client codec} used by the browser.
 */

 if(user == 'prof')
 {

  console.log(user);

var client = AgoraRTC.createClient({ mode: "rtc", codec: "vp8" });
 
/*
 * Clear the video and audio tracks used by `client` on initiation.
 */
var localTracks = {
  videoTrack: null,
  audioTrack: null
};


console.log('******************************Pressed');
console.log(option);

/*
 * On initiation no users are connected.
 */
var remoteUsers = {};

/*
 * On initiation. `client` is not attached to any project or channel for any specific user.
 */
/*
 * When this page is called with parameters in the URL, this procedure
 * attempts to join a Video Call channel using those parameters.
 */


// $(() => {
//   var urlParams = new URL(location.href).searchParams;
//   option.appid = urlParams.get("appid");
//   option.channel = urlParams.get("channel");
//   option.token = urlParams.get("token");
//   option.uid = urlParams.get("uid");
//   if (option.appid && option.channel) {
//     $("#uid").val(option.uid);
//     $("#appid").val(option.appid);
//     $("#token").val(option.token);
//     $("#channel").val(option.channel);
//     $("#join-form").submit();
//   }
// })

/*
 * When a user clicks Join or Leave in the HTML form, this procedure gathers the information
 * entered in the form and calls join asynchronously. The UI is updated to match the option entered
 * by the user.
 */ 

 $("#join-form").click(async function (e) {

  console.log('******************************Pressed');
  console.log(option);

  e.preventDefault();
 
  try {

    //call for server to inform connecting to call
    const res = await fetch('/pro_join/' + uid +'/' +meet)
    .then(res => res.json());
    if (res.message == 'joined')
    {
      console.log('Success',res.message);
      $("#join").attr("disabled", true);
    }
    else{
      // the code wont connect when person is rejected for some reason
      console.log('failed',res.message);
      return ;
    }

   


    await join(); 
    if(option.token) {
      $("#success-alert-with-token").css("display", "block");
    } else {
      $("#success-alert a").attr("href", `index.html?appid=${option.appid}&channel=${option.channel}&token=${option.token}`);
      $("#success-alert").css("display", "block");
    }
  } catch (error) {
    console.error(error);
  } finally {
    $("#leave").attr("disabled", false);
  }
})

/*
 * Called when a user clicks Leave in order to exit a channel.
 */
$("#leave").click(function (e) {
  leave();
})

/*
 * Join a channel, then create local video and audio tracks and publish them to the channel.
 */
async function join() {
  // Add an event listener to play remote tracks when remote user publishes.
  client.on("user-published", handleUserPublished);
  client.on("user-unpublished", handleUserUnpublished);

  // Join a channel and create local tracks. Best practice is to use Promise.all and run them concurrently.
  [ option.uid, localTracks.audioTrack, localTracks.videoTrack ] = await Promise.all([
    // Join the channel.
    client.join(option.appid, option.channel, option.token || null, option.uid || null),
    // Create tracks to the local microphone and camera.
    AgoraRTC.createMicrophoneAudioTrack(),
    AgoraRTC.createCameraVideoTrack()
  ]);

  // Play the local video track to the local browser and update the UI with the user ID.
  localTracks.videoTrack.play("local-player");
  $("#local-player-name").text(`localVideo(${option.uid})`);

  // Publish the local video and audio tracks to the channel.
  await client.publish(Object.values(localTracks));
  console.log("publish success");
}

/*
 * Stop all local and remote tracks then leave the channel.
 */
async function leave() {
  for (trackName in localTracks) {
    var track = localTracks[trackName];
    if(track) {
      track.stop();
      track.close();
      localTracks[trackName] = undefined;
    }
  }

  // Remove remote users and player views.
  remoteUsers = {};
  $("#remote-playerlist").html("");

  // leave the channel
  await client.leave();

  $("#local-player-name").text("");
  $("#join").attr("disabled", false);
  $("#leave").attr("disabled", true);
  console.log("client leaves channel success");
}


/*
 * Add the local use to a remote channel.
 *
 * @param  {IAgoraRTCRemoteUser} user - The {@link  https://docs.agora.io/en/Voice/API%20Reference/web_ng/interfaces/iagorartcremoteuser.html| remote user} to add.
 * @param {trackMediaType - The {@link https://docs.agora.io/en/Voice/API%20Reference/web_ng/interfaces/itrack.html#trackmediatype | media type} to add.
 */
async function subscribe(user, mediaType) {
  const uid = user.uid;
  // subscribe to a remote user
  await client.subscribe(user, mediaType);
  console.log("subscribe success");
  if (mediaType === 'video') {
    const player = $(`
      <div id="player-wrapper-${uid}">
        <p class="player-name">remoteUser(${uid})</p>
        <div id="player-${uid}" class="player"></div>
      </div>
    `);
    $("#remote-playerlist").append(player);
    user.videoTrack.play(`player-${uid}`);
  }
  if (mediaType === 'audio') {
    user.audioTrack.play();
  }
}

/*
 * Add a user who has subscribed to the live channel to the local interface.
 *
 * @param  {IAgoraRTCRemoteUser} user - The {@link  https://docs.agora.io/en/Voice/API%20Reference/web_ng/interfaces/iagorartcremoteuser.html| remote user} to add.
 * @param {trackMediaType - The {@link https://docs.agora.io/en/Voice/API%20Reference/web_ng/interfaces/itrack.html#trackmediatype | media type} to add.
 */
function handleUserPublished(user, mediaType) {
  const id = user.uid;
  remoteUsers[id] = user;
  subscribe(user, mediaType);
}



/*
 * Remove the user specified from the channel in the local interface.
 *
 * @param  {string} user - The {@link  https://docs.agora.io/en/Voice/API%20Reference/web_ng/interfaces/iagorartcremoteuser.html| remote user} to remove.
 */
function handleUserUnpublished(user) {
  const id = user.uid;
  delete remoteUsers[id];
  $(`#player-wrapper-${id}`).remove();
}


// Code to connect if he has disconnected in between the meeting
// this code will connect them autmatically
if(auto_connect == 'True')
{
  let element = document.getElementById('join-form');
  element.click();
  console.log('Auto connect');
}


// Code to get the meeting status from everyone

var h = 0;
var interval = 1000;
var check_interval = 20000;

var pro_count = 0;  // profesional count
var fre_count = 0;  //fresher return count
var rec_count = 0;  // recording count
var get_time = 1;
var chance = 0;   //variable to record the chance given to keep up with meeting.,

// if the chance is gfreater than 3, stop the meeting and recording.

async function meeting_status()
{

  // meeting_status/<int:aid>/<int:mid>/<int:pfmid>
  const res = await fetch('/meeting_status/' + aid  +'/' + mid + '/' + pfmid + '/' + get_time )
    .then(res => res.json());
    if (res.message == 'success')
    { 
      //check if time is recived or not, if received set 'get_time = 0', 
      // if not receivd call tick_tock(res.time)
      if (get_time == 1 && typeof res.time != 'undefined' )
      {
        tick_tock(res.time)
        get_time = 0;
      }

      
      // check whether the status of profesional or fresher has changed or not
      if (pro_count == res.pro )
      {
          chance = chance + 1;
      }
      else if( pro_count == res.fres)
      {
        chance = chance + 1;
      }
      else if( rec_count == res.record ) 
      {
        chance = chance + 1;
      }
      else{
        chance = 0;
      }

      pro_count = res.pro
      fre_count = res.fres
      rec_count = res.record
      
      console.log(pro_count, fre_count, rec_count);

      
      
      // check the chance given, if it is greater than 3, close the window
      if (chance > 5)
      {
        leave();
        window.location = '/pro_dashboard' ;

      }
       
    }
// If it recieves any message saying stop, stop the meeting
    else if (res.message == 'stop')
    {
      window.location = '/pro_dashoard';
    }
    else{
      leave();
      // the code wont connect when person is rejected for some reason
      console.log('failed',res.message);
      window.close(); 
    }

    
    setTimeout(meeting_status, interval);


}

setTimeout(meeting_status, interval);





 }


 
window.fun = function()
{
  this.document.getElementById('leave').click();
  window.location = '/pro_dashboard';
  
}


 function tick_tock(time)
{
// Set the date we're counting down to
var countDownDate = new Date().getTime() + (time * 1000);
// console.log(countDownDate);
// Update the count down every 1 second
var x = setInterval(function() {

  // Get today's date and time
  var now = new Date().getTime();
  // new Date(now + (30*60*1000));
// console.log(now);
  // Find the distance between now and the count down date
  var distance = countDownDate - now;

  // Time calculations for days, hours, minutes and seconds
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

  // Display the result in the element with id="demo"
  document.getElementById("demo").innerHTML =  hours + ":"
  + minutes + ":" + seconds ;
  // console.log('testing');
  // If the count down is finished, write some text
  if (distance < 0) {
    clearInterval(x);
    window.fun();
    document.getElementById("demo").innerHTML = "EXPIRED";
  
    
  }
}, 1000);


}



