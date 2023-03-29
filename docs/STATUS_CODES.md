# Status Codes
All messages from the FlexMusic server begin with a three-digit integer. This integer is a FmLTP **status code**, and it can be used by the client to determine the state of the server, and/or the server's response to a command/operative. In short, the server packs this extra information into all of it's responses for the client to use for handling the FmLTP session.

Status codes are generally grouped by their first and second digits. The first digit delimits the general cause of the status code, and the second digit delimits a more specific sub-grouping of codes.

## 1xx (Interpreter Startup / Lockdown Mode Specific)
### 10x (Compatibility)
<table>
  <tr>
    <th>Code</th>
    <th>Reason</th>
  </tr>
  <tr>
    <td>100</td>
    <td>The client and server are both the same version.</td>
  </tr>
  <tr>
    <td>101</td>
    <td>The client's compatibility sub-stepping is higher than the server's.</td>
  </tr>
  <tr>
    <td>102</td>
    <td>The server's compatibility sub-stepping is higher than the client's.</td>
  </tr>
</table>

### 11x (Compatibility)
<table>
  <tr>
    <th>Code</th>
    <th>Reason</th>
  </tr>
  <tr>
    <td>110</td>
    <td>The client's compatibility stepping is higher than the server's.</td>
  </tr>
  <tr>
    <td>111</td>
    <td>The client's compatibility stepping is higher than the server's, and the client's compatibility sub-stepping is higher than the server's.</td>
  </tr>
  <tr>
    <td>112</td>
    <td>The client's compatibility stepping is higher than the server's, and the server's compatibility sub-stepping is higher than the client's.</td>
  </tr>
</table>

### 12x (Compatibility)
<table>
  <tr>
    <th>Code</th>
    <th>Reason</th>
  </tr>
  <tr>
    <td>120</td>
    <td>The server's compatibility stepping is higher than the client's.</td>
  </tr>
  <tr>
    <td>121</td>
    <td>The server's compatibility stepping is higher than the client's, and the client's compatibility sub-stepping is higher than the server's.</td>
  </tr>
  <tr>
    <td>122</td>
    <td>The server's compatibility stepping is higher than the client's, and the server's compatibility sub-stepping is higher than the client's.</td>
  </tr>
</table>

### 15x (Authentication)
<table>
  <tr>
    <th>Code</th>
    <th>Reason</th>
  </tr>
  <tr>
    <td>150</td>
    <td>Authentication successful.</td>
  </tr>
  <tr>
    <td>151</td>
    <td>Authentication failed.</td>
  </tr>
</table>

## 2xx (Command/Operative Success)
### 20x (General Success)
<table>
  <tr>
    <th>Code</th>
    <th>Reason</th>
  </tr>
  <tr>
    <td>200</td>
    <td>General success.</td>
  </tr>
</table>

## 4xx (Failure)
### 40x (Interpreter Failure)
<table>
  <tr>
    <th>Code</th>
    <th>Reason</th>
  </tr>
  <tr>
    <td>400</td>
    <td>Invalid command or operative.</td>
  </tr>
</table>

### 41x (Command/Operative Failure)
<table>
  <tr>
    <th>Code</th>
    <th>Reason</th>
  </tr>
  <tr>
    <td>410</td>
    <td>Too many arguments passed.</td>
  </tr>
  <tr>
    <td>411</td>
    <td>Too few arguments passed.</td>
  </tr>
</table>

### 42x (Command Failure)
<table>
  <tr>
    <th>Code</th>
    <th>Reason</th>
  </tr>
  <tr>
    <td>420</td>
    <td>Command error.</td>
  </tr>
</table>
