#!/bin/bash

cd doc_src && make html
cp -R build/html/ ../docs/
