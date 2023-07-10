The files and folders in this directory are necessary for the successful execution of REANN example job, even the empy `test` folder.

For the execution follow the following steps:

1. Modify line 23 in `submit_reann_gpu.sh`, and set the COMMAND variable with the path to the REANN train script. 
2. Modify line 41 in `para/input_nn` file, and set the folder variable to the path containing these files.
3. Submit the job: `sbatch submit_reann_gpu.sh`

