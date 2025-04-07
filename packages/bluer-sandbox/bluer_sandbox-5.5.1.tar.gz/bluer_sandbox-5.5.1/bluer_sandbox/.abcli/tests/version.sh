#! /usr/bin/env bash

function test_bluer_sandbox_version() {
    local options=$1

    abcli_eval ,$options \
        "bluer_sandbox version ${@:2}"
}
