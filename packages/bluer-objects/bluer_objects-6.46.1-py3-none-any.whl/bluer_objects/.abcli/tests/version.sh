#! /usr/bin/env bash

function test_bluer_objects_version() {
    local options=$1

    abcli_eval ,$options \
        "bluer_objects version ${@:2}"

    return 0
}
