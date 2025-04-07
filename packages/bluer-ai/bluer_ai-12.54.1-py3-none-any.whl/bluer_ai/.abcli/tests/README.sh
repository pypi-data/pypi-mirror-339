#! /usr/bin/env bash

function test_bluer_ai_README() {
    local options=$1

    abcli_eval ,$options \
        bluer_ai build_README
}
