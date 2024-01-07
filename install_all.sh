#/bin/bash
directory=$1
for file in $directory/*.vsix
do
    code --install-extension $file
done