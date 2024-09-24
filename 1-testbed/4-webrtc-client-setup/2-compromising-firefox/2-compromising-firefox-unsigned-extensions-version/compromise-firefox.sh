#!/bin/bash

#title           		: Compromise Firefox
#description     		: This script will allow to install unsigned extensions for Firefox
#js script author		: banbot <https://forum.mozilla-russia.org/profile.php?id=21189>
#bash script author		: Guillaume Nibert <guillaume.nibert@snowpack.eu>
#date            		: 2023-04-21
#version         		: 0.0.1
#notes           		: Configuration from: https://forum.mozilla-russia.org/viewtopic.php?id=70326
#require         		: Firefox 102 and above.


sudo bash -c 'cat > /usr/lib/firefox/config.js <<EOL
//
try {(jsval => {
	var dbg, gref, genv = func => {
		var sandbox = new Cu.Sandbox(g, {freshCompartment: true});
		Cc["@mozilla.org/jsdebugger;1"].createInstance(Ci.IJSDebugger).addClass(sandbox);
		(dbg = new sandbox.Debugger()).addDebuggee(g);
		gref = dbg.makeGlobalObjectReference(g);
		return (genv = func => func && gref.makeDebuggeeValue(func).environment)(func);
	}
	var g = Cu.getGlobalForObject(jsval), o = g.Object, {freeze} = o, disleg;

	var AC = "AppConstants", uac = \`resource://gre/modules/\${AC}.\`;
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
EOL

cat > /usr/lib/firefox/defaults/pref/config-prefs.js <<EOL
pref("general.config.obscure_value", 0);
pref("general.config.filename", "config.js");
pref("general.config.sandbox_enabled", false);
EOL'
