document.addEventListener('DOMContentLoaded', () => {

    let socket = io()
    const messages = document.getElementById('messages')
    const button = document.getElementById('sendbutton')
    const myMessage = document.getElementById('myMessage')

    function scrollDownMessages() {
        messages.scrollTop = messages.scrollHeight;
        myMessage.focus()
    }

    scrollDownMessages()

    button.addEventListener('click', function() {
        socket.send(myMessage.value);
        myMessage.value = "";
    });

    socket.on('message', function(msg) {
        messages.innerHTML += '<p>'+msg+'</p>';
        scrollDownMessages()
    });

    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room});
    }

    socket.on('disconnect', function() {
        leaveRoom()
        console.log('disco')
    })

});