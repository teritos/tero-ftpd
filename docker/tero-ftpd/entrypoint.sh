#!/bin/bash

set -e
echo "-- entrypoint.sh --"
cd /tero-ftpd


if [ "$CREATE_VIRTUALENV" = "1" ]
then
  echo "-- Creando el virtualenv --"
  if [ -d /env ]
  then
    rm -rf /env
  fi
  python3 -m venv /env
  source /env/bin/activate
  export PYTHONPATH=/env/
  export PYTHON=/env/bin/python3
  export PIP=/env/bin/pip
  echo "-- Configurado entorno virtual de python en $PYTHONPATH --"
  echo "-- El interprete de python que voy a usar es $PYTHON --"
  echo "-- Instalando requerimientos con $PIP --"
  echo "-- Installing: requirements.txt --"
  $PIP install --upgrade pip
  if [ "$INSTALL_REQUIREMENTS" = "1" ]
  then
    $PIP install -r requirements.txt
    echo "-- Installing: requirements.txt done --"
  fi
  $PYTHON setup.py develop
fi

case "$1" in
    start-ftpd)
        echo "Runing tero ftpd server..."
        source /env/bin/activate
        cd /tero-ftpd/
        ./bin/teroftpd 
        ;;
    *)
        cd /
        exec "$@"
esac

exit 1
