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
    <td rowspan="2">Version Exchange</td>
    <td><a href="https://github.com/89mpxf/FlexMusic/blob/main/docs/HANDSHAKE.md#server_vex_init">SERVER_VEX_INIT</a></td>
    <td>x</td>
    <td></td>
  </tr>
  <tr>
    <td><a href="https://github.com/89mpxf/FlexMusic/blob/main/docs/HANDSHAKE.md#client_vex_reply">CLIENT_VEX_REPLY</a></td>
    <td></td>
    <td>x</td>
  </tr>
  <tr>
    <td>Encryption Phase</td>
    <td colspan="3"><i>Not implemented yet</i></td>
  </tr>
  <tr>
    <td>Authoritative Phase</td>
    <td colspan="3"><i>Not implemented yet</i></td>
  </tr>
</table>

## Packets
### SERVER_VEX_INIT
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
    <td>Service Name</td>
    <td>str</td>
    <td>The name of the service (typically, "FlexMusic").</td>
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
FlexMusic,0.0.0
```
### CLIENT_VEX_REPLY
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
    <td>Service Name</td>
    <td>str</td>
    <td>The name of the service (typically, "FlexMusic").</td>
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
FlexMusic,0.0.0
```
