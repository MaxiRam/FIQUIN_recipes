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


