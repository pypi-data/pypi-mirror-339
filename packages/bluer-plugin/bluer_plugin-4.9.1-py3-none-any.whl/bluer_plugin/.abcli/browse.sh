#! /usr/bin/env bash

function bluer_plugin_browse() {
    local options=$1
    local what=$(abcli_option_choice "$options" actions,repo repo)

    local url="https://github.com/kamangir/bluer-plugin"
    [[ "$what" == "actions" ]] &&
        url="$url/actions"

    bluer_ai_browse $url
}
