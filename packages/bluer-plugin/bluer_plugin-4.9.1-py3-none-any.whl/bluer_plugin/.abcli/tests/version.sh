#! /usr/bin/env bash

function test_bluer_plugin_version() {
    local options=$1

    abcli_eval ,$options \
        "bluer_plugin version ${@:2}"
}
