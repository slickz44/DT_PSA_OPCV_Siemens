#!/usr/bin/env python3
"""Write this module's released version into module.json.

    python _workflow/tools/set_module_version.py            print the current version
    python _workflow/tools/set_module_version.py --check    validate module.json, write nothing
    python _workflow/tools/set_module_version.py 0.2.0      set the version

WHY THIS EXISTS. This module is not a Node package and has no package.json, so
semantic-release has nowhere of its own to write the version. `module.json` is this
module's identity - it is what the main repo's check_compatibility.py fetches over https
to answer "which version is this module" - so that is where the version belongs. `.releaserc.json` calls this from @semantic-release/exec's
prepareCmd, and @semantic-release/git commits the result alongside CHANGELOG.md.

WHY IT IS IN _workflow/ AND NOT _private/. The line is what a tool READS. This one reads
and writes one tracked file. It touches no vendor project and no Unity export, so
publishing it discloses nothing - and .github/workflows/release.yml has to run it from a
checkout of this repository alone. It is this module's first tool, and _workflow/tools/
is where the public half lives; a generator that reads the TIA project, when there is
one, belongs in the gitignored _private/ instead.

WHY IT EDITS ONE LINE RATHER THAN REWRITING THE FILE. module.json is hand-maintained:
its key order and its formatting are somebody's, not a serialiser's. json.dump() would
reformat all of it on every release and bury the one field that actually changed in a
diff nobody reads. The file is parsed first, so a malformed one is refused rather than
silently patched.

NEVER HAND-EDIT `version` AFTER THE FIRST RELEASE. From then on the release bot owns it,
exactly as it owns CHANGELOG.md, and the next release overwrites whatever was put there.
"""

import json
import re
import sys
from pathlib import Path

# Anchored on this file, never on the working directory: the same command has to work
# from a standalone clone of this module and from a main repo checkout above it.
MODULE = Path(__file__).resolve().parents[2]
MODULE_JSON = MODULE / "module.json"

# The official semver pattern, minus build metadata - a tag is `v${version}` and a `+`
# is not valid in a git ref name.
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*))?$")

# The `"version": "..."` member, captured so only its value is replaced. Anchored to the
# start of a line so a `version` key nested inside some future object cannot match.
VERSION_LINE = re.compile(r'^(?P<head>\s*"version"\s*:\s*")(?P<value>[^"]*)(?P<tail>")',
                          re.MULTILINE)


def load():
    """The parsed module.json and its raw text, or a fatal message."""
    if not MODULE_JSON.exists():
        raise SystemExit(f"error: {MODULE_JSON} does not exist")
    # Read as bytes and decode by hand rather than read_text(): text mode translates
    # CRLF to LF on the way in, and the patched string is written straight back out.
    # Path.read_text() only grew a `newline` argument in 3.13, so this is the portable
    # way to leave a CRLF working tree exactly as it was found.
    raw = MODULE_JSON.read_bytes().decode("utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise SystemExit(f"error: {MODULE_JSON} is not valid JSON - {e}")
    if not isinstance(data, dict):
        raise SystemExit(f"error: {MODULE_JSON} is not a JSON object")
    return data, raw


def check(data, raw):
    """Everything a release will need from this file, verified before one is cut."""
    problems = []
    current = data.get("version")
    if current is None:
        problems.append('no "version" member - add one, the release cannot create it')
    elif not isinstance(current, str) or not SEMVER.match(current):
        problems.append(f'"version" is {current!r}, which is not a semver string')
    elif len(VERSION_LINE.findall(raw)) != 1:
        # Parsing found exactly one version; the text must too, or the rewrite below
        # would edit the wrong member or none at all.
        problems.append('"version" could not be located as a single line of text')
    for key in ("name", "vendor", "repository"):
        if not data.get(key):
            problems.append(f'no "{key}" member')
    if problems:
        for p in problems:
            print(f"error: module.json {p}", file=sys.stderr)
        return 1
    print(f"module.json is {data['name']} {current}")
    return 0


def write(version, data, raw):
    version = version.lstrip("v")          # tolerate `v1.2.0`, which is the tag, not the version
    if not SEMVER.match(version):
        raise SystemExit(f"error: {version!r} is not a semver version")
    if len(VERSION_LINE.findall(raw)) != 1:
        raise SystemExit('error: module.json has no single "version" line to rewrite')

    current = data.get("version")
    if current == version:
        print(f"module.json already reads {version} - nothing to write")
        return 0

    patched = VERSION_LINE.sub(lambda m: m.group("head") + version + m.group("tail"),
                               raw, count=1)
    # Written back byte for byte apart from the one value: this file is committed by the
    # release, and a whole-file line-ending flip would be an unreviewable diff.
    MODULE_JSON.write_bytes(patched.encode("utf-8"))
    print(f"module.json: {current} -> {version}")
    return 0


def main(argv):
    data, raw = load()
    args = [a for a in argv if a != "--check"]
    if "--check" in argv:
        return check(data, raw)
    if not args:
        print(data.get("version") or "")
        return 0
    if len(args) > 1:
        raise SystemExit("usage: set_module_version.py [--check | <version>]")
    return write(args[0], data, raw)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
