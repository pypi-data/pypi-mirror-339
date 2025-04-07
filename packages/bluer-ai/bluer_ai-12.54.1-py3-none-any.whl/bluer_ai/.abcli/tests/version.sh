#! /usr/bin/env bash

function test_bluer_ai_version() {
    local options=$1

    abcli_eval ,$options \
        "bluer_ai version ${@:2}"

    return 0
}
