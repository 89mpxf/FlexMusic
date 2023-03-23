# Handshake Specification

The FlexMusic server will accept all incoming TCP connections while it is online. Once a potential client first establishes a connection with the FlexMusic server, the FlexMusic server will begin sending the client a series of messages to ensure the following:
- The client is a valid FlexMusic client.
- The client is compatible with the FlexMusic server.
- The client's communications to the server can be (and will be) secured.
- The client is authorized to access the FlexMusic server.

This series of initial communication between the server and the client to ensure these requirements are met is called the **handshake**. The handshake is required for the server and the client to communicate, and any clients that fail the handshake will be refused connection.

## Outline

The FmLTP handshake consists of three main portions: the version exchange, the encryption phase, and the authoritative phase. The diagram below outlines these phases, which packets should be sent during each phase, and which member of the handshake sends each packet:

<table>
  <tr>
    <th>Phase</th>
    <th>Packet Type</th>
    <th>Server</th>
    <th>Client</th>
  </tr>
  <tr>
    <td colspan="4"><i>client establishes TCP connection with server</li></td>
  </tr>
  <tr>
    <td rowspan="2"><a href="../docs/HANDSHAKE.md#version_exchange">Version Exchange</a></td>
    <td><a href="../docs/HANDSHAKE.md#server_vex_init">SERVER_VEX_INIT</a></td>
    <td>x</td>
    <td></td>
  </tr>
  <tr>
    <td><a href="./docs/HANDSHAKE.md#client_vex_reply">CLIENT_VEX_REPLY</a></td>
    <td></td>
    <td>x</td>
  </tr>
  <tr>
    <td rowspan="5"><a href="../docs/HANDSHAKE.md#key-exchange--encryption-phase">Encryption Phase</a></td>
    <td><a href="../docs/HANDSHAKE.md#server_kex_init">SERVER_KEX_INIT</a></td>
    <td>x</td>
    <td></td>
  </tr>
  <tr>
    <td>CLIENT_KEX_ID</td>
    <td></td>
    <td>x</td>
  </tr>
  <tr>
    <td>SERVER_KEX_ID</td>
    <td>x</td>
    <td></td>
  </tr>
  <tr>
    <td>CLIENT_KEX_CHAL</td>
    <td></td>
    <td>x</td>
  </tr>
  <tr>
    <td>SERVER_KEX_FINAL</td>
    <td>x</td>
    <td></td>
  </tr>
  <tr>
    <td>Authoritative Phase</td>
    <td colspan="3"><i>Not implemented yet</i></td>
  </tr>
</table>

# Packets
## Version Exchange
The version exchange portion of the handshake serves many purposes. On paper, the version exchange portion is responsible for the first two points listed in the introduction; making sure the client is FlexMusic-compatible and that the version of the client is compatible with the server. In practice, this portion alone will filter out most, if not all:

- Incompatible/old FlexMusic clients (on newer servers)
- Incompatible/new FlexMusic clients (on older servers)
- Non-FlexMusic connections

### SERVER_VEX_INIT
This is the very first packet sent in the handshake. This packet is sent by the server to initiate the handshake, and should be used by the client to manage version compatibility. Once a TCP connection is established, this packet should be sent by the server immediately afterwards.

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
FlexMusic Server,0.0.0\r\n
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
FlexMusic Python Client Library,0.0.0\r\n
```
## Key Exchange / Encryption Phase
Unsurprisingly, the encryption phase of the handshake is the most complicated, but most important, phase of the handshake. Using a combination of the Diffie-Hellman key exchange and the Fernet cipher, the FlexMusic server creates a secure encrypted connection between itself and all of it's clients. This allows for the FlexMusic server and FlexMusic clients to connect to each other, from separate devices or potentially separate networks, without giving up security.

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
