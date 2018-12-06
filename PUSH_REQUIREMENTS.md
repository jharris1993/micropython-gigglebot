## Pushing to Master Branch

On the `master` branch, the build system releases new version to GitHub in the form of tarballs and changelogs. 

The CI system acts differently depending on what branch the build is triggered. We are now going to cover what's needed to do to merge a branch into the `master` branch.

1. Before pushing anything to `master` branch either through a merge or a direct push (highly discouraged), the `changelog.yaml` has to be updated to reflect the new release appropriately. Failure to do so will result in an errored build.

1. The new version that's added to the changelog must be higher than the previous one. We are following the rules of [semantic versioning](https://semver.org/). Failure to do so will result in an errored build.

1. The changelog entry must follow one of the 2 formats. The formats cannot be mixed together, so when writing the changelogs for a version, stick to a single format:

```yaml
v0.1.0:
  title: "Super Freaking Awesome Title"
  body:
    - Fix problem x that caused y to react badly.
    - Here's an improvement log.
    - And this is me just entering something.
```

Or this way.
```yaml
v0.2.3:
  title: "Intriguing and Dull Title"
  body:
    Sub Title:
      - Subpoint text.
      - This is the day you will always remember as the day you almost caught Captain Jack Sparrow.
    Another Sub Title:
      - Yet another subpoint.
      - Captain Barbossa hates this.
```

4. Last but not least, the version number that's used in the changelogs is going to end up being the tag in the repository at the end of the build - if all goes okay. The version number must follow this pattern: `v<x>.<y>.<z>`.

## Pushing to Other Branches

When pushes are done on other branches, nothing gets deployed anywhere, but the build can still fail if:
1. There are compilation errors in the firmware build - which is a good way to see if changing something in the code breaks the build.
1. The changelog is not updated to the next version.

## Avoiding the CI Build

If you wish to skip the build on a commit, just add to its commit message `[ci skip]`. Note that in case multiple commits are pushed together, the skip command is effective only if it is present in the commit message of the HEAD commit.