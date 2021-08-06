# isye6739-project-summer-2021
[ISYE 6739] Project, Summer 2021

## Project Member
William Won (william.won@gatech.edu)

## How to Run
1. Install Python dependencies.
### Conda
```bash
conda install --file packagelist.txt
```

### pip
```bash
pip3 install -r requirements.txt
```

2. Change Configurations inside `configs.json`

3. Run simulation and plotter.
```bash
./run_script.sh 
```

4. The simulation results is dumped as pickle in `simlation_result/`, and the plotted graphs will be saved in `graph/`.
