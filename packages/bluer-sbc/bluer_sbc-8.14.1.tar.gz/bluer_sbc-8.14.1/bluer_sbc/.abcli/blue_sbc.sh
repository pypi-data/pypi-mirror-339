#! /usr/bin/env bash

function bluer_sbc() {
    local task=$1

    abcli_generic_task \
        plugin=bluer_sbc,task=$task \
        "${@:2}"
}

abcli_log $(bluer_sbc version --show_icon 1)
