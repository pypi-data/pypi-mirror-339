#! /usr/bin/env bash

function test_bluer_sandbox_README() {
    local options=$1

    abcli_eval ,$options \
        bluer_sandbox build_README
}
