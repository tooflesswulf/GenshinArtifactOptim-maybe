# GenshinArtifactOptim-maybe
This project is kinda a mess.

## Python Deps
`pip install numpy pandas`

## Running simulator
You can run `sim_arti_prob.py` to get the total probability of some criteria being fulfilled. Edit the file directly to try different configurations.

Top of the file `sim_arti_prob.py` contains this block:
```python
# Target information
N = 1_000_000
arti_slot = 1  # Feather
mainstat = c.statmap['ATK']
subtargs = {
    'CD': 20.2,
    'DEF': 42
}
```

- Number of trials is controlled by N
- You can change the slot you want to target to [0=Flower, 1=Feather, 2=Sands, 3=Cup, 4=Hat].
- The mainstat can be written as a string, which is converted to my internal integer representation using `c.statmap`.

- You can also specify any number of substats and minimum values in the `subtargs` dict.

With this configuration, we would see an output like:
```
Feath @ ATK
- CD >= 20.2
- DEF >= 42

P = 0.00112
```


