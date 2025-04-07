#! /usr/bin/env bash

function test_bluer_sandbox_help() {
    local options=$1

    local module
    for module in \
        "@sandbox" \
        \
        "@sandbox pypi" \
        "@sandbox pypi browse" \
        "@sandbox pypi build" \
        "@sandbox pypi install" \
        \
        "@sandbox pytest" \
        \
        "@sandbox test" \
        "@sandbox test list" \
        \
        "@sandbox browse" \
        \
        "bluer_sandbox"; do
        abcli_eval ,$options \
            bluer_ai_help $module
        [[ $? -ne 0 ]] && return 1

        abcli_hr
    done

    return 0
}
