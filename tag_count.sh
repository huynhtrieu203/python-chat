#!/bin/bash
#get highest tag number
VERSION=`git tag -l --sort -version:refname | head -n 1`
#replace . with space so can split into an array
VERSION_BITS=(${VERSION//./ })
#get number parts and increase last one by 1
VNUM1=${VERSION_BITS[0]}
VNUM2=${VERSION_BITS[1]}
VNUM3=${VERSION_BITS[2]}
# VNUM1=`echo $VNUM1 | sed \'s/v//\'`
# Check for #major or #minor in commit message and increment the relevant version number
MAJOR=`git log --format=%B -n 1 HEAD | grep '#major'`
MINOR=`git log --format=%B -n 1 HEAD | grep '#minor'`
if [ "$MAJOR" ]; then
    echo "Update major version"
    VNUM1=$((VNUM1+1))
    VNUM2=0
    VNUM3=0
elif [ "$MINOR" ]; then
    echo "Update minor version"
    VNUM2=$((VNUM2+1))
    VNUM3=0
else
    echo "Update patch version"
    VNUM3=$((VNUM3+1))
fi
#create new tag
NEW_TAG="$VNUM1.$VNUM2.$VNUM3"
#get current hash and see if it already has a tag
GIT_COMMIT=`git rev-parse HEAD`
NEEDS_TAG=`git describe --contains $GIT_COMMIT` > /dev/null
#only tag if no tag already (would be better if the git describe command above could have a silent option)
if [ -z "$NEEDS_TAG" ]; then
    git tag $NEW_TAG
    echo "Updating $VERSION to $NEW_TAG"
else
    echo "Already a tag on this commit"
fi
