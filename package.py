name = "git"

__version__ = "2.32.0"
version = __version__

relocatable = True

build_command = r"""
set -eufx -o pipefail

cp "$REZ_BUILD_SOURCE_PATH"/Dockerfile "$REZ_BUILD_SOURCE_PATH"/entrypoint.sh .

IMAGE_ID_FILE="$(readlink -f DockerImageID)"
docker build --rm --iidfile="$IMAGE_ID_FILE" .

[ -t 1 ] && CONTAINER_ARGS=("--tty") || CONTAINER_ARGS=()
CONTAINER_ARGS+=("--workdir" "/usr/local/src")
CONTAINER_ARGS+=("--env" "INSTALL_DIR={install_dir}")
CONTAINER_ARGS+=("--env" "VERSION={version}")
CONTAINER_ARGS+=("$(cat $IMAGE_ID_FILE)")

if [ $REZ_BUILD_INSTALL -eq 1 ]
then
    CONTAINTER_ID=$(docker create "{CONTAINER_ARGS}")
    docker start -ia "$CONTAINTER_ID"
    docker cp "$CONTAINTER_ID":"{install_dir}"/. "{install_dir}"/
    docker rm "$CONTAINTER_ID"
fi
""".format(
    version=__version__,
    install_dir="${{REZ_BUILD_INSTALL_PATH:-/usr/local}}",
    CONTAINER_ARGS="${{CONTAINER_ARGS[@]}}",
)


def commands():
    import os.path

    env.PATH.append(os.path.join("{root}", "bin"))


@late()
def tools():
    import os

    bin_path = os.path.join(str(this.root), "bin")
    return os.listdir(bin_path)
