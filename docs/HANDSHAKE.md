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
    <th>Encrypted</th>
  </tr>
  <tr>
    <td colspan="5"><i>client establishes TCP connection with server</li></td>
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
    <td>CLIENT_KEX_CHAL</td>
    <td></td>
    <td>x</td>
    <td>Yes</td>
  </tr>
  <tr>
    <td>SERVER_KEX_FINAL</td>
    <td>x</td>
    <td></td>
    <td>Yes</td>
  </tr>
  <tr>
    <td>Authoritative Phase</td>
    <td colspan="4"><i>Not implemented yet</i></td>
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

**From this point forward, all further communications between the server and client are fully encrypted.**

**From this point forward, read all packet tables as what is to be encrypted with the session's Fernet cipher before being sent.**
