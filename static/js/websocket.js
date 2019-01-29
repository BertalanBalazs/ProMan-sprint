const socket = io.connect('http://localhost:8000');
    socket.on('database-change', function(data) {
        console.log(data)
    });