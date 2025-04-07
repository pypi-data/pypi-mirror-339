#! /usr/bin/env bash

function test_bluer_south_README() {
    local options=$1

    abcli_eval ,$options \
        bluer_south build_README
}
