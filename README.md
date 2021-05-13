# rocketnotion
Service for Rocketbook-Notion integration
## Setup to test notebook
* create new virtualenv
```bash
   $ virtualenv .venv
```

* activate virtualenv
```bash
   $ source .venv/bin/activate
```

* load dependencies
```bash
   $ pip install -r requirements.txt
```

* unizp MNIST dataset
```bash
   $ cd data
   $ unzip *.zip
   $ cd ..
```

* lauch notebook
```bash
   $ jupyter-notebook
```
## Plots generated with `altair`
You can find the plot corresponding to specific notebook in `plot` folder
