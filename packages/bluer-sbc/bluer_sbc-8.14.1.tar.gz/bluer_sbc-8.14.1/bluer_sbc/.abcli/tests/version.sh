#! /usr/bin/env bash

function test_bluer_sbc_version() {
    local options=$1

    abcli_eval ,$options \
        "bluer_sbc version ${@:2}"
}
