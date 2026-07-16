# AutoTyper v1.1 Deployment Guide

## 1. Release Targets
- **GitHub Releases**: Target for developers and power users requiring source or raw binaries.
- **The IoT Labs Website**: Target for general end-users.

## 2. GitHub Release Process
1. Draft a new release for tag `v1.1.0`.
2. Title the release: `AutoTyper v1.1 - Quality of Life Update`.
3. Paste the contents of `FINAL_PRODUCTION_CHANGELOG.md` into the release description.
4. Attach the following artifacts:
   - `AutoTyper_v1.1_Portable.zip` (Generated from the `BUILD_GUIDE.md`)
   - Source code (zip and tar.gz)

## 3. Website Deployment
1. Upload `AutoTyper_v1.1_Portable.zip` to the primary S3/CDN hosting bucket.
2. Update the website database version string to `1.1.0` to trigger any auto-update banners for v1.0 users.
3. Update the changelog widget on the product landing page.

## 4. Post-Deployment Verification
- Download the zip from the live GitHub release link on a fresh Windows 11 Sandbox environment.
- Extract and launch `AutoTyper.exe`.
- Verify no Windows SmartScreen blocks occur (if EV code signed, otherwise ignore).
- Verify standard typing functionality works out of the box.
