```bash
conda create --name reann
conda activate reann
```

```bash
pip3 install torch torchvision torchaudio
conda install opt_einsum -c conda-forge
```

```bash
mkdir $HOME/Software
cd $HOME/Software
git clone https://github.com/zhangylch/REANN.git

# To make sure python will find all reann's scripts
conda develop $HOME/Software/REANN/reann
```


