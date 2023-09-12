<div id="top"></div>

# Socki-Talki

## Summary
This project is a command-line interface (CLI) chat application that uses Websockets, JavaScript, Python, and the following AWS Services: API Gateway, AWS Lambda, and DynamoDB. On the client-side, I used JavaScript and a few CLI libraries to allow users to interact with the command line and use it as a chat graphical user interface (GUI). The back-end is serverless, using an AWS API Gateway to handle websocket requests and route traffic to a series of Lambdas according to request type. Finally, DynamoDB is used to persist users' connection IDs and keep track of users' respective chat rooms.

## Getting Started
To get started with the project, follow the steps below:

1. Clone the repository.
```bash
git clone git@github.com:daniel-jacks/socki-talki-v2.git
```
2. Change into the 'clientside' folder.
```bash
cd socki-talki-v2/socki-talki-v2-clientside/
```
3. Install the required dependencies locally.
```bash
npm install
```
4. Run the app using 'node' command!
```bash
node client.js
```

_OPTIONAL_

__Create global 'talki' CLI command:__
1. Install Node.js package globally using
```bash
npm install -g
```
2. Run socki-talki from anywhere using 'talki' command!
```bash
talki
```

## Prerequisites
Make sure you have the following prerequisites before attemping to build and run the application:

- Node.js

## Usage

Once the application is running, you can use the following commands in the command-line interface:

    - *help: Display a list of available commands.
    - *config: Show the current username and roomname.
    - *setUsername <username>: Set the username.
    - *createRoom <roomname> -j: Create a new room with an optional auto-join flag '-j'.
    - *changeRoom <roomname>: Change the current room.
    - exit: Exit the application.

## Repository Layout

There are two portions to this codebase, and they work together to provide users quick and reliable chat functionality from the CLI!
1. The 'clientside' folder, responsible for:
- constructing the message payload based off user input and sending along to the server.
- receiving messages and relaying information to users via CLI GUI.

2. The 'serverside' folder, resopnsible for: 
- handling user requests depending on requested endpoint.
- updating users' usernames and rooms according to user requests (these values are stored in DynamoDB, however our Lambda functions access and update these tables according to user reqeusts).

## Contributing

Contributions to the project are welcome. If you want to contribute, please follow these steps:

    - Fork the repository.
    - Create a new branch for your feature or bug fix.
    - Make your changes.
    - Commit your changes.
    - Push the branch to your fork.
    - Open a pull request.

## License

MIT License