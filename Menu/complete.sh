#!/usr/bin/env bash
# https://stackoverflow.com/questions/45778261/custom-bash-autocomplete-with-file-path-completion
complete -o default -W "--menu --read_only --help --path --load --load_timer_time" menu
