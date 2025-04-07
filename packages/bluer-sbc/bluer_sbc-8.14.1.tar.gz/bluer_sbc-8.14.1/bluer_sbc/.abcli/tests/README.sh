#! /usr/bin/env bash

function test_bluer_sbc_README() {
    local options=$1

    abcli_eval ,$options \
        bluer_sbc build_README
}
