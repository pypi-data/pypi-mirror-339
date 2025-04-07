#! /usr/bin/env bash

function test_bluer_ai_repeat() {
    bluer_ai_repeat - ls
    abcli_assert "$?" 0

    bluer_ai_repeat count=3 ls
    abcli_assert "$?" 0
}
