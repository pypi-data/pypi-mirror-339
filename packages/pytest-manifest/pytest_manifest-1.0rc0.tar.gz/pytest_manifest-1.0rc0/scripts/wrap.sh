pathspec="*"


# echo $pathspec
eval "pathspec_parts=('$pathspec')"
echo "$pathspec_parts"


touched=$(git diff --name-only HEAD HEAD^ -- "${pathspec_parts[@]}")

touched=$(echo "$touched" | tr '\n' ' ' | xargs)

echo "touched: $touched"
