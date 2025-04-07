#! /usr/bin/env bash

function test_bluer_objects_storage() {
    local options=$1

    local object_name=test_bluer_objects_storage-$(abcli_string_timestamp_short)
    local object_path=$ABCLI_OBJECT_ROOT/$object_name
    mkdir -pv $object_path

    python3 -m bluer_objects.testing \
        create_test_asset \
        --object_name $object_name
    [[ $? -ne 0 ]] && return 1

    # testing upload
    abcli_hr

    bluer_objects_upload \
        filename=this.yaml \
        $object_name
    [[ $? -ne 0 ]] && return 1
    abcli_hr

    bluer_objects_upload \
        filename=subfolder/this.yaml \
        $object_name
    [[ $? -ne 0 ]] && return 1
    abcli_hr

    bluer_objects_upload \
        - \
        $object_name
    [[ $? -ne 0 ]] && return 1
    abcli_hr

    # clean-up
    rm -rfv $object_path
    abcli_hr

    # testing download

    bluer_objects_download \
        filename=this.yaml \
        $object_name
    [[ $? -ne 0 ]] && return 1
    abcli_hr

    bluer_objects_download \
        filename=subfolder/this.yaml \
        $object_name
    [[ $? -ne 0 ]] && return 1
    abcli_hr

    bluer_objects_download \
        - \
        $object_name
}
