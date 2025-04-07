#! /usr/bin/env bash

function bluer_ai_conda_list() {
    abcli_eval ,$1 \
        conda info \
        --envs "${@:2}"
}
