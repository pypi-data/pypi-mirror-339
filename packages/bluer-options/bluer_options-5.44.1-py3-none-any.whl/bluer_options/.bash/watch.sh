#! /usr/bin/env bash

function bluer_ai_watch() {
    local options=$1
    local do_clear=$(abcli_option_int "$options" clear 1)

    while true; do
        [[ "$do_clear" == 1 ]] && clear

        abcli_eval "$@"

        bluer_ai_sleep ,$options
    done
}
