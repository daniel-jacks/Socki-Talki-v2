<div id="top"></div>

# Socki-Talki

## Summary
This project is a command-line-interface (CLI) chat application that uses Websockets, JavaScript, Python, and the following AWS Services: API Gateway, AWS Lambda, and DynamoDB. On the client-side, I used JavaScript and a few CLI libraries to allow users to interact with the command line and use it as a chat graphical user interface (GUI). The back-end is serverless, using an AWS API Gateway to handle websocket requests and route traffic to a series of Lambdas according to request type. Finally, DynamoDB is used to persist users' connection IDs and keep track of users' respective chat rooms.

## Getting Started
To get started with the project, follow the steps below:

1. Clone the repository.
2. Install the required dependencies locally.
3. Build backend with API Gateway, and all the separate function code.
4. Update the WebSocket endpoint in the main file to connect to the desired server.
5. Run the application.

## Prerequisites
Make sure you have the following prerequisites before running the application:

- Node.js
- AWS Account

## Installation

__Clone the repository:__
```bash
git clone <repository_url>
```

<hr />

__Install the dependencies:__

```bash
npm install
```

__Update the WebSocket endpoint:__
```bash
In the main file, update the WebSocket endpoint URL to connect to your desired server.
```

__Run the application:__
```bash
node client.js
```

## Usage

Once the application is running, you can use the following commands in the command-line interface:

    - *help: Display a list of available commands.
    - *config: Show the current username and roomname.
    - *setUsername <username>: Set the username.
    - *createRoom <roomname> [-j]: Create a new room with an optional auto-join flag (-j).
    - *changeRoom <roomname>: Change the current room.
    - exit: Exit the application.

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

Please replace `<project_name>`, `<repository_url>`, and `<main_file>` with appropriate values specific to your project. You can also customize the sections as needed.

Let me know if you need any further assistance!