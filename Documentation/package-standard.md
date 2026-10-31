# Portable mod packages and metadata

Schema v1 remains additive. The published JSON Schema source is `SDK/mod.schema.json` (legacy alias: `SDK/bmf-manifest.schema.json`). Validate with `python Tools/validate_manifest.py path/to/mod.json`. The bundled validator implements the keywords used by this schema; it is not a general JSON Schema engine.

Keep stable IDs: `BladesongModFramework`, `BladesongModManager`, `PreconstructionLibraryProbe`. Renaming IDs would duplicate installations and break dependencies. `api` is the SDK API range, while `version` is the mod/runtime package version. Required and optional dependencies use existing `{id: version_range}` objects. `dependency_sources` supplies HTTPS repository or release-manifest URLs for dependencies that discovery cannot identify. Optional dependencies are described but never installed automatically.

`release_source` describes a GitHub repository and optional tag, tag_prefix and manifest_asset. An ordinary mod's repository publishes its own `mod.json` asset plus a release archive. An index entry remains only `{name,url}` and is not a runtime requirement. The optional manager has its own LTR-JT/BladesongModManager repository, v-tags and mod.json release assets. Framework releases remain in LTR-JT/BladesongModFramework. Component updates filter release tags by tag_prefix rather than assuming that the repository-wide latest release belongs to that component.

`package: {format: "bladesong-mod-1", target: "ue4ss-mods"}` identifies a portable root-manifest archive. `runtime_components: {UE4SS: "*"}` describes the loader requirement separately. `download` contains the HTTPS archive URL and SHA-256. `files` lists every payload path, byte size and SHA-256. The root `mod.json` describes the archive and is not itself a payload file.

All managers use these fixed installation mappings relative to the Steam Bladesong root:

| Archive payload | Authorized destination |
| --- | --- |
| `Scripts/`, `dlls/`, configuration and ordinary files | `Bladesong/Binaries/Win64/ue4ss/Mods/<id>/...` |
| `shared/...` in **BladesongModFramework only** | `Bladesong/Binaries/Win64/ue4ss/Mods/shared/BladesongFramework/...` |
| `assets/logicmods/<filename>.pak/.utoc/.ucas` | `Bladesong/Content/Paks/LogicMods/<filename>` |

A manager must deploy the portable root manifest or an identical portable receipt where the runtime can read it. BindMod accepts mod.json, the historical manifest name, or bmf-installed.json. Installation ownership belongs in a separate deployment record, not the author's manifest. User Data, SaveGames, PCL libraries and logs are excluded. Paths with traversal, drive letters, links, reserved names, duplicates or unlisted files are refused. Ownership receipts and deployment records cannot be supplied as payload.

The SDK packager produces the same archive for the in-game manager and any future compatible third-party adapter. A Vortex extension would map these fixed roots, check hashes, register its own ownership and resolve these dependencies through Vortex's supported APIs. No native Vortex support is claimed. Other managers must implement a verified adapter before offering automatic install or migration.


`standalone: true` describes a UE4SS mod that does not bind the framework API, such as BladesongModManager. Its manifest can omit `api`. Ordinary SDK-integrated mods must still declare `api` and their runtime dependencies. A manager itself need not require the framework to resolve it as a dependency for an SDK mod. The schema and validator both enforce the conditional API requirement.
