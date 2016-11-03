# ICaml
Caml Light kernel for Jupyter

## 
* Install Caml Light

https://doc.ubuntu-fr.org/caml_light

* Download ICaml
```
git clone https://github.com/Phyronnaz/ICaml.git
```

* Install the camlkernel module (replace ```python``` with ```python3``` if jupyter has been installed with ```python3```)
```
python ICaml/setup.py install
```

* Add the kernel to jupyter
```
jupyter kernelspec install --name caml-kernel ICaml
```
