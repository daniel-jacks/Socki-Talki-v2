#!/usr/bin/env node

'use strict';

import { WebSocket } from "ws";
import pkg from 'utf8';
const { encode, decode } = pkg;
import * as readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";
import { readFile } from 'fs/promises';

const json = JSON.parse(
    await readFile(
        new URL('./commands.json', import.meta.url)
    )
);

const socket = new WebSocket("wss://2gc6x410ok.execute-api.us-west-2.amazonaws.com/production");

const rl = readline.createInterface({
    input,
    output
});

let userName = "none";
let roomName = "global";

socket.addEventListener("open", () => {
    console.log(`You have been added to the "global" room by default.`);
    console.log(`Type "*help" for a list of commands`);
    console.log("Websocket connected, retrieving messages..");
    rl.setPrompt(` > `);
    rl.prompt();
});

socket.addEventListener("close", _ => {
    console.log("Websocket disconnected");
    process.exit();
});

socket.addEventListener("error", e => {
    console.log("Websocket encountered error", e);
});

socket.addEventListener("message", response => {
    let payload = decode(response.data);
    output.clearLine();
    output.cursorTo(0);
    console.log(`> ${payload}`);
    rl.prompt(true);
});

rl.on("line", message => {
    let input = message.split(" ");
    let [command, arg] = input.slice(0, 2);
    let payload;
    switch (command) {
        case "*help":
            Object.entries(json).forEach(([key, value]) => {
                console.log(`Command: ${key}`);
                console.log(`         ${value}`);
            });
            break;

        case "*config":
            console.log(`Current username: ${userName}`);
            console.log(`Current roomname: ${roomName}`);
            break;

        case "*setUsername":
            userName = message.split(" ")[1];
            payload = {
                action: "setUsername",
                userName
            };
            socket.send(JSON.stringify(payload));
            break;

        case "*createRoom":
            var requestedRoom = (arg !== "-j") ?
                message.split(" ")[1] :
                message.split(" ")[2];
            payload = {
                action: "createRoom",
                newRoom: requestedRoom,
                autoJoin: false
            };
            if (arg === "-j") {
                payload.autoJoin = true;
                roomName = requestedRoom;
            };
            socket.send(JSON.stringify(payload));
            break;

        case "*changeRoom":
            roomName = message.split(" ")[1];
            payload = {
                action: "changeRoom",
                newRoom: roomName,
            };
            socket.send(JSON.stringify(payload));
            break;

        case "exit":
            socket.close();
            process.exit();

        default:
            payload = {
                action: "message",
                message
            };
            socket.send(JSON.stringify(payload));
    };
    rl.setPrompt(` > `);
    rl.prompt();
});