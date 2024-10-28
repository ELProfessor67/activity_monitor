const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server,{
    cors: {
        origin: '*', // Adjust this to your needs for production
        methods: ['GET', 'POST'],
        allowedHeaders: "*",
        credentials: true
    }
});

io.on('connection', (socket) => {
    console.log('a user connected',socket.id);

    socket.on("join",({room_id}) => {
        socket.join(room_id);
        console.log(room_id)
    });
    
    socket.on("on_event", ({event,room_id}) => {
        console.log(event,'event')
        socket.to(room_id).emit('on_event', {event});
    });

    socket.on("on_order",({room_id,type}) => {
        socket.to(room_id).emit("on_order",type);
    })

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
});

server.listen(3000, () => {
    console.log('listening on *:3000');
});
