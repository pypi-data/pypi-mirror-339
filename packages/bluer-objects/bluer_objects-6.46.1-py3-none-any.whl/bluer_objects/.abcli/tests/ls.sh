#! /usr/bin/env bash

function test_bluer_objects_ls() {
    local object_name=test_bluer_objects_ls-$(abcli_string_timestamp_short)

    python3 -m bluer_objects.testing \
        create_test_asset \
        --object_name $object_name
    [[ $? -ne 0 ]] && return 1
    abcli_hr

    bluer_objects_upload - $object_name
    [[ $? -ne 0 ]] && return 1
    abcli_hr

    bluer_objects_ls cloud $object_name
    [[ $? -ne 0 ]] && return 1
    abcli_hr

    bluer_objects_ls local $object_name
    [[ $? -ne 0 ]] && return 1
    abcli_hr

    bluer_objects_ls $abcli_path_bash/tests/
}
