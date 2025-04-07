#! /usr/bin/env bash

function bluer_ai_repeat() {
    local options=$1
    local count=$(abcli_option "$options" count 1)

    # https://stackoverflow.com/a/3737773/17619982
    for index in $(seq $count); do
        abcli_log "🔄 $index / $count"
        abcli_eval "$@"
    done
}
