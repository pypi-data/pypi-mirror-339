#! /usr/bin/env bash

function test_bluer_south_version() {
    local options=$1

    abcli_eval ,$options \
        "bluer_south version ${@:2}"
}
