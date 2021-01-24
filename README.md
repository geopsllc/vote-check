# ARK Vote Reward Calculator

## Installation

Basic install:
```sh
git clone https://github.com/geopsllc/vote-check
cd vote-check
bash install.sh
nano config.py
```
- change config.py to adjust deelgate info and/or enable dutch team's api
- run with ```python3 votecheck.py vote_amount``` or ```./votecheck.py vote_amount```

## General

This is an ARK Vote Reward Calculator.
- Supports Core v2+.
- Requires Python 3.6.7 or above - native on Ubuntu 18.04.
- Async coded so api calls are made almost simultaneously.

## Changelog
### 0.2

- added option to use dutch team's api to pull and verify sharing %
- ignores delegates with vote weight over 2M and ones sharing less than 75%

### 0.1

- initial release

## Security

If you discover a security vulnerability within this package, please open an issue. All security vulnerabilities will be promptly addressed.

## Credits

- [All Contributors](../../contributors)
- [Georgi Stoyanov](https://github.com/geopsllc)

## License

- [MIT](LICENSE) © [geopsllc](https://github.com/geopsllc)
