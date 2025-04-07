#! /usr/bin/env bash

function bluer_objects_mlflow_tags_get() {
    local object_name=$(abcli_clarify_object $1 .)

    python3 -m bluer_objects.mlflow \
        get_tags \
        --object_name $object_name \
        "${@:2}"
}
