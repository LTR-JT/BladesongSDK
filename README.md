# Bladesong SDK

Independent developer SDK for [BladesongModFramework](https://github.com/LTR-JT/BladesongModFramework). SDK 1.0.1 targets API 1.0.0 and manifest schema 1. Developing and packaging mods requires no Mod Manager installation or source checkout.

SDK/ contains portable JSON schemas, Lua type definitions, stable API contracts and mod templates. Documentation/ and Examples/ cover runtime services, compatibility, authoring and publishing. Tools/ contains metadata validation and installer-independent package generation. No runtime or manager binary is included.

```powershell
python Tools/run_checks.py --lua C:/path/to/lua.exe
python Tools/validate_manifest.py SDK/templates/basic/mod.json
python Tools/package_mod.py SDK/templates/basic MyMod.zip
python Tools/package_release.py
python Tools/check_packages.py
```

Use `python Tools/generate_api.py --framework ../BladesongModFramework` for optional implementation validation. The ordinary checks are standalone. Install the framework in the game when running a developed mod; the optional manager is not required.

The published schema source is [SDK/mod.schema.json](https://github.com/LTR-JT/BladesongSDK/blob/main/SDK/mod.schema.json). [BladesongModManager](https://github.com/LTR-JT/BladesongModManager) is one optional client of the portable package format; future third-party adapters can reuse it. No Vortex integration is claimed.

Extracted from the existing framework project; see UPSTREAM.md for provenance. This is an unpublished split candidate. Releases are manual, independently versioned v-tags. MIT license.
