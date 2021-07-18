#!/bin/bash
set -euf -o pipefail

# Perform the actual Python building and installing
# Ideally we're currently in an empty directory
INSTALL_DIR="${INSTALL_DIR:-$(mktemp -d)}"
VERSION="${VERSION:-2.32.0}"
URL=https://mirrors.edge.kernel.org/pub/software/scm/git/git-"$VERSION".tar.gz
export RUNTIME_PREFIX=YesPlease

mkdir -vp "$INSTALL_DIR"

CURL_FLAGS=("-L")
[ -t 1 ] && CURL_FLAGS+=("-#") || CURL_FLAGS+=("-sS")

echo "Downloading and extracting: $URL"
echo "    into current directory: $(pwd)"
curl "${CURL_FLAGS[@]}" "$URL" | tar --strip-components=1 -xz

# LD_RUN_PATH='$ORIGIN:$ORIGIN/../lib' make -s -j"$(nproc)"
make -j "$(nproc)" --quiet prefix="$INSTALL_DIR" install

make -j "$(nproc)" --quiet prefix="$INSTALL_DIR" install-doc
make -j "$(nproc)" --quiet prefix="$INSTALL_DIR" install-html
cp -rv contrib/completion "$INSTALL_DIR"/share/

# Ensure all libraries are linked properly. Exit 1 if any libraries are "not found"
LDD_RESULTS="$(mktemp)"
ldd -v "$INSTALL_DIR"/bin/git > "$LDD_RESULTS"
grep -q "not found" "$LDD_RESULTS" || exit 0

grep "not found" "$LDD_RESULTS"
echo "----- from: ldd -v "$INSTALL_DIR"/bin/git -----"
cat "$LDD_RESULTS"
exit 1