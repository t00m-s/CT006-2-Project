$(document).ready(function(){
    const socket = io.connect("http://localhost:5001/chat")
    socket.on('connect', function(){
        socket.send("User connected!");
    });

    socket.on('message', function(data){

    })
})