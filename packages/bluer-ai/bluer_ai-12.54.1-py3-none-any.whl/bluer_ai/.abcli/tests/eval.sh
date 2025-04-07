#! /usr/bin/env bash

function test_bluer_ai_eval() {
    abcli_eval - ls
    abcli_assert "$?" 0

    abcli_eval - lsz
    abcli_assert "$?" 0 not
}
