#!/bin/bash

# Pongo a disposición pública este script bajo el término de "software de dominio público".
# Puedes hacer lo que quieras con él porque es libre de verdad; no libre con condiciones como las licencias GNU y otras patrañas similares.
# Si se te llena la boca hablando de libertad entonces hazlo realmente libre.
# No tienes que aceptar ningún tipo de términos de uso o licencia para utilizarlo o modificarlo porque va sin CopyLeft.

# ----------
# Script de NiPeGun para instalar el simulador del PLC 1214c de clase de Zubiri
#
# Ejecución remota (puede requerir permisos sudo):
#   curl -sL https://raw.githubusercontent.com/nipegun/pySIEM/refs/heads/main/install_reinstall_update.sh | bash
#
# Ejecución remota como root (para sistemas sin sudo):
#   curl -sL https://raw.githubusercontent.com/nipegun/pySIEM/refs/heads/main/install_reinstall_update.sh | sed 's-sudo--g' | bash
#
# Bajar y editar directamente el archivo en nano
#   curl -sL https://raw.githubusercontent.com/nipegun/pySIEM/refs/heads/main/install_reinstall_update.sh | nano -
# ----------

# Definir constantes de color
  cColorAzul='\033[0;34m'
  cColorAzulClaro='\033[1;34m'
  cColorVerde='\033[1;32m'
  cColorRojo='\033[1;31m'
  # Para el color rojo también:
    #echo "$(tput setaf 1)Mensaje en color rojo. $(tput sgr 0)"
  cFinColor='\033[0m'

# Notificar inicio de ejecución del script
  echo ""
  echo -e "${cColorAzulClaro}  Iniciando el script de instalación/reinstalación/actualización de pySIEM...${cFinColor}"

# Clonar el repositorio
  echo ""
  echo "    Clonando el repositorio..."
  echo ""
  # Comprobar si el paquete git está instalado. Si no lo está, instalarlo.
    if [[ $(dpkg-query -s git 2>/dev/null | grep installed) == "" ]]; then
      echo ""
      echo -e "${cColorRojo}      El paquete git no está instalado. Iniciando su instalación...${cFinColor}"
      echo ""
      sudo apt-get -y update
      sudo apt-get -y install git
      echo ""
    fi
  cd /tmp
  git clone https://github.com/nipegun/pySIEM.git

# Preparar estructura de carpetas
  rm -f ~/pySIEM/* 2>/dev/null
  mkdir ~/pySIEM/ 2>/dev/null
  mv /tmp/pySIEM/* ~/pySIEM/
  # Asignar permisos de ejecución a los scripts
    chmod +x ~/pySIEM/*.sh
    chmod +x ~/pySIEM/*.py

# Notificar fin de ejecución del script
  echo ""
  echo "    El script ha finalizado."
  echo ""
  echo "      Para ejecutar el servidor:"
  echo ""
  echo "        Como usuario normal:"
  echo ""
  echo "          cd ~/pySIEM/ && sudo python3 server.py && cd ~/"
  echo ""
  echo "        Como usuario root:"
  echo ""
  echo "          cd ~/pySIEM/ && sudo python3 server.py && cd ~/"
  echo ""
  echo "      Para reinstalarlo o actualizarlo:"
  echo ""
  echo "        ~/pySIEM/install_reinstall_update.sh"
  echo ""
  echo "      Para enviar datos:"
  echo ""
