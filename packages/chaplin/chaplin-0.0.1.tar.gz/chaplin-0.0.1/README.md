![logo](docs/_static/logo_small.png)

---

## About chaplin

chaplin is a deep learning-based predictor of protein-chaperon interaction that works from cDNA sequence. The tool can therefore handle different DNA encodings of the same protein. It can also be used to optimize a protein to interact (or not interact) with chaperons only implementing synonimous mutations.

If you use chaplin in your research, please consider citing:


## Installation

Package installation should only take a few minutes with any of these methods (pip, source).

### Installing chaplin with pip:

We suggest to create a local conda environment where to install chaplin. it can be done with:

```sh
conda create -n chaplin
```
and activated with

```sh
conda activate chaplin
```

or

```sh
source activate chaplin
```

We also suggest to install pytorch separately following the instructions from https://pytorch.org/get-started/locally/

```sh
pip install chaplin
```

The procedure will install chaplin in your computer.

### Installing chaplin from source:

If you want to install chaplin from this repository, you need to install the dependencies first.
First, install [PyTorch](https://pytorch.org/get-started/locally/) separately following the instructions from https://pytorch.org/get-started/locally/.

Then install the other required libraries:

```sh
pip install numpy scikit-learn transformers
```

Finally, you can clone the repository with the following command:

```sh
git clone https://github.com/grogdrinker/chaplin/
```

## Usage

the pip installation will install a script called chaplin_standalone that is directly usable from command line (at least on linux and mac. Most probably on windows as well if you use a conda environemnt).

### Using the standalone
The script can take a fasta file or a sequence as input and provide a prediction as output

for a full list of options, use the command

```sh
chaplin_standalone -h
```

if you want to predict the probability of a protein cDNA, just call the standalone in predict mode with the DNA sequence as argument. The script can also take a fasta file as input instead of a single seuqence

as example

```sh
chaplin_standalone --command predict  ATGGAAGATGCTAAAAACATCAAGAAGGGTCCGGCT
```

or, for multiple sequences, do

```sh
chaplin_standalone fastaFile.fasta
```

if you want to find the optimal cDNA enocding for a protein, just call the standalone in optimize mode with the amino acid sequence as argument.


```sh
chaplin_standalone --command optimize AWESAMEPRTEINSEQENCEASINPT
```
this will give a cDNA sequence encoding for the input protein with a maximized probability of interacting with chaperons. If you want to optimize it to not interacting with chaperons, you can use the option --target_optimization, which takes as argument the probability of interaction the protein should be optimized to.


### Using chaplin into a python script

chaplin can be imported as a python module

```python
from chaplin.optimize import optimize
from chaplin.predict import run_prediction

seq = "MKYLLPTAAAGLLL"
s = optimize(target_seq=seq)
print("optimized protein cDNA:",s)
p = run_prediction(["ATGGAAGATGCTAAAAACATCAAGAAGGGTCCGGCT","ATGCGAGCAGCA"])
print("cDNA prediction:",p)
```

## Help

For bug reports, features addition and technical questions please contact gabriele.orlando@kuleuven.be
