document.addEventListener('DOMContentLoaded', () => {

    let socket = io()
    const users = document.getElementById('users')
    const usesrname = "{{current_user.username}}"


    socket.on('user', function(clients) {
        div = []
        clients.forEach(function (item) {
            div.push(`<div class="card bg-dark border-light p-1 m-1">${item}</div>`)
        })
        users.innerHTML = div.join("")
    });


    document.querySelectorAll('.room_join').forEach(a => {
        a.onclick = () => {
            let room = a.innerHTML
            socket.emit('join', {'username': usesrname, 'room': room});
        };
    });




});