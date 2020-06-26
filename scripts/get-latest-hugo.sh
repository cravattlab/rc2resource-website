#!/usr/bin/env bash

# run from root directory of repository

set -o errexit

# function taken from https://gist.github.com/lukechilds/a83e1d7127b78fef38c2914c4ececc3c
get_latest_release() {
  curl --silent "https://api.github.com/repos/gohugoio/hugo/releases/latest" | # Get latest release from GitHub api
    grep '"tag_name":' |                                                       # Get tag line
    sed -E 's/.*"([^"]+)".*/\1/'                                               # Pluck JSON value
}

main() {
    local version="$(get_latest_release)"   # eg v0.36.1

    # remove first 'v'
    version="${version#?}"

    local url="https://github.com/gohugoio/hugo/releases/download/v${version}/hugo_${version}_Linux-64bit.tar.gz"
    wget -qO- "${url}" | tar xvz -C ./bin/hugo/
}

main "$@"
