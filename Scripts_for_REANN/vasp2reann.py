from ase.calculators.vasp import Vasp
from shutil import rmtree

###################################################################################################
def write_reann(atoms, filename, index):
    line1 = 'point = \t{}'.format(index)

    cell = '\n'.join([''.join(['{:14}'.format(item) for item in row]) for row in atoms.cell])

    pbc = 'pbc  {}'.format('  '.join([str(elem) for elem in atoms.pbc.astype('int')]))

    pos_for = []
    forces = atoms.get_forces()
    for atom in atoms:

        pos_for.append('\t'.join([atom.symbol, str(atom.mass), ' '.join(map(lambda x: "%.8f" % x, atom.position)), ' '.join(map(lambda x: "%.8f" % x,forces[atom.index]))]))

    conf_data = '\n'.join(pos_for)

    #print(conf_data)
    ener = 'abprop:  {}'.format(str(atoms.get_potential_energy()))

    text = '\n'.join([line1, cell, pbc, conf_data, ener]) + '\n'
    filename.write(text)


###################################################################################################
parser=argparse.ArgumentParser(description='''This script finds all the OUTCAR files contained
                                              in tgz, and writes the energy and configuration
                                   into a configs.in file suitable for GSRD fitting''',
                        allow_abbrev=True)

#Set the arguments we want to implement
parser.add_argument("--dir", help="base directory for the resursive search of VASP output files (default: current directory")
parser.add_argument("--output", help="name for the output file (default: config.out)")
parser.add_argument("--existing_confs", help="number of existing conf in current configuation file  (default: 0")


#Apply the arguments so they can be used
args=parser.parse_args()

#Set the folder from which OUTCAR (tgz) files will be searched recursively
if args.dir:
    print(args.dir)
    base_dir=os.path.expanduser(args.dir)
    print("Searching from {} directory".format(base_dir))
else:
    base_dir=os.getcwd()
    print("Searching from current directory: {}".format(base_dir))

# Set the name of the output file received as argument
if args.output:
    outfile=str(args.output)
    print("Output file name set to: {}".format(outfile))
else:
    outfile="configuration"
    print("Using default name for output file: {}".format(outfile))


#Set the initial number for the first conf in the configuration file
if args.first_file:
    numconfs=args.existing_confs+1
else:
    numconfs=1
###################################################################################################

if __name__ == "__main__":
    # Set the root folder for searching OUTCARs recursively
    base_dir = os.path.abspath(base_dir)

    # Search for all files containing the OUTCAR string
    outcar_files = [y for x in os.walk(base_dir) for y in glob(os.path.join(x[0], 'OUTCAR*'))]

    # Opend file in append mode if numfiles provided, else in write mode
    if numconfs != 1:
        output_file = open(outfile, 'a')
    else:
        output_file = open(outfile, 'w')


    # Read configurations from every OUTCAR file and write in REANN configuration format
    for file in sorted(outcar_files):                               # loop over the list of outcar files
        (folder, filename) = os.path.split(file)
        print(folder, filename)
        os.chdir(folder)
        for conf in iread(filename, index=':', format="vasp-out"):  # load OUTCAR file using ASE module
            write_reann(conf, output_file, numfiles)
            numconfs += 1

        os.chdir(base_dir)
