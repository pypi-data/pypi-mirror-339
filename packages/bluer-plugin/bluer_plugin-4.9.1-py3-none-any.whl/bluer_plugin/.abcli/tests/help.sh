#! /usr/bin/env bash

function test_bluer_plugin_help() {
    local options=$1

    local module
    for module in \
        "@plugin" \
        \
        "@plugin pypi" \
        "@plugin pypi browse" \
        "@plugin pypi build" \
        "@plugin pypi install" \
        \
        "@plugin pytest" \
        \
        "@plugin test" \
        "@plugin test list" \
        \
        "@plugin browse" \
        "@plugin leaf" \
        "@plugin node" \
        "@plugin node leaf" \
        \
        "@plugin task" \
        \
        "bluer_plugin"; do
        abcli_eval ,$options \
            bluer_ai_help $module
        [[ $? -ne 0 ]] && return 1

        abcli_hr
    done

    return 0
}
