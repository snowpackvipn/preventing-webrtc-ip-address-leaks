<small><i>This README is a copy of [subsection 4.2 - Compromised Firefox web browser](../../README.md#43-compromised-firefox-web-browser) from the `1-testbed/README.md` file.</i></small>


## Table of contents

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.3. Compromised Firefox web browser](#43-compromised-firefox-web-browser)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.3.1. Threat model](#431-threat-model)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.3.2. Compromising tools](#432-compromising-tools)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.3.2.1. Compromised configuration used in our evaluation](#4321-compromised-configuration-used-in-our-evaluation)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.3.2.1.1. Host configuration](#43211-host-configuration)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.3.2.1.2. Containerised compromised web browser](#43212-containerised-compromised-web-browser)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.3.2.2. Other compromised configuration allowing the installation of extensions not signed by Mozilla [19]](#4322-other-compromised-configuration-allowing-the-installation-of-extensions-not-signed-by-mozilla-19)  
[References](#references)

### 4.3. Compromised Firefox web browser

#### 4.3.1. Threat model

The adversary is able to exploit any vulnerability in Firefox to force it to operate in the most unfavourable WebRTC mode, or even to modify the WebRTC implementation maliciously (e.g. mode 1 always used regardless of the user's consent). The adversary's capabilities are limited to compromise the browser. The WebRTC client is corrupted and is unaware of it.

Our compromised browser is forced to run only in a mode where WebRTC does not respect privacy: no mDNS protection, even if the user does not give his consent, and link-local/loop-back IP addresses can be candidates (cf. [ subsection 4.3.2.1](#4321-compromised-configuration-used-in-our-evaluation)).

A post on the Mozilla Russia forum [[19](#references)] gives a way of authorising the installation of extensions not signed by Mozilla. All that needs to be done is to create an executable script and have the user download it (cf. [subsection 4.3.2.2](#4322-other-compromised-configuration-allowing-the-installation-of-extensions-not-signed-by-mozilla-19)). This compromised Firefox browser version is not included in our evaluation.

#### 4.3.2. Compromising tools

<small><i>The bash scripts and paths presented in this subsection are only valid for Ubuntu. This has been tested with **Ubuntu 22.04 LTS** with the **.deb version** of Firefox [[18](#references)]. If you wish to compromise your Firefox web browser on **Windows** or **macOS**, the only Firefox configuration files to overwrite are ***config.js*** and **config-prefs.js**. Refer to this GitHub issue to find out where the paths to these configuration files can be found: https://github.com/xiaoxiaoflood/firefox-scripts/issues/8 [Accessed: Feb. 26, 2024].</i></small>

##### 4.3.2.1. Compromised configuration used in our evaluation

###### 4.3.2.1.1. Host configuration

The configuration used in our host system evaluation can be done by modifying/creating theses two files:

***config-prefs.js***

```javascript
pref("general.config.obscure_value", 0);
pref("general.config.filename", "config.js");
pref("general.config.sandbox_enabled", false);
```

***config.js***

```javascript
lockPref("media.peerconnection.ice.obfuscate_host_addresses", false);
lockPref("media.peerconnection.ice.proxy_only", false);
lockPref("media.peerconnection.ice.link_local", true);
lockPref("media.peerconnection.ice.loopback", true);
lockPref("media.peerconnection.ice.proxy_only_if_behind_proxy", false);
lockPref("media.peerconnection.ice.relay_only", false);
lockPref("media.peerconnection.ice.force_interface", true);
lockPref("media.peerconnection.ice.relay_only", false);
lockPref("media.peerconnection.use_document_iceservers", true);
lockPref("media.peerconnection.ice.default_address_only", false);
lockPref("media.peerconnection.ice.no_host", false);
lockPref("media.peerconnection.enabled", true);
lockPref("media.peerconnection.ice.tcp", true);
lockPref("media.peerconnection.identity.enabled", true);
lockPref("media.peerconnection.turn.disable", false);
lockPref("media.peerconnection.allow_old_setParameters", true);
```

To automatically achieve this configuration on Ubuntu, go to the [`1-compromising-firefox-evaluation-version`](1-compromising-firefox-evaluation-version) folder, open the [`index.html`](1-compromising-firefox-evaluation-version/index.html) page and follow the instructions on that page.


###### 4.3.2.1.2. Containerised compromised web browser

This compromising configuration is also included in the containerised version of the compromised Firefox web browser for all types of host OS (Linux, Windows, macOS).

To use them, simply use the *docker compose files* containing the word ***"compromised"***, e.g. for the ***Linux Wayland version***: 

```bash
UID=${UID} GID=${GID} docker compose -f ./docker-compose-compromised-firefox-wayland-linux.yml up
```

For more information on the Firefox containerised browser, please read [section 3 - Run the containerised web browser solution of the `1-testbed/README.md`](../README.md#3-run-the-containerised-web-browser-solution).


##### 4.3.2.2. Other compromised configuration allowing the installation of extensions not signed by Mozilla [[19](#references)]

This section is provided for information purposes only, to show that there are other ways of compromising the browser. For example by using the configuration provided by banbot [[19](#references)] which allows the installation of extensions not signed by Mozilla:

***config-prefs.js*** - Firefox v102+, author: banbot [[19](#references)]

```javascript
try {(jsval => {
	var dbg, gref, genv = func => {
		var sandbox = new Cu.Sandbox(g, {freshCompartment: true});
		Cc["@mozilla.org/jsdebugger;1"].createInstance(Ci.IJSDebugger).addClass(sandbox);
		(dbg = new sandbox.Debugger()).addDebuggee(g);
		gref = dbg.makeGlobalObjectReference(g);
		return (genv = func => func && gref.makeDebuggeeValue(func).environment)(func);
	}
	var g = Cu.getGlobalForObject(jsval), o = g.Object, {freeze} = o, disleg;

	var AC = "AppConstants", uac = `resource://gre/modules/${AC}.`;
	var lexp = () => lockPref("extensions.experiments.enabled", true);
	if (o.isFrozen(o)) { // Fx 102.0b7+
		lexp(); disleg = true;
		var env, def = g.ChromeUtils.defineModuleGetter;
		g.ChromeUtils.defineModuleGetter = (...args) => {
			try {
				genv();
				dbg.addDebuggee(globalThis);
				var e = dbg.getNewestFrame().older.environment;
				var obj = e.parent.type == "object" && e.parent.object;
				if (obj && obj.class.startsWith("N")) // JSM, NSVO
					obj.unsafeDereference().Object = {
						freeze: ac => (ac.MOZ_REQUIRE_SIGNING = false) || freeze(ac)
					};
				else env = e; // ESM, Lexy "var"(?)
			}
			catch(ex) {Cu.reportError(ex);}
			(g.ChromeUtils.defineModuleGetter = def)(...args);
		}
		ChromeUtils.import(uac + "jsm");
		// (?)
		env && env.setVariable(AC, gref.makeDebuggeeValue(freeze(o.assign(
			new o(), env.getVariable(AC).unsafeDereference(), {MOZ_REQUIRE_SIGNING: false}
		))));
	}
	else o.freeze = obj => {
		if (!Components.stack.caller.filename.startsWith(uac)) return freeze(obj);
		obj.MOZ_REQUIRE_SIGNING = false;

		if ((disleg = "MOZ_ALLOW_ADDON_SIDELOAD" in obj)) lexp();
		else
			obj.MOZ_ALLOW_LEGACY_EXTENSIONS = true,
			lockPref("extensions.legacy.enabled", true);

		return (o.freeze = freeze)(obj);
	}
	lockPref("xpinstall.signatures.required", false);
	lockPref("extensions.langpacks.signatures.required", false);

	var useDbg = true, xpii = "resource://gre/modules/addons/XPIInstall.jsm";
	if (Ci.nsINativeFileWatcherService) { // Fx < 100
		jsval = Cu.import(xpii, {});
		var shouldVerify = jsval.shouldVerifySignedState;
		if (shouldVerify.length == 1)
			useDbg = false,
			jsval.shouldVerifySignedState = addon => !addon.id && shouldVerify(addon);
	}
	if (useDbg) {
		jsval = g.ChromeUtils.import(xpii);

		var env = genv(jsval.XPIInstall.installTemporaryAddon);
		var ref = name => {try {return env.find(name).getVariable(name).unsafeDereference();} catch {}}
		jsval.XPIDatabase = (ref("lazy") || {}).XPIDatabase || ref("XPIDatabase");

		var proto = ref("Package").prototype;
		var verify = proto.verifySignedState;
		proto.verifySignedState = function(id) {
			return id ? {cert: null, signedState: undefined} : verify.apply(this, arguments);
		}
		dbg.removeAllDebuggees();
	}
	if (disleg) jsval.XPIDatabase.isDisabledLegacy = () => false;
})(
	"permitCPOWsInScope" in Cu ? Cu.import("resource://gre/modules/WebRequestCommon.jsm", {}) : Cu
);}
catch(ex) {Cu.reportError(ex);}
```

To compromise your Firefox web browser automatically on Ubuntu, go to the [`2-compromising-firefox-unsigned-extensions-version`](2-compromising-firefox-unsigned-extensions-version) folder, open the [`index.html`](2-compromising-firefox-unsigned-extensions-version/index.html) page and follow the instructions on that page. The page will ask you in this order:
1. to compromise Firefox using the a compromising script (located in the folder), then
2. to install an extension whose official purpose is to disable WebRTC and whose **hidden purpose** is to **leave WebRTC enabled** (and therefore vulnerable to the WebRTC IP address leakage).

## References


[[18](#43-compromised-firefox-web-browser)] A. Wyman et al., *Install Firefox .deb package for Debian-based distributions* **In**: *Install Firefox on Linux*, Mozilla Support. Accessed: May 24, 2024. [Online]. Available: https://support.mozilla.org/en-US/kb/install-firefox-linux#w_install-firefox-deb-package-for-debian-based-distributions.  
[[19](#431-threat-model)] banbot, *Как отключить проверку цифровых подписей в дополнениях Firefox [How to disable digital signature verification in Firefox add-ons]*, Forum Mozilla Russia. Accessed: Feb. 26, 2024. [Online]. Available: https://forum.mozilla-russia.org/viewtopic.php?id=70326.