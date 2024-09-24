function stun_without_getusermedia() {
    let candidateDiv = document.createElement('div');
    candidateDiv.id = "ice_candidates";

    var pc = new RTCPeerConnection({iceServers: [{urls: ["stun:192.0.2.1:5349", "stun:[2001:db8::1]:5349"]}]}, {optional: [{RtpDataChannels: true}]});
    pc.createDataChannel("STUN with getUserMedia permission WebRTC Leak");
    pc.createOffer().then(offer => pc.setLocalDescription(offer));
    pc.onicecandidate = event => {
        if (event.candidate) {
            var cdte = event.candidate.candidate;
            if (cdte !== "") {
                candidateDiv.textContent += cdte + ','; // Append cdte to the div element
            }
        }
    }
    document.body.appendChild(candidateDiv); // Add the div element to the page
}


function stun_with_getusermedia() {
    let candidateDiv = document.createElement('div');
    candidateDiv.id = "ice_candidates";

    navigator.mediaDevices.enumerateDevices()
        .then(devices => {
            const cams = devices.filter(device => device.kind == "videoinput");
            const mics = devices.filter(device => device.kind == "audioinput");

            const constraints = { video: cams.length > 0, audio: mics.length > 0 };
            return navigator.mediaDevices.getUserMedia(constraints);
        })
        .then(function(stream) {
        var pc = new RTCPeerConnection({iceServers: [{urls: ["stun:192.0.2.1:5349", "stun:[2001:db8::1]:5349"]}]}, {optional: [{RtpDataChannels: true}]});
        pc.createDataChannel("STUN with getUserMedia permission WebRTC Leak");
        pc.createOffer().then(offer => pc.setLocalDescription(offer));

        pc.onicecandidate = event => {
            if (event.candidate) {
                var cdte = event.candidate.candidate;
                if (cdte !== "") {
                    candidateDiv.textContent += cdte + ','; // Append cdte to the div element
                }
            }
        }
        })
    document.body.appendChild(candidateDiv); // Add the div element to the page
}


function turn_without_getusermedia() {
    let candidateDiv = document.getElementById("ice_candidates");

    var pc = new RTCPeerConnection({iceServers: [{
        urls: ["turn:192.0.2.1:5349", "turn:[2001:db8::1]:5349"],
        credential: "TURN_PASSWORD",
        username: "TURN_USERNAME"
    }]}, {optional: [{RtpDataChannels: true}]});
    pc.createDataChannel("TURN without getUserMedia permission WebRTC Leak");
    pc.createOffer().then(offer => pc.setLocalDescription(offer))
    pc.onicecandidate = event => {
        if (event.candidate) {
            var cdte = event.candidate.candidate;
            if (cdte !== "") {
                candidateDiv.textContent += cdte + ','; // Append cdte to the div element
            }
        }
    }
    document.body.appendChild(candidateDiv); // Add the div element to the page
}


function turn_with_getusermedia() {
    let candidateDiv = document.getElementById("ice_candidates");

    navigator.mediaDevices.enumerateDevices()
        .then(devices => {
            const cams = devices.filter(device => device.kind == "videoinput");
            const mics = devices.filter(device => device.kind == "audioinput");

            const constraints = { video: cams.length > 0, audio: mics.length > 0 };
            return navigator.mediaDevices.getUserMedia(constraints);
        }).then(function(stream) {
        var pc = new RTCPeerConnection({iceServers: [{
            urls: ["turn:192.0.2.1:5349", "turn:[2001:db8::1]:5349"],
            credential: "TURN_PASSWORD",
            username: "TURN_USERNAME"
        }]}, {optional: [{RtpDataChannels: true}]});
        pc.createDataChannel("TURN with getUserMedia permission WebRTC Leak");
        pc.createOffer().then(offer => pc.setLocalDescription(offer))
        pc.onicecandidate = event => {
            if (event.candidate) {
                var cdte = event.candidate.candidate;
                if (cdte !== "") {
                    candidateDiv.textContent += cdte + ','; // Append cdte to the div element
                }
            }
        }
    })
    document.body.appendChild(candidateDiv); // Add the div element to the page
}