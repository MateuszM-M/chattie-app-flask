document.addEventListener('DOMContentLoaded', () => {

    let mainSocket = io();
    let socket = io("/chat");
    // main site functionalities
    console.log(socket)
    try {
        mainSocket.on('userlist_update', function(clients) {
            div = []
            clients.forEach(function (item) {
                div.push(`<div class="card bg-dark border-light p-1 m-1">${item}</div>`)
            });
            try {
                document.getElementById('users').innerHTML = div.join("")
            } catch (e) {}
        });
    } catch (e) {}
    
    
    // room functionalities
    try {
        function scrollDownMessages() {
            document.getElementById('messages').scrollTop = messages.scrollHeight;
            document.getElementById('myMessage').focus();
        };

        scrollDownMessages();



        document.getElementById('sendbutton').addEventListener('click', function() {
            socket.emit('message', myMessage.value, room, username);
            document.getElementById('myMessage').value = "";
        });

        socket.on('message', function(msg) {
            if (msg['username']) {
                document.getElementById('messages').innerHTML += `<p> ${msg['username']}: ${msg['message']}</p>`
            } else {
                document.getElementById('messages').innerHTML += `<p>${msg['message']}</p>`
            }
            scrollDownMessages()
        });

        try {
            socket.on('roomlist_update', function(clients) {
                console.log(clients)
                div = []
                clients.forEach(function (item) {
                    div.push(`<div class="card bg-dark border-light p-1 m-1">${item}</div>`)
                });
                    document.getElementById('room_users').innerHTML = div.join("")
            });
        } catch (e) {
            console.log(e)
        }
    } catch (e) {
        console.log(e)
    }
});