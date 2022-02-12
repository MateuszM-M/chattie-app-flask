document.addEventListener('DOMContentLoaded', () => {

    let socket = io()
    const messages = document.getElementById('messages')
    const button = document.getElementById('sendbutton')
    const myMessage = document.getElementById('myMessage')

    function scrollDownMessages() {
        messages.scrollTop = messages.scrollHeight;
        myMessage.focus();
    };

    scrollDownMessages();

    button.addEventListener('click', function() {
            socket.send(myMessage.value, room, username);
            myMessage.value = "";
    });

    socket.on('message', function(msg) {
        if (msg['username']) {
            messages.innerHTML += `<p> ${msg['username']}: ${msg['message']}</p>`
        } else {
            messages.innerHTML += `<p>${msg['message']}</p>`
        }
        scrollDownMessages()
    });

    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room});
    }

    socket.on('connect', function() {
        console.log(room)
        socket.emit('join', {'username': username, 'room': room});
    })

    socket.on('disconnect', function() {
        console.log(log)
        leaveRoom()
    });

});