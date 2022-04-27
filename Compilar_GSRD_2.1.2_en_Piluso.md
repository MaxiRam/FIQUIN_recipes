# Compilacion de GSRD con librerias de AENET

Se va a compilar GSRD de manera que pueda evaluar la energía y las fuerzas sobre cada átomso usando redes neuronales generadas con AENET. Vamos a hacer usando la suite de Intel y por otro lado usando gfortran.

## 1- Prerrequisitos

- Descargar AENET

```bash
cd $HOME; mkdir Software; cd Software
module load gitClone
git clone https://github.com/atomisticnet/aenet.git
```

- Obtener el código de GSRD y ponerlo en la carpeta $HOME/Software (para tener la última version pedir a Fabio o a Maxi).
- Definir unas variables para que sea más sintético el procedimiento
```bash
export AENET_ROOT=$HOME/Software/aenet
export GSRD_ROOT=$HOME/Software/gsrd-2.1.2
```

## 2- Compilacion usando Intel OneApi

En Piluso la suite Intel OneApi funciona sólo en algunos nodos, precisamente en los de las colas memium_amd, long_amd, fiquin, fiquinIB y colisionesIB. Así que vamos a tener que hacer una sesión interactiva en uno de esos nodos para compilar.

- Crear sesión interactiva
```bash
qrsh -q medium_amd -l h_rt=1:00:00
```
- Cargar intel OneApi
```bash
module load gcc-6.3.0
source /share/apps/intelOneApi/pilusoSetvars.sh
```
- Compilación de AENET y creación de librería AENET
```bash
cd $AENET_ROOT/lib

# Editar el Makefile y comentar la primera linea y descomentar la segunda para que use ifort.
make
cd $AENET_ROOT/src
make -f makefiles/Makefile.ifort_intelmpi
make -f makefiles/Makefile.ifort_intelmpi lib
```

Ahora en la carpeta `$AENET_ROOT/src` tienen que existir los archivos `libaenet.a` y `libaenet.so`; y en la carpeta `$AENET_ROOT/bin` tienen que existir los archivos `generate.x-2.0.4-ifort_intelmpi`, `train.x-2.0.4-ifort_intelmpi` y `predict.x-2.0.4-ifort_intelmpi`

Vamos a mover esos archivos para ponerlos en lugares donde no van a ser sobreescritos si hay que volver a compilar:
```bash
mkdir $HOME/bin
mv AENET_ROOT/bin/* $HOME/bin
mkdir $HOME/lib
mv $AENET_ROOT/lib/liblbfgsb.so $HOME/lib/liblbfgsb_intel.so
mv $AENET_ROOT/src/libaenet.so $HOME/lib/libaenet_intel.so
```

- Compilación de GSRD
  En este caso puede haber algunas diferencias en el proceso porque Fabio y yo hemos ido modificando el Makefile cada uno por su lado.
  
  - Editar el archivo `$GSRD_ROOT/Makefile_mpiifort` (con nano, vi o el editor que prefiera)
    1. Debajo de la linea donde se define `SRCD = $(BASE)/src`agregar una linea con lo siguiente: `LIBS_AENET=$(HOME)/lib`
    2. Modificar la linea donde se define la variable `LIB` para que diga: `LIB = -L$(LIBS_AENET) -laenet_intel -llbfgsb_intel`
  En este repositorio hay una carpeta que se llama `Makefiles_GSRD-2.1.2`, ahí pongo los makefiles para que queden adaptados a este archivo.
  
  - Compilar GSRD
```bash
cd $GSRD_ROOT 
make -f Makefile_mpiifort
```

Ahora debe existir el archivo `gsrd.x` en la carpeta `$GSRD_ROOT`. Vamos a moverlo a una ubicación más cómoda:

```bash
mv $GSRD_ROOT/gsdr.x $HOME/bin/gsrd-2.1.2_intel.x
```
 
