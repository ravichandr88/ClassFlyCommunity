
//error handling code
// Handle errors.
let handleError = function(err){
  console.log("Error: ", err);
};


// Query the container to which the remote stream belong.
 let remoteContainer = document.getElementById("remote-container");

// Add video streams to the container.
 function addVideoStream(elementId){
  // Creates a new div for every stream
  let streamDiv = document.createElement("div");
  // Assigns the elementId to the div.
  streamDiv.id = elementId;
  // Takes care of the lateral inversion
  streamDiv.style.transform = "rotateY(180deg)";
  // Adds the div to the container.
  remoteContainer.appendChild(streamDiv);
};

// Remove the video stream from the container.
 function removeVideoStream(elementId) {
  let remoteDiv = document.getElementById(elementId);
  if (remoteDiv) remoteDiv.parentNode.removeChild(remoteDiv);
};


//Actaula Code




function start(){
    let client = AgoraRTC.createClient({
      mode: "live",
      codec: "vp8",
  });
  
  client.init("1128f072e89c4034b413a8833804467d", function() {
      console.log("client initialized");
  }, function(err) {
      console.log("client init failed ", err);
  });



    // The value of role can be "host" or "audience".
    client.setClientRole("host");

    // var token =  "006d4cbfcd02b9f446185fe3a8784107a06IACCyE5cefxMCOpQdMjBgwXzMDHDoituRfAm42AsgWXzAJ3mPXcAAAAAEAB+PjEWSY6wYAEAAQBKjrBg";
  var token = ""


    // Join a channel
client.join(token, "car", null, (uid)=>{
  // Create a local stream
}, handleError);
  


let localStream = AgoraRTC.createStream({
  audio: true,
  video: true,
});
// Initialize the local stream
localStream.init(()=>{
  // Play the local stream
  localStream.play("me");
  // Publish the local stream
  client.publish(localStream,handleError);
}, handleError);



  // Subscribe to the remote stream when it is published
  client.on("stream-added", function(evt){
    client.subscribe(evt.stream, handleError);
  });
  
  
  // Play the remote stream when it is subsribed
  client.on("stream-subscribed", function(evt){
    let stream = evt.stream;
    let streamId = String(stream.getId());
    console.log("xxxxxxxxxxxxxxxxxxxxxxx",streamId)
    addVideoStream(streamId);
    stream.play(streamId);
  });
  
  
  
  
  // Remove the corresponding view when a remote user unpublishes.
  client.on("stream-removed", function(evt){
    let stream = evt.stream;
    let streamId = String(stream.getId());
    stream.close();
    removeVideoStream(streamId);
  });
  // Remove the corresponding view when a remote user leaves the channel.
  client.on("peer-leave", function(evt){
    let stream = evt.stream;
    let streamId = String(stream.getId());
    stream.close();
    removeVideoStream(streamId);
  });
  
  

  
return client;



}

var client = start();



function join()
{


  
// Query the container to which the remote stream belong.
 let remoteContainer = document.getElementById("remote-container");

 // Add video streams to the container.
  function addVideoStream(elementId){
   // Creates a new div for every stream
   let streamDiv = document.createElement("div");
   // Assigns the elementId to the div.
   streamDiv.id = elementId;
   // Takes care of the lateral inversion
   streamDiv.style.transform = "rotateY(180deg)";
   // Adds the div to the container.
   remoteContainer.appendChild(streamDiv);
 };
 
 // Remove the video stream from the container.
  function removeVideoStream(elementId) {
   let remoteDiv = document.getElementById(elementId);
   if (remoteDiv) remoteDiv.parentNode.removeChild(remoteDiv);
 };
 

 
  // Subscribe to the remote stream when it is published
client.on("stream-added", function(evt){
  client.subscribe(evt.stream, handleError);
});


// Play the remote stream when it is subsribed
client.on("stream-subscribed", function(evt){
  let stream = evt.stream;
  let streamId = String(stream.getId());
  console.log("xxxxxxxxxxxxxxxxxxxxxxx",streamId)
  addVideoStream(streamId);
  stream.play(streamId);
});




// Remove the corresponding view when a remote user unpublishes.
client.on("stream-removed", function(evt){
  let stream = evt.stream;
  let streamId = String(stream.getId());
  stream.close();
  removeVideoStream(streamId);
});
// Remove the corresponding view when a remote user leaves the channel.
client.on("peer-leave", function(evt){
  let stream = evt.stream;
  let streamId = String(stream.getId());
  stream.close();
  removeVideoStream(streamId);
});



}

