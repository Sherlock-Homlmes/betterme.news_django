/////////////////video
var mapPeers = {};

var userId = document.querySelector("#user-id");
var joinBtn = document.querySelector('#join-btn');
var username;

joinBtn.addEventListener('click',() =>{
    userid = userId.value;
    if (userid == ""){
        return;
    }
    userId.value = ""
    userId.disable = true;
    userId.getElementsByTagName.visibility = 'hidden';

    joinBtn.disable = true;
    joinBtn.getElementsByTagName.visibility = 'hidden';

    var labelUsername = document.querySelector("#label-user-id");
    labelUsername.innerHTML = userid;

    // var loc = window.location;
    // var wsStart = "ws://";

    // if(loc.protocol == "https"){
    //   wsStart = "wss://";
    // }
    // var endPoint = wsStart + loc.host +"/ws/chat/admin";

    // console.log('endPoint:',endPoint);

    // websocket = new WebSocket(endPoint);

    // websocket.addEventListener('open',(e) =>{
    //   console.log('connection open')
    // });
    // websocket.addEventListener('message',websocketOnMessage);
    // websocket.addEventListener('close',(e) =>{
    //   console.log('connection close')
    // });
    // websocket.addEventListener('error',(e) =>{
    //   console.log('connection error')
    // });
})

const constrains = {
  'video': true, 
  'micro':true,
}

var localStream = new MediaStream();
var localVideo = document.querySelector('#local-video');

var userMedia = navigator.mediaDevices.getUserMedia(constrains)
  .then(stream => {
    localStream = stream;
    localVideo.srcObject = localStream;
    localVideo.muted = true;
  })
  .catch(error => {
    console.log('Error accessing media devices',error);
  })

function createVideo(peerUsername){
  var videoContainer = document.querySelector('#video-container');
  var remoteVideo = document.createElement('video');

  remoteVideo.id = peerUsername + '-video';
  remoteVideo.autoplay = true;
  remoteVideo.playsInline = true;

  var videoWrapper = document.createElement('div');
  videoContainer.appendChild(videoWrapper);
  videoWrapper.appendChild(remoteVideo);

  return remoteVideo;
} 

function createOfferer(peerUsername,receiver_channel_name){
  var peer = new RTCPeerConnection(null);
  addLocalTracks(peer);
  var dc = peer.createDataChannel('channel');
  dc.addEventListener('open',() => {
    console.log('connection opened!');
  });
  //dc.addEventListener('message',dcOnMessage);
  
  var remoteVideo = createVideo(peerUsername);
  serOnTrack(peer, remoteVideo);

  mapPeers[peerUsername] = [peer,dc];

  peer.addEventListener('iceconnectionstatechange',() => {
    var iceConnectionState = peer.iceConnectionState;

    if(iceConnectionState === 'failed' || iceConnectionState ==="disconnected" || iceConnectionState === 'close'){
      delete mapPeers[peerUsername];

      if(iceConnectionState != 'close'){
        peer.close();
      }
      remoteVideo(remoteVideo);
    }
  });

  peer.addEventListener('icecandicate',(event) => {
    if (event.candidate){
      console.log('New ice candicate',JSON.stringify(peer.setLocalDescription));
      return;
    }
    sendSignal('news-offer',{
      'sdp':peer.localDescription,
      'receiver_channel_name':receiver_channel_name,
    })
  });

  peer.createOffer()
    .then(o => peer.setLocalDescription(o))
    .then(() =>{
      console.log('Local des set success');
    })
  
}

function addOnTrack(peer){
  localStream.getTracks().forEach(track =>{
      peer.addTrack(track,localStream);
  })
}

function serOnTrack(peer, remoteVideo){
  var remoteStream = new MediaStream();
  remoteVideo.srcObject = remoteStream;
  peer.addEventListener('track', async (event) => {
    remoteStream.addTrack(event,track,remoteStream);
  })
}

function remoteVideo(remoteVideo){
  var videoWrapper = video.parentNode;

  videoWrapper.parentNode.removeChild(videoWrapper);
}