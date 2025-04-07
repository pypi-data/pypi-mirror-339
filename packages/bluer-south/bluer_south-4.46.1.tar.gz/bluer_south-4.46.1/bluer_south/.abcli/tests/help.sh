#! /usr/bin/env bash

function test_bluer_south_help() {
    local options=$1

    local module
    for module in \
        "@south" \
        \
        "@south pypi" \
        "@south pypi browse" \
        "@south pypi build" \
        "@south pypi install" \
        \
        "@south pytest" \
        \
        "@south test" \
        "@south test list" \
        \
        "@south browse" \
        \
        "bluer_south"; do
        abcli_eval ,$options \
            bluer_ai_help $module
        [[ $? -ne 0 ]] && return 1

        abcli_hr
    done

    return 0
}
