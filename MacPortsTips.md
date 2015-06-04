# Some maintenance bash tips #

```
function port-install {
  sudo port -v install -u $@
}

# Cleanup all deactivated ports (forcing the removal, hoping not to break too much)
function port-autoclean {
  sudo port installed | tail -n +2 | grep -v "(active)" | sudo xargs -n2 port -f uninstall
}

function port-reinstall {
	sudo port -v uninstall -f $@
	sudo port -v install -u $@
}
```