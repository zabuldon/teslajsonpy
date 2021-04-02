# Changelog

<!--next-version-placeholder-->

## v0.17.0 (2021-04-02)
### Feature
* Add heated seats switch ([#180](https://github.com/zabuldon/teslajsonpy/issues/180)) ([`69599db`](https://github.com/zabuldon/teslajsonpy/commit/69599db08678066bbd78705147399435d9f9e90b))

### Documentation
* Rebuild docs ([`7f9c154`](https://github.com/zabuldon/teslajsonpy/commit/7f9c15433195cea73f46bf903e55575fc4a75b67))

## v0.16.1 (2021-03-30)
### Fix
* Properly require updated authcaptureproxy ([`fb1b58e`](https://github.com/zabuldon/teslajsonpy/commit/fb1b58ed99697cd852b38089c420a3e52829674e))

## v0.16.0 (2021-03-29)
### Feature
* Use auth.cn as initial start ([`6b2ca52`](https://github.com/zabuldon/teslajsonpy/commit/6b2ca52f66c37fc2b8eb8b6ed07bb7bad1fa091e))

## v0.15.1 (2021-03-20)
### Fix
* Bump deps ([`601a237`](https://github.com/zabuldon/teslajsonpy/commit/601a2375c66353e5d2c5342404ef0ff8023e66c0))

## v0.15.0 (2021-03-02)
### Feature
* Add support for domain redirection ([`471ea16`](https://github.com/zabuldon/teslajsonpy/commit/471ea1609fc28890657362b06501fdfe082cddb5))

### Fix
* Fix mfa code handling ([`e005fcf`](https://github.com/zabuldon/teslajsonpy/commit/e005fcfe524fcba1f281ab826111eb92ff8f50e3))
* Increase time for waf retry ([`31b56cc`](https://github.com/zabuldon/teslajsonpy/commit/31b56cc67f1f4489119409fbc1f2470e6b850e44))
* Reset waf retry count on successful login ([`6202eed`](https://github.com/zabuldon/teslajsonpy/commit/6202eed44c7da8a492f4aa079035169765c16b22))

## v0.14.0 (2021-02-25)
### Feature
* Allow reset of proxy ([`2218c57`](https://github.com/zabuldon/teslajsonpy/commit/2218c570fb35b26a962cfff8287ac66d126fe3ab))

### Fix
* Catch code even without redirect ([`37207ce`](https://github.com/zabuldon/teslajsonpy/commit/37207cea14b19d7961f2d6f774d2ba4ffadce043))

## v0.13.0 (2021-02-20)
### Feature
* Add mfa support ([`413b585`](https://github.com/zabuldon/teslajsonpy/commit/413b585b306304e970cefd6c71182f47bdd95b52))

### Fix
* Process i18n urls ([`a4a40fd`](https://github.com/zabuldon/teslajsonpy/commit/a4a40fdf896e99fd9deea711e4aacc5e5a846f1e))

### Documentation
* Add sphinx support ([`483ddd0`](https://github.com/zabuldon/teslajsonpy/commit/483ddd099df0ecffaa7397b1dfb70d875d1d4161))

## v0.12.3 (2021-02-14)
### Fix
* Increase delay for refresh and update message ([`af78a8b`](https://github.com/zabuldon/teslajsonpy/commit/af78a8b9eed4630a0ec4889280a26403c86be09f))

## v0.12.2 (2021-02-14)
### Fix
* Fix requirement for authcaptureproxy ([`bfaccc7`](https://github.com/zabuldon/teslajsonpy/commit/bfaccc732423e37f2c1b9b97fb896cf0c1b6fd10))

## v0.12.1 (2021-02-13)
### Fix
* Bump authcaptureproxy ([`2a6635f`](https://github.com/zabuldon/teslajsonpy/commit/2a6635fb3822f04ba3e9b8ad84b0e01f2a2eae32))

## v0.12.0 (2021-02-13)
### Feature
* Add teslaproxy to capture oauth credentials ([`dd209d9`](https://github.com/zabuldon/teslajsonpy/commit/dd209d9c9f7d78b6cc2e2ca0da083054a58f0bc1))

### Documentation
* Add badges ([`02b583b`](https://github.com/zabuldon/teslajsonpy/commit/02b583b3ab4a53579bf8c68c03f03ee4405f6559))

## v0.11.5 (2021-02-02)
### Fix
* Address attribute error properly for form ([`11f59ea`](https://github.com/zabuldon/teslajsonpy/commit/11f59eaa398d70e1444151414cc5235ce68584d9))

## v0.11.4 (2021-02-02)
### Fix
* Check for existence of input field in form ([`613406e`](https://github.com/zabuldon/teslajsonpy/commit/613406e4f6bc95f7306b18e54ba47ea718b63fd8))

## v0.11.3 (2021-01-31)
### Fix
* Detect missing name/password ([`c4f8c54`](https://github.com/zabuldon/teslajsonpy/commit/c4f8c54d0149fa0b22dfcb299cb4ae6b4cbffaa3))

## v0.11.2 (2021-01-31)
### Fix
* Add bs4 as dependency for install ([`2a3c154`](https://github.com/zabuldon/teslajsonpy/commit/2a3c15488b26f116a40156bdd8e3ae0b6d24ec01))

## v0.11.1 (2021-01-31)
### Fix
* Use oauth3 login ([`487c7b4`](https://github.com/zabuldon/teslajsonpy/commit/487c7b4d3ff2cddf3bf3fdd099dc8a51ae2d4e5d))
* Fix header passing in __open ([`f193c64`](https://github.com/zabuldon/teslajsonpy/commit/f193c6439b3b6bc682e8884ec6950b44e0f0303c))

## v0.11.0 (2021-01-12)
### Feature
* Add charge limit soc ([#120](https://github.com/zabuldon/teslajsonpy/issues/120)) ([`441a72a`](https://github.com/zabuldon/teslajsonpy/commit/441a72a9f25b71cd9aecba10dab358a7f37f513f))

### Fix
* Tests.* (subpackage) exclusion from installs ([#116](https://github.com/zabuldon/teslajsonpy/issues/116)) ([`2d3ae90`](https://github.com/zabuldon/teslajsonpy/commit/2d3ae907506c8f59e32ef38fdd5b4902c2a7ab29))
