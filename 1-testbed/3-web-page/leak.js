/*
Copyright (C) 2024 Guillaume Nibert <guillaume.nibert@snowpack.eu>,
                   Sébastien Tixeuil <sebastien.tixeuil@lip6.fr>,
                   Baptiste Polvé <baptiste.polve@snowpack.eu>,
                   Nana J. Bakalafoua M'boussi <nana.bakalafoua@snowpack.eu>,
                   Xuan Son Nguyen <xuanson.nguyen@snowpack.eu>

This file is part of WebRTC Leak Test

WebRTC Leak Test is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

WebRTC Leak Test is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with WebRTC Leak Test. If not, see <https://www.gnu.org/licenses/>.
*/

const gatherIceCandidates = (userConsent) => {
    return new Promise(async resolve => {

        // According to user's choice
        iceServersList = [{ urls: [defaultStunServerIPv4, defaultStunServerIPv6] }, { urls: [defaultTurnServerIPv4, defaultTurnServerIPv6], username: defaultTurnServerUsername, credential: defaultTurnServerCredential }];

        if ((stunServerSelected === false) && (turnServerSelected === false)) {
            iceServersList = [{ urls: [defaultStunServerIPv4, defaultStunServerIPv6] }, { urls: [defaultTurnServerIPv4, defaultTurnServerIPv6], username: defaultTurnServerUsername, credential: defaultTurnServerCredential }];
        }
        else if ((stunServerSelected === true) && (turnServerSelected === false)) {
            iceServersList = [{ urls: selectedStunAddress.value }, { urls: [defaultTurnServerIPv4, defaultTurnServerIPv6], username: defaultTurnServerUsername, credential: defaultTurnServerCredential }];
        }
        else if ((stunServerSelected === false) && (turnServerSelected === true)) {
            iceServersList = [{ urls: [defaultStunServerIPv4, defaultStunServerIPv6] }, { urls: selectedTurnAddress.value, username: selectedTurnUsername.value, credential: selectedTurnCredential.value }];
        }
        else {
            iceServersList = [{ urls: selectedStunAddress.value }, { urls: selectedTurnAddress.value, username: selectedTurnUsername.value, credential: selectedTurnCredential.value }];
        }

        async function createRTCPeerConnection(candidates) {
            // # Google STUN: stun:stun.l.google.com:19302
            // # turn:hostname:3478 idem for STUN (listening is addr et port transport)
            // # turn:hostanme:5349 (TLS) idem for STUN

            const rtc = new RTCPeerConnection({ iceServers: iceServersList }, { iceTransportPolicy : "all" }, { optional: [{ RtpDataChannels: true }] });

            rtc.createDataChannel("");
            const offer = await rtc.createOffer();
            await rtc.setLocalDescription(offer);

            const id = setTimeout(() => {
                rtc.onicecandidate = null;
                resolve(candidates);
            }, 10000);

            rtc.onicecandidate = (event) => {
                if (!event.candidate) {
                    resolve(candidates);
                    return clearTimeout(id);
                }
                else {
                    if (event.candidate.candidate != "") {
                        // RTCIceCandidate properties
                        // cf. https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate
                        var cdte = event.candidate.candidate;

                        console.log(cdte);

                        var cdteFirsPartArray = cdteFirstPartRegex.exec(cdte);

                        var foundationStr = cdteFirsPartArray[1];
                        var componentStr = cdteFirsPartArray[2];
                        var rtprtcpCandidateStr = "";

                        if (componentStr === "1") {
                            rtprtcpCandidateStr = "RTP";
                        }
                        else if (componentStr === "2") {
                            rtprtcpCandidateStr = "RTCP";
                        }

                        var transProtocolStr = cdteFirsPartArray[3].toUpperCase();
                        var priorityStr = cdteFirsPartArray[4]; //idem

                        var addressStr = addrRegex.exec(cdte)[0];

                        var hostnameIPprotocolStr = "";

                        if (ipv4Regex.test(addressStr) == true) { hostnameIPprotocolStr = "IPv4"; }
                        else if (ipv6Regex.test(addressStr) == true) { hostnameIPprotocolStr = "IPv6"; }
                        else if (mdnsRegex.test(addressStr) == true) { hostnameIPprotocolStr = "mDNS"; }

                        var portStr = portRegex.exec(cdte)[1];

                        var candidateTypeStr = candTypeRegex.exec(cdte)[0];

                        var raddrStr = "-";
                        var rportStr = "-";

                        if (candidateTypeStr != "host") {
                            raddrStr = relatedAddrRegex.exec(cdte)[1]; // 1 for the first capturing group
                            rportStr = relatedPortRegex.exec(cdte)[1]; // idem
                        }

                        var tcptypeStr = "-"

                        if (transProtocolStr === "TCP") {
                            tcptypeStr = tcptypeRegex.exec(cdte)[1]
                        }

                        var privPubStr = "";

                        if (hostnameIPprotocolStr === "mDNS") {
                            privPubStr = "Protected";
                        }
                        else {
                            if (privIpAddrRegex.test(addressStr) == true) {privPubStr = "Private";}
                            else {privPubStr = "Public";}
                        }

                        if (foundationStr.length < 4) { foundationStr = "NS*"; }
                        candidates.push({
                            foundation: foundationStr,
                            rtprtcpCandidate: rtprtcpCandidateStr,
                            transProtocol: transProtocolStr,
                            priority: priorityStr,
                            address: addressStr,
                            hostnameIPprotocol: hostnameIPprotocolStr,
                            port: portStr,
                            candidateType: candidateTypeStr,
                            raddr: raddrStr,
                            rport: rportStr,
                            tcptype: tcptypeStr,
                            privPub: privPubStr,
                            candidateRaw: cdte,
                        });
                    }
                }
            };
        }


        // REGEXES
        // navigator.mediaDevices.getUserMedia({ video: true, audio: true}).then(async function(stream) {
        // ex: candidate:11 1 UDP 1561861 ->
        //
        // foundation: 11, group 1
        // component: 1, group 2
        // transport: UDP, group 3
        // priority: 1561861, group 4
        var cdteFirstPartRegex = /candidate:(\d+)\s(1|2)\s(udp|tcp|UDP|TCP)\s(\d+)\s/

        // group 1
        // var addrRegex = /((((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4})|([a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})|(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.local))/;
        var addrRegex = /((((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4})|(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))|(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.local))/;
        var ipv4Regex = /((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}/;
        //var ipv6Regex = /([a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/;
        var ipv6Regex = /(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))/;
        var mdnsRegex = /(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.local)/;
        var privIpAddrRegex = /(^127\.)|(^192\.168\.)|(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^::1$)|(^[fF][cCdD])/;

        // group 1
        var portRegex = /([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])\styp/;

        // match 0
        var candTypeRegex = /(host|srflx|prflx|relay)/;

        // group 1
        //var relatedAddrRegex = /raddr\s((((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4})|([a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})|(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.local))/;
        var relatedAddrRegex = /raddr\s((((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4})|(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))|(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.local))/;
        // group 1
        var relatedPortRegex = /rport\s(\d{1,5})/;
        // group 1
        var tcptypeRegex = /tcptype\s(active|passive|so)/;

        let candidates = [];

        if (userConsent) {
            navigator.mediaDevices.getUserMedia({ video: true, audio: true }).then(async function (stream) {
                createRTCPeerConnection(candidates);
            });
        }
        else {
            createRTCPeerConnection(candidates);
        }
    });
}

async function gatherIceCandidatesExec() {
    var gatherCandidateButton = document.getElementById('gatherCandidateButton');

    gatherCandidateButton.disabled = true;
    gatherCandidateButton.innerHTML = `<span class="spinner-grow" style="width: 1.2rem; height: 1.2rem; margin-right: 10px" role="status" aria-hidden="true"></span>
    Gathering ICE candidates...`;

    tableData.candidates = await gatherIceCandidates(userMediaPermission);

    minDetails();
    moreDetails();
    fullDetails();
    rawInfo();

    gatherCandidateButton.disabled = false;
    gatherCandidateButton.innerHTML = `Gather ICE candidates`;
}

function minDetails() {

    if (document.getElementById("minDetailsTable")) {
        document.getElementById("minDetailsTable").remove();
    }

    var divMinDetails = document.getElementById('minDetails');

    let tbl = document.createElement("table");
    tbl.setAttribute("id", "minDetailsTable");
    tbl.classList.add('table');
    tbl.classList.add('table-hover');
    tbl.classList.add('table-striped');
    const tblBody = document.createElement("tbody");


    let row = tbl.insertRow();
    row.innerHTML = `<th scope="col">Private | Protected<sup>1</sup> | Public</th>
    <th scope="col">Resolution | IP protocol</th>
    <th scope="col">Hostname | IP address</th>`;

    var addresses = {};

    for (let i = 0; i < tableData.candidates.length; ++i) {
        addresses[tableData.candidates[i].address] = [tableData.candidates[i].hostnameIPprotocol, tableData.candidates[i].privPub]
    }

    for (var address in addresses) {
        let row = tbl.insertRow();
        for (let j = 0; j < 3; ++j) {
            let cell = row.insertCell();
            if (j === 0) { cell.textContent = addresses[address][1]; } // public/private
            else if (j === 1) { cell.textContent = addresses[address][0]; }
            else if (j === 2) { cell.textContent = address; }
        }
    }

    // put the <tbody> in the <table>
    tbl.appendChild(tblBody);
    // appends <table> into <body>

    if (document.getElementById("minDetailsCardBody")) {
        document.getElementById("minDetailsCardBody").remove();
    }

    var divMinDetailsCardBody = document.createElement("div");
    divMinDetailsCardBody.setAttribute("id", "minDetailsCardBody");
    divMinDetailsCardBody.classList.add('card');
    divMinDetailsCardBody.classList.add('card-body');
    divMinDetailsCardBody.innerHTML = `<p>Adresses that have been gathered:</p>`;

    let footnotes = document.createElement("p");
    footnotes.innerHTML=`<p align="left" style="margin: 0; padding: 0;"><sup>1</sup> When the address is a hostname only
     resolvable by <a href="https://datatracker.ietf.org/doc/html/rfc6762" target="_blank" 
     title="RFC 6762">mDNS</a>; see Internet Draft: Fablet et al., <i>Using Multicast DNS to protect privacy when 
     exposing ICE candidates</i>, IETF, December 5, 2021: <a 
     href="https://datatracker.ietf.org/doc/html/draft-ietf-mmusic-mdns-ice-candidates-03" 
     target="_blank">draft-ietf-mmusic-mdns-ice-candidates-03</a>.</p>`;

    divMinDetailsCardBody.appendChild(tbl);
    divMinDetailsCardBody.appendChild(footnotes);
    divMinDetails.append(divMinDetailsCardBody);
}


function moreDetails() {

    if (document.getElementById("moreDetailsTable")) {
        document.getElementById("moreDetailsTable").remove();
    }

    var divMoreDetails = document.getElementById('moreDetails');
    
    // creates a <table> element and a <tbody> element

    let tbl = document.createElement("table");
    tbl.setAttribute("id", "moreDetailsTable");
    tbl.classList.add('table');
    tbl.classList.add('table-hover');
    tbl.classList.add('table-striped');
    const tblBody = document.createElement("tbody");


    let row = tbl.insertRow();
    row.innerHTML = `<th scope="col">#</th>
    <th scope="col">Candidate type<sup>1</sup></th>
    <th scope="col">Private | Protected<sup>2</sup> | Public</th>
    <th scope="col">Resolution | IP protocol</th>
    <th scope="col">Hostname | IP address</th>
    <th scope="col">Port</th>
    <th scope="col">Transport protocol</th>
    <th scope="col">Related address<sup>3</sup></th>
    <th scope="col">Related port<sup>4</sup></th>`;

    for (let i = 0; i < tableData.candidates.length; ++i) {
        let row = tbl.insertRow();
        for (let j = 0; j < 9; ++j) {
            let cell = row.insertCell();
            if (j === 0) { row.innerHTML = `<th scope="row">${i + 1}</th>`; }
            else if (j === 1) { cell.textContent = tableData.candidates[i].candidateType; }
            else if (j === 2) { cell.textContent = tableData.candidates[i].privPub; }
            else if (j === 3) { cell.textContent = tableData.candidates[i].hostnameIPprotocol; }
            else if (j === 4) { cell.textContent = tableData.candidates[i].address; }
            else if (j === 5) { cell.textContent = tableData.candidates[i].port; }
            else if (j === 6) { cell.textContent = tableData.candidates[i].transProtocol; }
            else if (j === 7) { cell.textContent = tableData.candidates[i].raddr; }
            else if (j === 8) { cell.textContent = tableData.candidates[i].rport; }
        }
    }

    // put the <tbody> in the <table>
    tbl.appendChild(tblBody);
    // appends <table> into <body>

    if (document.getElementById("moreDetailsCardBody")) {
        document.getElementById("moreDetailsCardBody").remove();
    }

    var divMoreDetailsCardBody = document.createElement("div");
    divMoreDetailsCardBody.setAttribute("id", "moreDetailsCardBody");
    divMoreDetailsCardBody.classList.add('card');
    divMoreDetailsCardBody.classList.add('card-body');
    divMoreDetailsCardBody.innerHTML = `<p>ICE candidates that have been gathered:</p>`;

    let footnotes = document.createElement("p");
    footnotes.innerHTML=`<p align="left" style="margin: 0; padding: 0;">
    <sup>1</sup> Possible values: <code>host</code> | <code>srflx</code> | <code>prflx</code> | <code>relay</code>; 
    more information at: <a href="https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/type" target="_blank"
     title="RTCIceCandidate: type property">https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/type</a>.
    <br>
    <sup>2</sup> When the address is a hostname only
    resolvable by <a href="https://datatracker.ietf.org/doc/html/rfc6762" target="_blank" 
    title="RFC 6762">mDNS</a>; see Internet Draft: Fablet et al., <i>Using Multicast DNS to protect privacy when 
    exposing ICE candidates</i>, IETF, December 5, 2021: <a 
    href="https://datatracker.ietf.org/doc/html/draft-ietf-mmusic-mdns-ice-candidates-03" 
    target="_blank">draft-ietf-mmusic-mdns-ice-candidates-03</a>.
    <br>
    <sup>3</sup> Reflexive or relay address, more information at: 
    <a href="https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/relatedAddress" target="_blank" 
    title="RTCIceCandidate: relatedAddress property">https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/relatedAddress</a>.
    <br>
    <sup>4</sup> Reflexive or relay port, more information at: 
    <a href="https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/relatedPort" target="_blank" 
    title="RTCIceCandidate: relatedPort property">https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/relatedPort</a>.
    <br></p>`;

    divMoreDetailsCardBody.appendChild(tbl);
    divMoreDetailsCardBody.appendChild(footnotes);
    divMoreDetails.append(divMoreDetailsCardBody);
}


function fullDetails() {

    if (document.getElementById("fullDetailsTable")) {
        document.getElementById("fullDetailsTable").remove();
    }

    var divFullDetails = document.getElementById('fullDetails');
    // creates a <table> element and a <tbody> element

    let tbl = document.createElement("table");
    tbl.setAttribute("id", "fullDetailsTable");
    tbl.classList.add('table');
    tbl.classList.add('table-hover');
    tbl.classList.add('table-striped');
    const tblBody = document.createElement("tbody");


    let row = tbl.insertRow();
    row.innerHTML = `<th scope="col">#</th>
    <th scope="col">Candidate type<sup>1</sup></th>
    <th scope="col">Private Protected<sup>2</sup> Public</th>
    <th scope="col">Resolution / IP protocol</th>
    <th scope="col">Hostname / IP address</th>
    <th scope="col">Port</th>
    <th scope="col">Transport protocol</th>
    <th scope="col">TCP Type<sup>3</sup></th>
    <th scope="col">Related address<sup>4</sup></th>
    <th scope="col">Related port<sup>5</sup></th>
    <th scope="col">Priority<sup>6</sup></th>
    <th scope="col">Foundation<sup>7</sup></th>
    <th scope="col">Component<sup>8</sup></th>`;

    for (let i = 0; i < tableData.candidates.length; ++i) {
        let row = tbl.insertRow();
        for (let j = 0; j < 13; ++j) {
            let cell = row.insertCell();
            if (j === 0) { row.innerHTML = `<th scope="row">${i + 1}</th>`; }
            else if (j === 1) { cell.textContent = tableData.candidates[i].candidateType; }
            else if (j === 2) { cell.textContent = tableData.candidates[i].privPub; }
            else if (j === 3) { cell.textContent = tableData.candidates[i].hostnameIPprotocol; }
            else if (j === 4) { cell.textContent = tableData.candidates[i].address; }
            else if (j === 5) { cell.textContent = tableData.candidates[i].port; }
            else if (j === 6) { cell.textContent = tableData.candidates[i].transProtocol; }
            else if (j === 7) { cell.textContent = tableData.candidates[i].tcptype; }
            else if (j === 8) { cell.textContent = tableData.candidates[i].raddr; }
            else if (j === 9) { cell.textContent = tableData.candidates[i].rport; }
            else if (j === 10) { cell.textContent = tableData.candidates[i].priority; }
            else if (j === 11) { cell.textContent = tableData.candidates[i].foundation; }
            else if (j === 12) { cell.textContent = tableData.candidates[i].rtprtcpCandidate; }
        }
    }

    // put the <tbody> in the <table>
    tbl.appendChild(tblBody);
    // appends <table> into <body>

    if (document.getElementById("fullDetailsCardBody")) {
        document.getElementById("fullDetailsCardBody").remove();
    }

    var divFullDetailsCardBody = document.createElement("div");
    divFullDetailsCardBody.setAttribute("id", "fullDetailsCardBody");
    divFullDetailsCardBody.classList.add('card');
    divFullDetailsCardBody.classList.add('card-body');
    divFullDetailsCardBody.innerHTML = `<p>ICE candidates that have been gathered:</p>`;

    let footnotes = document.createElement("p");
    footnotes.innerHTML=`<p align="left" style="margin: 0; padding: 0;">
    <sup>1</sup> Possible values: <code>host</code> | <code>srflx</code> | <code>prflx</code> | <code>relay</code>; 
    more information at: <a href="https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/type" target="_blank"
     title="RTCIceCandidate: type property">https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/type</a>.
    <br>
    <sup>2</sup> When the address is a hostname only
    resolvable by <a href="https://datatracker.ietf.org/doc/html/rfc6762" target="_blank" 
    title="RFC 6762">mDNS</a>; see Internet Draft: Fablet et al., <i>Using Multicast DNS to protect privacy when 
    exposing ICE candidates</i>, IETF, December 5, 2021: <a 
    href="https://datatracker.ietf.org/doc/html/draft-ietf-mmusic-mdns-ice-candidates-03" 
    target="_blank">draft-ietf-mmusic-mdns-ice-candidates-03</a>.
    <br>
    <sup>3</sup> Possible values: <code>"active"</code> | <code>"passive"</code> | <code>"so"</code> | 
    <code>null</code>; more information at: <a 
    href="https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/tcpType" target="_blank" 
    title="RTCIceCandidate: tcpType property">https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/tcpType</a>.
    <br>
    <sup>4</sup> Reflexive or relay address, more information at: 
    <a href="https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/relatedAddress" target="_blank" 
    title="RTCIceCandidate: relatedAddress property">https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/relatedAddress</a>.
    <br>
    <sup>5</sup> Reflexive or relay port, more information at: 
    <a href="https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/relatedPort" target="_blank" 
    title="RTCIceCandidate: relatedPort property">https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/relatedPort</a>.
    <br>
    <sup>6</sup> Candidate priority, more information at: 
    <a href="https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/priority" target="_blank" 
    title="RTCIceCandidate: priority property">https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/priority</a>.
    <br>
    <sup>7</sup> String that uniquely identify the ICE candidate (not supported on Firefox), more information at: 
    <a href="https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/foundation" target="_blank" 
    title="RTCIceCandidate: foundation property">https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/foundation</a>.
    <br>
    <sup>8</sup> <a href="https://datatracker.ietf.org/doc/html/rfc3550" target="_blank" title="RFC 3550">RTP</a> 
    or <a href="https://datatracker.ietf.org/doc/html/rfc3550#page-19" target="_blank" title="RFC 3550">RTCP</a> 
    candidate (if both, the component property is RTP), more information at: 
    <a href="https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/component" target="_blank" 
    title="RTCIceCandidate: component property">https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/component</a>.
    </p><br>
    <p align="left" style="margin: 0; padding: 0;">* NS : Not supported.</p>`;

    divFullDetailsCardBody.appendChild(tbl);
    divFullDetailsCardBody.appendChild(footnotes);
    divFullDetails.append(divFullDetailsCardBody);

}


function rawInfo() {

    if (document.getElementById("rawInfoPar")) {
        document.getElementById("rawInfoPar").remove();
    }

    var divRawInfo = document.getElementById('rawInfo');
    // creates a <table> element and a <tbody> element

    let paragraph = document.createElement("p");
    paragraph.setAttribute("id", "rawInfoPar");

    for (let i = 0; i < tableData.candidates.length; ++i) {
        paragraph.innerHTML+=`<code>${tableData.candidates[i].candidateRaw}</code><br>`
    }

    // appends <table> into <body>
    //div.appendChild(paragraph);

    if (document.getElementById("rawInfoCardBody")) {
        document.getElementById("rawInfoCardBody").remove();
    }

    var divRawInfoCardBody = document.createElement("div");
    divRawInfoCardBody.setAttribute("id", "rawInfoCardBody");
    divRawInfoCardBody.classList.add('card');
    divRawInfoCardBody.classList.add('card-body');
    divRawInfoCardBody.innerHTML = `<p>ICE candidates that have been gathered:</p>`;

    let footnotes = document.createElement("p");
    footnotes.innerHTML=`<p align="left" style="margin: 0; padding: 0;">
    Candidate property: 
    <a href="https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/candidate" target="_blank" 
    title="RTCIceCandidate: candidate property">https://developer.mozilla.org/en-US/docs/Web/API/RTCIceCandidate/candidate</a></p>`;

    divRawInfoCardBody.appendChild(paragraph);
    divRawInfoCardBody.appendChild(footnotes);
    divRawInfo.append(divRawInfoCardBody);
}


function displayStunTurnServer(stunServerAddr, turnServerAddr) {
    var div = document.getElementById("server-used");
    var text = document.createElement("p");
    var stunServerValue = "";
    var turnServerValue = "";

    if (stunServerAddr != "") {stunServerValue = stunServerAddr;} else { stunServerValue = "no STUN server specified"}
    if (turnServerAddr != "") {turnServerValue = turnServerAddr;} else { turnServerValue = "no TURN server specified"}

    text.innerHTML=`STUN server used: <b>${stunServerValue}</b> | TURN server used: <b>${turnServerValue}</b>.<br>
    Feel free to set other servers (<code>stunServer</code> and <code>turnServer</code> variables in the <b>leak.js</b> file).`;
    div.appendChild(text);
}


let tableData = { candidates: [] };
var userMediaPermission = false;

$('#getUserMediaPermission').on('change', function () {
    userMediaPermission = $(this).is(':checked');
});


// STUN server selection
var stunServerSelected = false;
var stunButtonClics = 0;
var defaultStunServerIPv4 = "stun:192.0.2.1:5349";
var defaultStunServerIPv6 = "stun:[2001:db8::1]:5349";
var selectedStunAddress = document.getElementById('selected-stun-address');
var selectStunButton = document.getElementById('select-stun-button');
var outputStunAddress = document.getElementById('current-stun-server-output')

function getStunServer() {
    if ((stunButtonClics < 1) && (selectedStunAddress.value === "")) {
        outputStunAddress.innerHTML = "<p>STUN default IPv4 server: <b>" + defaultStunServerIPv4 + "</b><br>STUN default IPv6 server: <b>" + defaultStunServerIPv6 + "</b></p>";
    }
    else if ((stunButtonClics > 1) && (selectedStunAddress.value === "")) {
        outputStunAddress.innerHTML = "<p>STUN default IPv4 server: <b>" + defaultStunServerIPv4 + "</b><br>STUN default IPv6 server: <b>" + defaultStunServerIPv6 + "</b></p>";
        stunServerSelected = false;
    }
    else {
        outputStunAddress.innerHTML = "<p>STUN selected server: <b>" + selectedStunAddress.value + "</b></p>";
        stunServerSelected = true;
    }
    stunButtonClics += 1;
}

getStunServer();

selectStunButton.addEventListener('click', getStunServer);


// TURN Server selection
var turnServerSelected = false;
var turnButtonClics = 0;
var defaultTurnServerIPv4 = "turn:192.0.2.1:5349";
var defaultTurnServerIPv6 = "turn:[2001:db8::1]:5349";
var defaultTurnServerUsername = "TURN_USERNAME";
var defaultTurnServerCredential = "TURN_PASSWORD";
var selectedTurnAddress = document.getElementById('selected-turn-address');
var selectedTurnUsername = document.getElementById('selected-turn-username');
var selectedTurnCredential = document.getElementById('selected-turn-credential');

var selectTurnButton = document.getElementById('select-turn-button');
var outputTurnAddress = document.getElementById('current-turn-server-output');

function getTurnServer() {
    if ((turnButtonClics < 1) && ((selectedTurnAddress.value === "") || (selectedTurnUsername.value === "") || (selectedTurnCredential.value === ""))) {
        outputTurnAddress.innerHTML = "<p>TURN default IPv4 server: <b>" + defaultTurnServerIPv4 + " [" + defaultTurnServerUsername+ ":" + defaultTurnServerCredential + "]</b><br>TURN default IPv6 server: <b>" + defaultTurnServerIPv6 + " [" + defaultTurnServerUsername + ":" + defaultTurnServerCredential + "]</b></p>";
    }
    else if ((turnButtonClics >= 1) && ((selectedTurnAddress.value === "") || (selectedTurnUsername.value === "") || (selectedTurnCredential.value === ""))) {
        outputTurnAddress.innerHTML = "<p>Please fill all fields!<br><br>TURN default IPv4 server: <b>" + defaultTurnServerIPv4 + " [" + defaultTurnServerUsername+ ":" + defaultTurnServerCredential + "]</b><br>TURN default IPv6 server: <b>" + defaultTurnServerIPv6 + " [" + defaultTurnServerUsername + ":" + defaultTurnServerCredential + "]</b></p>";
        turnServerSelected = false;
    }
    else {
        outputTurnAddress.innerHTML = "<p>TURN selected server: <b>" + selectedTurnAddress.value + " [" + selectedTurnUsername.value + ":" + selectedTurnCredential.value + "]</b></p>";
        turnServerSelected = true;
    }
    turnButtonClics += 1;
}

getTurnServer();

selectTurnButton.addEventListener('click', getTurnServer);