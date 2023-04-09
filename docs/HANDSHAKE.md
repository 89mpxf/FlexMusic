# Handshake Specification

The FlexMusic server will accept all incoming TCP connections while it is online. Once a potential client first establishes a connection with the FlexMusic server, the FlexMusic server will begin sending the client a series of messages to ensure the following:
- The client is a valid FlexMusic client.
- The client is compatible with the FlexMusic server.
- The client's communications to the server can be (and will be) secured.
- The client is authorized to access the FlexMusic server.

This series of initial communication between the server and the client to ensure these requirements are met is called the **handshake**. The handshake is required for the server and the client to communicate, and any clients that fail the handshake will be refused connection.

## Outline

The FmLTP handshake consists of three main portions: the version exchange, the encryption phase, and the authentication phase. The diagram below outlines these phases, which packets should be sent during each phase, and which member of the handshake sends each packet:

<table>
  <tr>
    <th>Phase</th>
    <th>Packet/Message Type</th>
    <th>Server</th>
    <th>Client</th>
    <th>Encrypted</th>
  </tr>
  <tr>
    <td colspan="5"><i>client establishes TCP connection with server</i></li></td>
  </tr>
  <tr>
    <td rowspan="2"><a href="../docs/HANDSHAKE.md#version_exchange">Version Exchange</a></td>
    <td><a href="../docs/HANDSHAKE.md#server_vex_init">SERVER_VEX_INIT</a></td>
    <td>x</td>
    <td></td>
    <td>No</td>
  </tr>
  <tr>
    <td><a href="./docs/HANDSHAKE.md#client_vex_reply">CLIENT_VEX_REPLY</a></td>
    <td></td>
    <td>x</td>
    <td>No</td>
  </tr>
  <tr>
    <td rowspan="5"><a href="../docs/HANDSHAKE.md#key-exchange--encryption-phase">Encryption Phase</a></td>
    <td><a href="../docs/HANDSHAKE.md#server_kex_init">SERVER_KEX_INIT</a></td>
    <td>x</td>
    <td></td>
    <td>No</td>
  </tr>
  <tr>
    <td><a href="../docs/HANDSHAKE.md#client_kex_id">CLIENT_KEX_ID</a></td>
    <td></td>
    <td>x</td>
    <td>No</td>
  </tr>
  <tr>
    <td><a href="../docs/HANDSHAKE.md#server_kex_id">SERVER_KEX_ID</a></td>
    <td>x</td>
    <td></td>
    <td>No</td>
  </tr>
  <tr>
    <td><a href="../docs/HANDSHAKE.md#client_kex_chal">CLIENT_KEX_CHAL</a></td>
    <td></td>
    <td>x</td>
    <td>Yes</td>
  </tr>
  <tr>
    <td><a href="../docs/HANDSHAKE.md#interpreter-ready-message">"Interpreter Ready." message</a></td>
    <td>x</td>
    <td></td>
    <td>Yes</td>
  </tr>
  <tr>
    <td rowspan="2"><a href="../docs/HANDSHAKE.md#authentication-phase">Authentication Phase</a></td>
    <td><a href="../docs/HANDSHAKE.md#auth-command">"AUTH" command</a></td>
    <td></td>
    <td>x</td>
    <td>Yes</td>
  </tr>
  <tr>
    <td><a href="../docs/HANDSHAKE.md#150151-response">150/151 Response</a></td>
    <td>x</td>
    <td></td>
    <td>Yes</td>
  </tr>
</table>

# Packets
## Version Exchange
The version exchange portion of the handshake serves many purposes. On paper, the version exchange portion is responsible for the first two points listed in the introduction; making sure the client is FlexMusic-compatible and that the version of the client is compatible with the server. In practice, this portion alone will filter out most, if not all:

- Incompatible/old FlexMusic clients (on newer servers)
- Incompatible/new FlexMusic clients (on older servers)
- Non-FlexMusic connections

### SERVER_VEX_INIT
This is the very first packet sent in the handshake. This packet is sent by the server to initiate the handshake, and should be used by the client to manage version compatibility. Once a TCP connection is established, this packet should be sent by the server immediately afterwards. The value of this packet should be saved by the client once it receives it, as it will be needed later on in the handshake process.

<table>
  <tr>
    <th colspan="3"><b>Fields</b></th>
  </tr>
  <tr>
    <th>Field</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Version Friendly Name</td>
    <td>str</td>
    <td>The friendly version string of the server. Should always start with "FlexMusic".</td>
  </tr>
  <tr>
    <td><i>separator</i></td>
    <td>Literal[str]</td>
    <td>","</td>
  </tr>
  <tr>
    <td>Version</td>
    <td>str</td>
    <td>The server version in x.y.z format, where:
      <ul>
        <li>x is the compatibility class of the server.</li>
        <li>y is the compatibility stepping of the server.</li>
        <li>z is the compatibility sub-stepping of the server.</li>
      </ul>
    </td>
  </tr>
</table>

For example, a valid SERVER_VEX_INIT packet should look something like this:

```
FlexMusic Server,0.0.0
```
### CLIENT_VEX_REPLY
This is the second packet sent in the handshake process, and the first packet in the handshake sent by the client. This packet does two things; establish that the client is also a FlexMusic entity, and to manage version compatibility on the server side.

<table>
  <tr>
    <th colspan="3"><b>Fields</b></th>
  </tr>
  <tr>
    <th>Field</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Version Friendly Name</td>
    <td>str</td>
    <td>The friendly version string of the client. Should always start with "FlexMusic".</td>
  </tr>
  <tr>
    <td><i>separator</i></td>
    <td>Literal[str]</td>
    <td>","</td>
  </tr>
  <tr>
    <td>Version</td>
    <td>str</td>
    <td>The client version in x.y.z format, where:
      <ul>
        <li>x is the compatibility class of the client.</li>
        <li>y is the compatibility stepping of the client.</li>
        <li>z is the compatibility sub-stepping of the client.</li>
      </ul>
    </td>
  </tr>
</table>

For example, a valid CLIENT_VEX_REPLY packet should look something like this:

```
FlexMusic Python Client Library,0.0.0
```
## Key Exchange / Encryption Phase
Unsurprisingly, the encryption phase of the handshake is the most complicated, but most important, phase of the handshake. Using a combination of the Diffie-Hellman Key Exchange and the Fernet cipher, the FlexMusic server creates a secure encrypted connection between itself and all of it's clients. This allows for the FlexMusic server and FlexMusic clients to connect to each other, from separate devices or potentially separate networks, without giving up security.

In basic terms, the entire process should look like this:
1. While the FlexMusic server is starting, it generates two extremely large prime numbers, or "parameters". This set of parameters will be used for all connections. After the FlexMusic server closes, it will generate another set of parameters once it is started again, and so on.
2. When a client connects, they enter the handshake. Once the client and the server exchange versions, the server will send the client these parameters in a serialized format.
3. When the client recieves these parameters, it should use them to generate a random private and public key, or a "keypair". Once the public key is serialized, the client should send it to the server.
4. When the server recieves the client's public key, it will then generate a random keypair of it's own, and will then exchange it's private key with the client's public key to generate the shared key.
5. Once the server has the shared key, it will then perform HKDF to derive the SHA256 key that will be used for encryption. Once this key is in a url-safe base64 encoded form, it can be used for Fernet encryption/decryption.
6. After the server has a valid Fernet cipher, it will send it's public key to the client. From that point, the client should follow the same steps as the server to perform the functions necessary for generating it's Fernet cipher.
7. Once both the server and the client have generated the Fernet cipher for this session, the client should reply to the server with the value of the server's SERVER_VEX_INIT packet (from the version exchange portion), but encrypted with this cipher.
8. Assuming the server recieves and successfully decrypts this message, the server will reply to the client with a status message. From this point forward, the server will begin accepting FmLTP operatives.

**Important! At no point EVER should the client or server send one another their private key or the shared key for the session, even after the session has been encrypted.**

### SERVER_KEX_INIT
This packet begins the encryption phase of the handshake. In order to begin the key exchange, the server sends it's Diffie-Hellman key parameters to allow the client to generate it's own compatible keypair.

<table>
  <tr>
    <th>Field</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Parameters</td>
    <td>bytes</td>
    <td>Diffie-Hellman parameters, in PKCS3 format with PEM encoding.</td>
  </tr>
</table>

For example, a valid SERVER_KEX_INIT packet should look like this:
```
-----BEGIN DH PARAMETERS-----
MIGHAoGBAK0a7BmdPoU2/snNlwsT8oW1G76yUTABAGcwoiOTFbAe+XARtx+gkILH
6eyWCKx6mn38HdBd9WdzRSMk6O1j0NrubsuSUKpXZSpc9mTtzyrp8ZfVv+223vci
Z/f5KhcPuk4EijhOd17vqsXXCalSWlP4nh8RlLkqAFuQudvxwNxvAgEC
-----END DH PARAMETERS-----
```
_(note: the parameters above are for example purposes only. FlexMusic generates a new set of parameters everytime the server is launched.)_

### CLIENT_KEX_ID
Once the client recieves the server's key generation parameters and generates a keypair of it's own, this packet returns the client's public key to the server.

<table>
  <tr>
    <th>Field</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Client Public Key</td>
    <td>bytes</td>
    <td>Diffie-Hellman public key, in SubjectPublicKeyInfo format with PEM encoding.</td>
  </tr>
</table>

For example, a valid CLIENT_KEX_ID packet should look something like this:
```
-----BEGIN PUBLIC KEY----
MIIBHzCBlQYJKoZIhvcNAQMBMIGHAoGBAIyAW0EUlyzVg3PZQTxRfLnbuyPu183B
SFlj6eSuDljEFWxIRu1/EomghMDVUXA1AbxMuLshALmz+OHDa6ovAAuf8RCdBxI2
Zi7MwEdp4i7CJuCraMeFW7XmVhSSrC22pYdMMz6TT9bw0M3j18c8vdirbr7uxmLQ
bdGyvhKDuBzPAgECA4GEAAKBgEPO5uRdV8x1H41Z1qetiLAknjo1YP7Sleo/Ocma
ipFpTyKhaAWWVZSEIgOyJZs6zY1x2nSXdlsg6wkNErHQ3pqgrJZM24Q3uC7wyFT1
YVHqhTdk735h5WWsG+XIgtmpyVNqIMMpBri0Z8bL2MO8zUjI7h5PvWcOwtfrvto+
r4nX
-----END PUBLIC KEY-----
```
_(note: the public key above is for example purposes only.)_

### SERVER_KEX_ID
Assuming the client sends a valid public key in the previous packet, the server will generate it's own keypair. This packet relays the server's public key back to the client.

<table>
  <tr>
    <th>Field</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Server Public Key</td>
    <td>bytes</td>
    <td>Diffie-Hellman public key, in SubjectPublicKeyInfo format with PEM encoding.</td>
  </tr>
</table>

For example, a valid SERVER_KEX_ID packet should look something like this:
```
-----BEGIN PUBLIC KEY-----
MIIBIDCBlQYJKoZIhvcNAQMBMIGHAoGBAOcrCbO0xRkVhwXNR0x27pRT+urJV83/
aO0+eZir5zB+PH5TmoQf+fx/7V3hqwfwUxqODwfLSj4EaKxL8xO66UPCzX435zLM
i/R/MlDsz9HnydPNTVVI9N+qBFKYaeJu/BsSFg3Ribx4+ZLBo7BrWnSFuqQsiz3s
FFSjfdwzVjsPAgECA4GFAAKBgQCAmW2AwjoL+zpsVsewcnlD41IHrbnuGU/9FwOP
WWH+jbtH0poXoOxIOicvG4PIQ4wLkfwcOP627hkNbRlMgXLNe0HfcV294DxAZPI9
NPx+BYqaaMzroE2Quz5V9vp3Apmp2J7OYvvOneFmU87PyomBZJj0Ed3BRfA6J0F+
C0GggA==
-----END PUBLIC KEY-----
```
_(note: the public key above is for example purposes only.)_

**From this point forward, all further communications between the server and client are fully encrypted.**

**From this point forward, read all packet tables as what is to be encrypted with the session's Fernet cipher before being sent.**

### CLIENT_KEX_CHAL
This is the first encrypted packet sent during the handshake. This packet's main purpose is to ensure that both the server and the client have the same cipher. The client does this by sending the value of the server's SERVER_VEX_INIT packet back to the server to check it against itself.

<table>
  <tr>
    <th>Field</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Server's SERVER_VEX_INIT</td>
    <td>str</td>
    <td>The value of the server's SERVER_VEX_INIT packet as a string.</td>
  </tr>
</table>

For example, assuming the server's version was v1.0.0, the CLIENT_KEX_CHAL should look something like this (before being encrypted):
```
FlexMusic Server,1.0.0
```

**From this point forward, all data will be sent to the server in the form of FmLTP operatives/commands, and all further responses from the server will be in the form of status codes and messages.**

### "Interpreter Ready." message
Assuming that the server receives and successfully decrypts the previous packet, and the value of the previous packet matches the expected value, the server will then pass the session to the FmLTP interpreter. This message is the FmLTP's interpreter's first message, and it is intended to inform the client that the server is ready to start receiving commands.

If the server's authentication mode is set to `none`, the server should respond like this:
```
100 FmLTP/1.0 Interpreter Ready.
``` 
The FmLTP is immediately ready to begin accepting all commands/operatives. The handshake is fully completed here, and you do not need to enter the authentication phase.

However, if the server's is set to anything other than `none` (i.e. `auth` or `system`), the server will respond like this:
```
100 FmLTP/1.0 Interpreter Ready.
Authentication required.
```
The `Authentication required.` line indicates that the FmLTP interpreter has been restricted to what is known as **lockdown mode**. In this state, the server will only accept `AUTH`, `HELP`, and `QUIT` commands.

_(note: more information regarding the status codes in this specific message can be found in sections 10x-12x [here](https://github.com/89mpxf/FlexMusic/blob/main/docs/STATUS_CODES.md#1xx-interpreter-startup--lockdown-mode-specific).)_

## Authentication Phase
At this point, we have addressed the first three points in the introduction. There is only one thing left to do, and that is ensuring the client is authenticated to run FmLTP commands/operatives. If the FlexMusic server that the client is connecting to has disabled authentication, as described in [previous section](../docs/HANDSHAKE.md#interpreter-ready-message), then you can skip this phase of the handshake entirely.

Due to it's optionality by design, this phase will sometimes not be apart of the handshake at all. However, when authentication is required by the server, it should be handled before further commands/operatives are passed to the server. Hence, **it should still be treated as a part of the handshake.**

### "AUTH" command
If authentication is required by the server, the interpreter will start in lockdown mode. The **AUTH command** is exclusive to this mode and is used by the client to authenticate to the server.

<table>
  <tr>
    <th>Field</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Command</td>
    <td>Literal[str]</td>
    <td>"AUTH"</td>
  </tr>
  <tr>
    <td>Username</td>
    <td>str</td>
    <td>The username to authenticate to the server as.</td>
  </tr>
  <tr>
    <td>Password</td>
    <td>str</td>
    <td>The password associated with the username desired.</td>
  </tr>
</table>

For example, a client authenticating as the user ``user`` with the password ``12345678`` should send the following AUTH command:
```
AUTH user 12345678
```

### 150/151 Response
Once the client attempts to authenticate to the server via the AUTH command, the server will then respond with whether or not authentication succeeded. This is in the form of status messages, corresponding to status codes **150** and **151**.

For example, if the client successfully authenticates with the server, the server will respond with the following message:
```
150 Authentication successful.
```
This response signifies that the interpreter has exited lockdown mode and authenticated was successful. **At this point, the handshake has fully concluded.**

However, if the client fails to authenticate with the server, the server will respond with the following message:
```
151 Authentication failed.
```
This response signifies that the authentication attempt was unsuccessful. This could mean that the user requested does not exist, or that the password provided was incorrect. Authentication can be reattempted a set number of times defined by the server (3 by default, however, the server will not present this information to the client) before the connection will be automatically closed.

It should be noted that if the client fails to authenticate with the server by means of an unrelated factor, such as the client passing the AUTH command incorrectly, it will respond with a different message, and a different status code. For more information as to possible failure status codes, click [here](https://github.com/89mpxf/FlexMusic/blob/main/docs/STATUS_CODES.md#4xx-failure).
