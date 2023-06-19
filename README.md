# nordcrutchnectok

`nordcrutchnectok` is wrapper over [`nordvpn`](https://github.com/NordSecurity/nordvpn-linux). It helps to find working servers and keep connections.

[Previous version with manual configuration nordvpn](https://github.com/The220th/nordcrutchnector).

# Set up nordvpn

- Install app `nordvpn` (dont forget `> sudo usermod -aG nordvpn $USER` and `> sudo systemctl enable nordvpnd`).

- Login (`> nordvpn login`)

<!-- ``` bash
# legacy login
nordvpn login --username "username@domen.net" --passwort "you_password"
``` -->

- Configure (`> nordvpn settings`) as you need.

- Run `nordcrutchnectok`.

# Set up nordcrutchnectok

## Dependencies

``` bash
pip3 install requests argparse
```

## Install

``` bash
git clone https://github.com/the220th/nordcrutchnectok
cd nordcrutchnectok
chmod u+x ./nordcrutchnectok
echo -e "\n\nexport PATH=\$PATH:$(pwd)" >> ~/.bashrc

# restart terminal and run
nordcrutchnectok
```

# Using

``` bash
> nordcrutchnectok help
```
