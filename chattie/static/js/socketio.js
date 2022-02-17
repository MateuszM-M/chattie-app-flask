document.addEventListener('DOMContentLoaded', () => {

    let socket = io("/");
    // main site functionalities
    try {
    socket.on('userlist_update', function(clients) {
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
            messages.scrollTop = messages.scrollHeight;
            myMessage.focus();
        };

        scrollDownMessages();

        socket.on('connect', () => {
            socket.emit('join_room', {
                'username':username,
                'room': room })
        });

        socket.on('disconnect', () => {
            socket.emit('leave_room', {
                'username':username,
                'room': room })
        });


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
                div = []
                clients.forEach(function (item) {
                    div.push(`<div class="card bg-dark border-light p-1 m-1">${item}</div>`)
                });
                console.log(div)
                    document.getElementById('room_users').innerHTML = div.join("")
            });
        } catch (e) {
            console.log(e)
        }
    } catch (e) {
        console.log(e)
    }
});