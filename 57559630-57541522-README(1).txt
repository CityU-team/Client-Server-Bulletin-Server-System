--------Client bulletin board system--------


---Python based client-server application---

This project is an implementation of a client bulletin board system as a
part of the client-server application. The system enables clients to
interact with the server by issuing various commands. The server
operates on a designated port and supports four specific commands:
POST_STRING, POST_FILE, GET, and EXIT. Each command serves a distinct
purpose, which is outlined below.

-   POST_STRING: Clients can send a text file to the server line by line. The command (POST_STRING) is the first line, followed by the text lines. Input ends with '&'.
-   POST_FILE: This command lets a client send a text file (up to 256 bytes) from their local machine to the server. The server responds by requesting the absolute path of the file on the client's machine.
-   GET: The server will return all previously posted messages and files from the client and other clients to the client as standard output.
-   EXIT: This command instructs the server to close the socket connection with the client. The server will respond with an acknowledgment message, "OK", confirming the receipt of the command.

After each command is executed, the program will display connection status and send status.


---------------Used libraries---------------

-   socket: The Socket Client is a Python program that allows you to interact with a server using socket communication. You can send messages, send files, and retrieve messages from the server.
-   os: This module provides a portable way of using operating system dependent functionality.
-   struct: It is used mostly for handling binary data stored in files or from network connections, among other sources.
