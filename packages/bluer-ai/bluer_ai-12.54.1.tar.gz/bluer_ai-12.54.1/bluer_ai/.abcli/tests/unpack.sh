#! /usr/bin/env bash

function test_bluer_ai_unpack_repo_name() {
    abcli_assert \
        $(abcli_unpack_repo_name bluer_ai) \
        bluer-ai
}
