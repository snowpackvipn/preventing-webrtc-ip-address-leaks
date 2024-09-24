# Testing the WebRTC IP adress leak

## Table of contents

[1. Test web page](#1-test-web-page)  
[2. Information about the scripts used on the web page](#2-information-about-the-scripts-used-on-the-web-page)  
[References](#references)  

## 1. Test web page

<small><i>This section is a copy of [section 3 - Testing the WebRTC IP adress leak](../README.md#3-testing-the-webrtc-ip-adress-leak) from the `1-testbed/README.md` file.</i></small>

1. Copy this entire `3-web-page` folder to your default `Downloads` folder<sup>[1](#footnote-1)</sup>.

<small id="footnote-1"><sup>[1](#1-test-web-page)</sup>This non-mandatory step makes it easy to access the test web page in the containerised browser solution (cf. [section 4 of the `1-testbed/README.md`](../../README.md#42-containerised-web-browser-solution)), as the `Downloads` folder on the host system (which can be Linux, Windows or macOS) is shared with the containers.</small>

***Linux/macOS***

```bash
cp -R ./preventing-webrtc-ip-address-leaks/1-testbed/3-web-page/ ~/Downloads
```

***Windows***

```powershell
Copy-Item -Path ".\preventing-webrtc-ip-address-leaks\1-testbed\3-web-page\" -Destination "$USERPROFILE\Downloads" -Recurse
```

2. Open the `index.html` page using the web browser you want to use by typing typing the following path in the address bar:

***Linux/macOS***

```bash
~/Downloads/3-web-page/index.html
```

***Windows***

```
file:///C:/Users/USERNAME/Downloads/3-web-page/index.html
```

3. Provide your STUN and TURN server adresses, click on the button **Gather ICE candidates** and see the addresses that have been gathered.

4. Restart the experiment by **turning ON** the switch **Give getUserMedia() permission**, click on the button **Gather ICE candidates** and see the new addresses that have been gathered.

## 2. Information about the scripts used on the web page

The tests used on this web page are as follows. Four tests intended to be executed in a browser console are available by contacting STUN and TURN server, with or without access authorisation for media devices (microphone/camera). This authorisation is managed by the [`getUserMedia()`](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia) method [[1](#references)]:

 a. *STUN* server contact **without** media device access permissions;  
 b. *STUN* server contact **with** media device access permissions;  
 c. *TURN* server contact **without** media device access permissions;  
 d. *TURN* server contact **with** media device access permissions.  

Please change the following fields to the servers you wish to use. You can use as many servers as you like, separated by commas (more information about the URI schemes in the RFC 7064 and 7065 [[2, 3](#references)]):
 - `STUN_SERVER_IPv4_ADRESS:PORT`
 - `[STUN_SERVER_IPv6_ADRESS]:PORT`
 - `STUN_SERVER_DOMAIN_NAME:PORT`<br><br>
 - `TURN_SERVER_IPv4_ADRESS:PORT`
 - `[TURN_SERVER_IPv6_ADRESS]:PORT`
 - `TURN_SERVER_DOMAIN_NAME:PORT`
 - `TURN_PASSWORD`
 - `TURN_USERNAME`

If you do not want to host your own STUN/TURN servers (see [`1-testbed/1-stun-turn-setup`](../1-stun-turn-setup/README.md)), you can find public servers via this non-exhaustive list of URLs. **Please note that to see IPv6 address leaks, the client (web browser) and the server (STUN/TURN) must support IPv6**:
 - https://dev.to/alakkadshaw/google-stun-server-list-21n4
 - https://gist.github.com/mondain/b0ec1cf5f60ae726202e
 - https://www.metered.ca/tools/openrelay/

These JavaScript codes are based on the code located in the work of Reiter and Marsalek [[4](#references)].

#### a. STUN server contact *without* getUserMedia()

```js
var pc = new RTCPeerConnection({iceServers: [{
    urls: [ "stun:STUN_SERVER_IPv4_ADRESS:PORT"
          , "stun:[STUN_SERVER_IPv6_ADRESS]:PORT"
          , "stun:STUN_SERVER_DOMAIN_NAME:PORT" ]}]}, {optional: [{RtpDataChannels: true}]});
pc.createDataChannel("STUN without getUserMedia permission WebRTC Leak");
pc.createOffer().then(offer => pc.setLocalDescription(offer));
pc.onicecandidate = event => {
    if (event.candidate) {
        var cdte = event.candidate.candidate;
        if (cdte !== "") {console.log(cdte);}
    }
}
```

#### b. STUN server contact *with* getUserMedia()

```js
navigator.mediaDevices.enumerateDevices()
    .then(devices => {
        const cams = devices.filter(device => device.kind == "videoinput");
        const mics = devices.filter(device => device.kind == "audioinput");

        const constraints = { video: cams.length > 0, audio: mics.length > 0 };
        return navigator.mediaDevices.getUserMedia(constraints);
    })
    .then(function(stream) {
    var pc = new RTCPeerConnection({iceServers: [{
        urls: [ "stun:STUN_SERVER_IPv4_ADRESS:PORT"
            , "stun:[STUN_SERVER_IPv6_ADRESS]:PORT"
            , "stun:STUN_SERVER_DOMAIN_NAME:PORT" ]}]}, {optional: [{RtpDataChannels: true}]});
    pc.createDataChannel("STUN with getUserMedia permission WebRTC Leak");
    pc.createOffer().then(offer => pc.setLocalDescription(offer));
    pc.onicecandidate = event => {
        if (event.candidate) {
            var cdte = event.candidate.candidate;
            if (cdte !== "") {console.log(cdte);}
        }
    }
})
```

#### c. TURN server contact *without* getUserMedia()

```js
var pc = new RTCPeerConnection({iceServers: [{
    urls: [ "turn:TURN_SERVER_IPv4_ADRESS:PORT"
          , "turn:[TURN_SERVER_IPv6_ADRESS]:PORT"
          , "turn:TURN_SERVER_DOMAIN_NAME:PORT" ],
    credential: "TURN_PASSWORD",
    username: "TURN_USERNAME" }]}, {optional: [{RtpDataChannels: true}]});
pc.createDataChannel("TURN without getUserMedia permission WebRTC Leak");
pc.createOffer().then(offer => pc.setLocalDescription(offer))
pc.onicecandidate = event => {
    if (event.candidate) {
        var cdte = event.candidate.candidate;
        if (cdte !== "") {console.log(cdte);}
    }
}
```

#### d. TURN server contact *with* getUserMedia()

```js
navigator.mediaDevices.enumerateDevices()
    .then(devices => {
        const cams = devices.filter(device => device.kind == "videoinput");
        const mics = devices.filter(device => device.kind == "audioinput");

        const constraints = { video: cams.length > 0, audio: mics.length > 0 };
        return navigator.mediaDevices.getUserMedia(constraints);
    })
    .then(function(stream) {
    var pc = new RTCPeerConnection({iceServers: [{
        urls: [ "turn:TURN_SERVER_IPv4_ADRESS:PORT"
          , "turn:[TURN_SERVER_IPv6_ADRESS]:PORT"
          , "turn:TURN_SERVER_DOMAIN_NAME:PORT" ],
        credential: "TURN_PASSWORD",
        username: "TURN_USERNAME" }]}, {optional: [{RtpDataChannels: true}]});
    pc.createDataChannel("TURN without getUserMedia permission WebRTC Leak");
    pc.createOffer().then(offer => pc.setLocalDescription(offer))
    pc.onicecandidate = event => {
        if (event.candidate) {
            var cdte = event.candidate.candidate;
            if (cdte !== "") {console.log(cdte);}
        }
    }
})
```

Additional information: 
 - https://www.webrtc-experiment.com/docs/rtc-datachannel-for-beginners.html, accessed: May 24, 2024.
 - https://developer.mozilla.org/en-US/docs/Web/API/RTCPeerConnection/icecandidate_event, accessed: May 24, 2024.
 - https://developer.mozilla.org/en-US/docs/Web/API/RTCIceServer/urls, accessed: May 24, 2024.


## References

[[1](#2-information-about-the-scripts-used-on-the-web-page)] Mozilla, *MediaDevices: getUserMedia() method*, MDN Web Docs. Accessed: Feb. 22, 2024. [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia.  
[[2](#2-information-about-the-scripts-used-on-the-web-page)] S. Nandakumar, G. Salgueiro, P. Jones, and M. Petit-Huguenin, *URI Scheme for the Session Traversal Utilities for NAT (STUN) Protocol*, Internet Engineering Task Force, Request for Comments RFC 7064, Nov. 2013. doi: [10.17487/RFC7064](https://doi.org/10.17487/RFC7064).  
[[3](#2-information-about-the-scripts-used-on-the-web-page)] M. Petit-Huguenin, S. Nandakumar, G. Salgueiro, and P. Jones, *Traversal Using Relays around NAT (TURN) Uniform Resource Identifiers*, Internet Engineering Task Force, Request for Comments RFC 7065, Nov. 2013. doi: [10.17487/RFC7065](https://doi.org/10.17487/RFC7065).  
[[4](#2-information-about-the-scripts-used-on-the-web-page)] A. Reiter and A. Marsalek, *WebRTC: your privacy is at risk*, in Proceedings of the Symposium on Applied Computing, in SAC '17. New York, NY, USA: Association for Computing Machinery, Apr. 2017, pp. 664–669. doi: [10.1145/3019612.3019844](https://doi.org/10.1145/3019612.3019844).