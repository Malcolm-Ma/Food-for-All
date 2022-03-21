#!/bin/bash

if (npm run doc);then
  echo "Generating API doc ..."
else
  echo "No apidoc detected, installing ..."
  npm install
  npm run doc
fi
