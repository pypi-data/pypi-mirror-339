#! /usr/bin/env bash

function abcli_install_bluer_sbc_template() {
    abcli_log "wip"
}

if [ "$BLUER_SBC_HARDWARE_KIND" == "bluer_sbc_template" ]; then
    abcli_install_module bluer_sbc_template 101
fi
