#!/bin/bash

# Rename myapplication to something of the user's choice.
# Also replace myapplication inside files with the above.
# Initial version by John Parejko

function rename_files ()
{
  echo "Renaming all $1->$2 filenames..."
  find . -depth -name "*$1*" -not -path '*/\.*' -execdir rename "s/$1/$2/g" {} \; -print
}

function replace_in_files ()
{
  echo "Replacing all $1->$2 in files..."
  find . -type f -not -path '*/\.*' -not -name $0 -execdir sed -i "" "s/$1/$2/g" "{}" \; -print
}

if [ $# -lt 1 ]; then
  echo "Specify the name you want myapplication changed to as arg1!"
  exit 1
else
  NEW_NAME=$1
fi

rename_files "myapplication" $NEW_NAME
echo
replace_in_files "myapplication" $NEW_NAME
