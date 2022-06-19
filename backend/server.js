const express = require("express");
const { Socket } = require("socket.io");

const app = express();

const PORT = 8081;

const db = require('./models')

const server = require('http').createServer(app);
const io = require("socket.io")(server, {
    pingTimeout : 1,
    pintInterval: 1000,

})
app.get('/', async (req,res) => {
    const result = await db['sensing'].findAll({
        attributes: ['num1']
    });
    console.log(result)
    res.send(result)
})

io.on('connection', async (Socket)=>{
    const result1 = await db['sensing'].findAll({
        attributes: ['num1']
    });
    const result2 = await db['sensing'].findAll({
         attributes: ['num2']
     });
     const result3 = await db['sensing'].findAll({
        attributes: ['num3']
    });

    num1Msg=(result1.map(e=>e.dataValues.num1))
    num2Msg=(result2.map(e=>e.dataValues.num2))
    num3Msg=(result3.map(e=>e.dataValues.num3))
 
    Socket.emit("pres",num1Msg)
    Socket.emit("temp",num2Msg)
    Socket.emit("humi",num3Msg)
})

server.listen(PORT, () => console.log(`이 서버는 ${PORT}번 포트로 동작 중`))
