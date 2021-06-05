var rtc = {
    // For the local client.
    client: null,
    // For the local audio and video tracks.
    localAudioTrack: null,
    localVideoTrack: null,
  };
  
  var options = {
    // Pass your app ID here.
    appId: "<YOUR APP ID>",
    // Set the channel name.
    channel: "demo_channel_name",
    // Pass a token if your project enables the App Certificate.
    token: null,
  };
  
  async function startBasicCall() {
    /**
     * Put the following code snippets here.
     */
  }
  
  startBasicCall();



  rtc.client.on("user-published", async (user, mediaType) => {
    // Subscribe to a remote user.
    await rtc.client.subscribe(user, mediaType);
    console.log("subscribe success");
  
    // If the subscribed track is video.
    if (mediaType === "video") {
      // Get `RemoteVideoTrack` in the `user` object.
      const remoteVideoTrack = user.videoTrack;
      // Dynamically create a container in the form of a DIV element for playing the remote video track.
      const playerContainer = document.createElement("div");
      // Specify the ID of the DIV container. You can use the `uid` of the remote user.
      playerContainer.id = user.uid.toString();
      playerContainer.style.width = "640px";
      playerContainer.style.height = "480px";
      document.body.append(playerContainer);
  
      // Play the remote video track.
      // Pass the DIV container and the SDK dynamically creates a player in the container for playing the remote video track.
      remoteVideoTrack.play(playerContainer);
  
      // Or just pass the ID of the DIV container.
      // remoteVideoTrack.play(playerContainer.id);
    }
  
    // If the subscribed track is audio.
    if (mediaType === "audio") {
      // Get `RemoteAudioTrack` in the `user` object.
      const remoteAudioTrack = user.audioTrack;
      // Play the audio track. No need to pass any DOM element.
      remoteAudioTrack.play();
    }
  });