#! /usr/bin/env bash

function bluer_ai_open() {
    local options=$1

    local extension=$(abcli_option "$options" extension)
    local open_GIS=$(abcli_option_int "$options" QGIS 0)
    [[ $open_QGIS == 1 ]] &&
        extension="qgz"

    local object_name=$(abcli_clarify_object $2 .)

    local filename=""
    [[ ! -z "$extension" ]] &&
        filename=$object_name.$extension
    filename=$(abcli_option "$options" filename $filename)

    local what=$ABCLI_OBJECT_ROOT/$object_name
    [[ ! -z "$filename" ]] &&
        what=$what/$filename

    abcli_log "📜 $what"
    open "$what"
}
