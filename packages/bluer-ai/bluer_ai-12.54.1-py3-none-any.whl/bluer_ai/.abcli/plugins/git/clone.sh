#! /usr/bin/env bash

function bluer_ai_git_clone() {
    local repo_address=$1
    local repo_name=$(abcli_unpack_repo_name $repo_address .)
    [[ "$repo_address" != http* ]] && [[ "$repo_address" != git@* ]] &&
        local repo_address=git@github.com:kamangir/$repo_name.git

    local options=$2
    local do_pull=$(abcli_option_int "$options" pull 0)
    local in_object=$(abcli_option_int "$options" object 0)
    local do_if_cloned=$(abcli_option_int "$options" if_cloned 0)
    local do_install=$(abcli_option_int "$options" install 0)
    local from_template=$(abcli_option_int "$options" from_template 1)
    local source=$(abcli_option "$options" source "")
    local then_cd=$(abcli_option_int "$options" cd 0)

    [[ "$in_object" == 0 ]] &&
        pushd $abcli_path_git >/dev/null

    abcli_log "cloning $repo_address -> $(pwd)"

    # https://docs.github.com/en/repositories/creating-and-managing-repositories/duplicating-a-repository
    # https://gist.github.com/0xjac/85097472043b697ab57ba1b1c7530274
    if [ ! -z "$source" ]; then
        git clone --bare git@github.com:$source.git
        local source_repo_name=$(abcli_string_after $source /)
        mv $source_repo_name.git $repo_name

        cd $repo_name
        git push --mirror $repo_address
        cd ..

        rm -rf $repo_name
    fi

    if [ ! -d "$repo_name" ]; then
        git clone $repo_address
    else
        [[ "$do_if_cloned" == 1 ]] && do_install=0

        if [ "$do_pull" == 1 ]; then
            cd $repo_name
            git pull
            cd ..
        fi
    fi

    if [ "$do_install" == 1 ]; then
        cd $repo_name
        pip3 install -e .
        cd ..
    fi

    [[ "$in_object" == 0 ]] &&
        popd >/dev/null

    [[ "$then_cd" == 1 ]] &&
        cd $abcli_path_git/$repo_name

    return 0
}
