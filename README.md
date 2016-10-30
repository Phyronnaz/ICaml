# ICaml
Caml Light kernel for Jupyter

## 
* Install Caml Light

https://doc.ubuntu-fr.org/caml_light

* Install the camlkernel module
```
python setup.py install
```

* Add the kernel to jupyter
```
jupyter kernelspec install --name caml-kernel `pwd`
```
**Important** we use pwd command so we should be in the icaml source directory!
