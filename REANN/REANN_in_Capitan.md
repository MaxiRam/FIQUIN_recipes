## Installation of REANN package for interatomic potential fitting

- Install Miniconda and create an environment for REANN
```bash
conda create --name reann
conda activate reann
```

- Install `PyTorch` and `opt_einsum` packages required by REANN.
```bash
conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
conda install opt_einsum -c conda-forge
```
Follow the instruction [here](https://pytorch.org/get-started/locally/) for installing PyTorch.

Documentation and installing instructions for opt_einsum can be found [here](https://optimized-einsum.readthedocs.io/en/stable/install.html).



```bash
mkdir $HOME/Software
cd $HOME/Software
git clone https://github.com/zhangylch/REANN.git

# To make sure python will find all reann's scripts
conda install conda-build
conda develop $HOME/Software/REANN/reann
```

The files included in the `examples/CO2Ni111` folder can be used for testing the installation. Follow the instructions in the README file included therein.

---

## Installation of LAMMPS for Molecular Dynamics Simulations using reann potential as pair_style

Step-by-step installation of lammps in Capitan with reann pair_style.
Following the guidelines from reann developer at: https://github.com/zhangylch/REANN/blob/main/manual/REANNPackage_manumal_v_1_1.pdf

I'm assuming REANN package is already installed for trainnig the models and the source code is located at $HOME/Software/REANN

Create folder and get the lammps version specified in reann manual

```bash
export LAMMPS=$HOME/Software/LAMMPS
mkdir -p $LAMMPS
cd $LAMMPS
curl https://download.lammps.org/tars/lammps-10Feb2021.tar.gz -o lammps-10Feb2021.tar.gz
tar -xzvf lammps-10Feb2021.tar.gz
export LAMMPS_ROOT=$LAMMPS/lammps-10Feb21
cd
```


    
Create folder and get libtorch C++ version (Serafin does not have GPU's)

```bash
export TORCH_ROOT=$HOME/Software/libtorch
mkdir -p $TORCH_ROOT
cd $TORCH_ROOT
curl https://download.pytorch.org/libtorch/cu117/libtorch-shared-with-deps-2.0.1%2Bcu117.zip -o libtorch-cu117.zip
unzip libtorch-cu117.zip
cd
```

Copy necessary files for the reann pair_style interface to the LAMMPS folder

```bash
mv $TORCH_ROOT/libtorch $LAMMPS_ROOT
export REANN_INTERFACE=$HOME/Software/REANN/reann/lammps-REANN-interface
mkdir $LAMMPS_ROOT/build
cp $REANN_INTERFACE/build/build.sh $LAMMPS_ROOT/build
cp $REANN_INTERFACE/cmake/CMakeLists.txt $LAMMPS_ROOT/cmake
mkdir $LAMMPS_ROOT/examples/reann
cp $REANN_INTERFACE/examples/* $LAMMPS_ROOT/examples/reann
cp $REANN_INTERFACE/src/* $LAMMPS_ROOT/src
```
    
Load cmake, compiler and library modules

```bash
module load cmake/3.21.3 intel/2022.0.2
```
    
Build lammps configuration