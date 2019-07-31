name = 'git'

version = '2.21.0'

build_command = '''
set -euf -o pipefail

cp -rv $REZ_BUILD_SOURCE_PATH/Dockerfiles .
# docker build --rm \
#     -f Dockerfiles/build_dependencies \
#     -t local/git-dependencies .

docker build --rm \
    --build-arg GIT_URL="https://github.com/git/git/archive/v{version}.tar.gz" \
    --build-arg INSTALL_DIR={install_dir} \
    -f Dockerfiles/git \
    -t local/git .

if [ $REZ_BUILD_INSTALL -eq 1 ]
then
    CONTAINTER_ID=$(docker run --rm -td local/git)
    docker cp $CONTAINTER_ID:{install_dir}/. {install_dir}
    docker stop $CONTAINTER_ID
    # echo "Please run: sudo yum install -y {install_dir}/etc/i3/runtime_deps/*.rpm"
fi
'''.format(
    version=version,
    install_dir='${{REZ_BUILD_INSTALL_PATH:-/usr/local}}',
)


def commands():
    import os.path
    env.PATH.append(os.path.join('{root}', 'bin'))
    env.LD_LIBRARY_PATH.append(os.path.join('{root}', 'lib'))


@late()
def tools():
    import os
    bin_path = os.path.join(str(this.root), 'bin')
    return os.listdir(bin_path)

