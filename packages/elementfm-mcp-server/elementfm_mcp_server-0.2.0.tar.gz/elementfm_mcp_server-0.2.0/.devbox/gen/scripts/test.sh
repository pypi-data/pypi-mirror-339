set -e

if [ -z "$__DEVBOX_SKIP_INIT_HOOK_0142eeb9a699a02e636df77a02a40496ef18b415a9a409a98449ff5d5cabd65f" ]; then
    . "/mnt/data/code/element.fm/elementfm-mcp-server/.devbox/gen/scripts/.hooks.sh"
fi

echo "Error: no test specified" && exit 1
