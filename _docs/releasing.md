# Publishing a release manually

Pushing commits updates the repository and its README download links. It does not create a release. GitHub Actions only validates module metadata; it does not choose versions, create tags or publish releases.

## Prepare the version

1. Test the TIA project and update `TIA_1/Archive/DT_PSA_OPCV.zap19` and any relevant documentation.
2. Choose a new version. For example, `1.0.1` for a correction, `1.1.0` for compatible new functionality, or `2.0.0` for incompatible changes. These are examples, not versions to create automatically.
3. Update `version` in `module.json` (without the `v` prefix) and add a dated entry describing the changes to `CHANGELOG.md`.
4. Commit and push the intended changes to `master`. Wait for **Project checks** to pass. Confirm that the release will include the intended archive and documentation.

## Create the release on GitHub

1. Open [Releases](https://github.com/slickz44/DT_PSA_OPCV_Siemens/releases), then **Draft a new release**.
2. Under **Choose a tag**, enter the chosen version with a `v` prefix, such as `v1.0.1`, and choose **Create new tag**. Use a new tag; do not reuse or move an existing release tag.
3. Select **master** as the target, ensuring it still points to the commit you intend to release.
4. Enter the release title and write the description manually: what changed, which tool versions were tested, and any setup changes or known limitations.
5. Optionally attach the tested `DT_PSA_OPCV.zap19` directly as a release asset for a convenient download and asset download counter. Use the same archive as in the selected repository version. GitHub also provides source ZIP/tar archives automatically.
6. Use **Save draft** to review first. Click **Publish release** only when ready. Mark a preview as a pre-release if appropriate.

The version in `module.json` and `CHANGELOG.md` is not changed automatically by the GitHub release form. Prepare these files before creating the tag.

A release is a snapshot of its tagged commit. Later pushes update the repository but do not update an existing release snapshot. Existing releases, including `v1.0.0`, remain available.

See [GitHub's release instructions](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).
