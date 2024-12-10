# QmQ

## Drawing a qubit

## Running simulation

### Environment

```
export ANSYSEM_ROOT241=/opt/AnsysEM/v241/Linux64/
export LD_LIBRARY_PATH=$ANSYSEM_ROOT241/common/mono/Linux64/lib64:$ANSYSEM_ROOT241/Delcross:$LD_LIBRARY_PATH
source pyaedt/bin/activate
```

### Running

```
python3 m3d.py
```


### Other useful commands

```
python3 -m venv pyaedt
ps -aux | grep ansysedt
```

## Estimating capacitance

```
python3 capacitance.py
```