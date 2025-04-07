#! /usr/bin/env bash

function bluer_objects() {
    local task=$1

    abcli_generic_task \
        plugin=bluer_objects,task=$task \
        "${@:2}"
}

abcli_log $(bluer_objects version --show_icon 1)
