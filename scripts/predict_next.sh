#!/usr/bin/env bash

function marisa () {
  marisa-predictive-search -n 0 $1 | tail -n +2 | cut -f 2 | cut -d ' ' -f $2- | awk '{if ($NF != $1) print $NF, $1}' | sort -n | cut -d ' ' -f 2 | head -n 1000
}

function unsorted () {

  rev_str=`tr '[:upper:]' '[:lower:]' | rev`
  last_4=`echo $rev_str | cut -d ' ' -f -4 | rev`
  last_3=`echo $rev_str | cut -d ' ' -f -3 | rev`
  last_2=`echo $rev_str | cut -d ' ' -f -2 | rev`
  last_1=`echo $rev_str | cut -d ' ' -f -1 | rev`

  offset=0

  if [[ ${rev_str:0:1} == " " ]]; then
      offset=1
  fi

  if [[ "$last_4" != "$last_3" ]]; then
    echo "$last_4" | marisa $1 $((4 + $offset))
  fi
  if [[ "$last_3" != "$last_2" ]]; then
    echo "$last_3" | marisa $1 $((3 + $offset))
  fi
  if [[ "$last_2" != "$last_1" ]]; then
    echo "$last_2" | marisa $1 $((2 + $offset))
  fi

  if [[ ${rev_str:0:1} == " " ]]; then
    echo "$last_1" | marisa $1 $((1 + $offset))
  fi
}

unsorted $1 | awk '!seen[$0]++' | head -n 100
