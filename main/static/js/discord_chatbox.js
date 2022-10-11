//////////////// chat
function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
}
const userToken = getCookie("discord_access_token")
const form = document.querySelector("form")
const chatMessages = document.querySelector(".chat__messages")
const input = document.querySelector(".sendMessage")

let url = `ws://${window.location.host}/ws/chat/${room_name}`;
console.log(url);
const chatSocket = new WebSocket(url);

form.addEventListener("submit", sendMessage)


chatSocket.onmessage = function(e) {
    let data = JSON.parse(e.data);
    console.log('Data:',data);
    const userName = data.user_name;
    const userAvatar = data.user_avatar;
    const messageReceive = data.message;
    showMessage(userName,userAvatar,messageReceive);
  };
  

function showMessage(userName,userAvatar,messageReceive) {

    if(messageReceive !== "") {
        var messageDiv = document.createElement("div")
        messageDiv.className = "message"

        var avatar = document.createElement("img")
        avatar.src = userAvatar

        var messageInfo = document.createElement("div")
        messageInfo.className = "message__info"

        var userInfo = document.createElement("h4")
        userInfo.innerHTML = userName

        var messageTimestamp = document.createElement("span")
        messageTimestamp.className = "message__timestamp"

        const date = new Date()
        const year = date.getFullYear()
        const month = String(date.getMonth()).padStart(2, "0")
        const day = String(date.getDate()).padStart(2, "0")

        messageTimestamp.innerHTML = month + "/" + day + "/" + year

        const message = document.createElement("p")

        message.innerHTML = messageReceive

        userInfo.appendChild(messageTimestamp)
        messageInfo.appendChild(userInfo)
        messageInfo.appendChild(message)

        messageDiv.appendChild(avatar)
        messageDiv.appendChild(messageInfo)

        chatMessages.appendChild(messageDiv)
        chatMessages.scrollBy(0, 10000)
    }
}

function sendMessage(e){
    e.preventDefault()

    if(input.value !== "") {

        chatSocket.send(JSON.stringify({
            'user_token': userToken,
            'message': input.value
        }));

        input.value = ""
    }
}


$.ajax({
  type: 'GET',
  url: 'load-chat/'+lastMessage,
  success: function(response){
      console.log(response,typeof(response));
      for (let res in response){
        const userName = response[res].username;
        const userAvatar = response[res].avatar_url;
        const messageReceive = response[res].message;
        showMessage(userName,userAvatar,messageReceive);
      }

  },
  error: function(error){
      console.log('load fail');
  }
})

//search message
const choosen_topic = document.getElementById("topic");
const search_input = document.getElementById("search-message");
const search_dropdown = document.getElementById("search-dropdown");
const client = new MeiliSearch({ host: 'http://localhost:7700', apiKey: 'masterKey' });
index = client.index("employee_chat");
var lim = 10;
let topic_type = {};

//topic converter
$.ajax({
    type: 'GET',
    url: '/topic-type/',
    success: function(request){
        topic_type = request;
    },
    error: function(error){
        console.log("can't get topic_type");
    }
})

//search engine
async function search_news(name){
    var results = await index.search(name,{
        limit: lim,
        attributesToHighlight: ["*"],
    });

    //console.log(results);
    return results;
}

function instant_search(){
    (async () => {
        if (search_input.value == ""){
            search_dropdown.innerHTML = ``;
        } 
        else{
            const results = await search_news(search_input.value)
            .then(function(result){return result.hits});
            console.log(results);
            if (results.length > 0){

                search_dropdown.innerHTML = 
                `<li><p>`+results[0].title+`</p></li>`;
                
                for (let hit=1; hit < results.length; hit++){
                    //console.log(results[hit],typeof(results[hit]));
                    search_dropdown.innerHTML += 
                    `
                    <li><hr class="dropdown-divider"></li>
                    <li><p>`+results[hit].title+`</p></li>
                    `

                };
            }
            else{
                search_dropdown.innerHTML = ``;
            }
        }

    })()

}

$('#choose-topic li').on('click', function(){
    choosen_topic.innerHTML = $(this).text();
    //console.log(search_input.value)
    if (search_input.value != ""){
        instant_search();
    }

  });

$( "#search-message" ).keyup(function() {
    instant_search();
});

$( "#search-message" ).keydown(function() {
    instant_search();
});