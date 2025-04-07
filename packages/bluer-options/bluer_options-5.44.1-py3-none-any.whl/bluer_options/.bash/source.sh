#! /usr/bin/env bash

function bluer_ai_source_path() {
    local path=$1

    local options=$2
    local ignore_error=$(abcli_option_int "$options" ignore_error 0)
    local do_log=$(abcli_option_int "$options" log 0)

    if [[ ! -d "$path" ]]; then
        [[ "$ignore_error" == 0 ]] &&
            abcli_log_error "bluer_ai_source_path: $path: path not found."
        return 1
    fi

    pushd $path >/dev/null

    local filename
    for filename in *.sh; do
        [[ "$do_log" == 1 ]] &&
            abcli_log "🔹 ${filename%.*}"

        source $filename
    done

    popd >/dev/null
}

function bluer_ai_source_caller_suffix_path() {
    local suffix=$1

    local path=$(dirname "$(realpath "${BASH_SOURCE[1]}")")

    [[ ! -z "$suffix" ]] &&
        path=$path$suffix

    bluer_ai_source_path "$path" \
        "${@:2}"
}
