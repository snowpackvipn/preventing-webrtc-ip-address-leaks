#!/bin/bash

#title              :Force unsafe WebRTC enabled
#description        :This script will enable WebRTC in an unsecure way.
#bash script author :Guillaume Nibert <guillaume.nibert@snowpack.eu>
#date               :2023-04-21
#version            :0.0.1


sudo bash -c 'cat > /usr/lib/firefox/config.js <<EOL
// Force unsafe WebRTC enabled
lockPref("media.peerconnection.ice.obfuscate_host_addresses", false);
lockPref("media.peerconnection.ice.proxy_only", false);
lockPref("media.peerconnection.ice.link_local", true);
lockPref("media.peerconnection.ice.loopback", true);
lockPref("media.peerconnection.ice.proxy_only_if_behind_proxy", false);
lockPref("media.peerconnection.ice.force_interface", "");
lockPref("media.peerconnection.ice.relay_only", false);
lockPref("media.peerconnection.use_document_iceservers", true);
lockPref("media.peerconnection.ice.default_address_only", false);
lockPref("media.peerconnection.ice.no_host", false);
lockPref("media.peerconnection.enabled", true);
lockPref("media.peerconnection.ice.tcp", true);
lockPref("media.peerconnection.identity.enabled", true);
lockPref("media.peerconnection.turn.disable", false);
lockPref("media.peerconnection.allow_old_setParameters", true);
EOL

cat > /usr/lib/firefox/defaults/pref/config-prefs.js <<EOL
pref("general.config.obscure_value", 0);
pref("general.config.filename", "config.js");
pref("general.config.sandbox_enabled", false);
EOL'
