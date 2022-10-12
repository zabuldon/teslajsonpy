# Changelog

<!--next-version-placeholder-->

## v3.0.0 (2022-10-12)
### Feature
* Add support for solar systems and powerwall ([#341](https://github.com/zabuldon/teslajsonpy/issues/341)) ([`5827dc9`](https://github.com/zabuldon/teslajsonpy/commit/5827dc9bda57e47dc0dafa674aeca2551582f43c))

### Breaking
* HomeAssistant specific code has been moved out. The API is now just a communication layer ([`5827dc9`](https://github.com/zabuldon/teslajsonpy/commit/5827dc9bda57e47dc0dafa674aeca2551582f43c))

## v2.4.5 (2022-10-09)
### Fix
* Fix key_error in version 2022.36 ([#351](https://github.com/zabuldon/teslajsonpy/issues/351)) ([`4deda7f`](https://github.com/zabuldon/teslajsonpy/commit/4deda7fcd282c9b8d3cfbfc5fcbe145f5e261947))

## v2.4.4 (2022-08-29)
### Fix
* Handle missing grid_status key(#346) ([`8c8f727`](https://github.com/zabuldon/teslajsonpy/commit/8c8f72728efedb29f027351caf407b1e73e914f0))

## v2.4.3 (2022-08-27)
### Fix
* Fix grid status and load sensor issues ([#343](https://github.com/zabuldon/teslajsonpy/issues/343)) ([`d815446`](https://github.com/zabuldon/teslajsonpy/commit/d815446aaba5b17363ed6ca60c07243e027d564b))

## v2.4.2 (2022-08-17)
### Fix
* Use solar name from app ([#339](https://github.com/zabuldon/teslajsonpy/issues/339)) ([`a1c3a41`](https://github.com/zabuldon/teslajsonpy/commit/a1c3a41f14b24bdeeb5206c7ad2afbaf81529fc6))

## v2.4.1 (2022-08-13)
### Fix
* Revert solar power name to prevent breaking change ([#336](https://github.com/zabuldon/teslajsonpy/issues/336)) ([`bf02629`](https://github.com/zabuldon/teslajsonpy/commit/bf02629fc7e7359339890089f4c240cfa3f17636))

### Documentation
* Update documentation ([`150f0bd`](https://github.com/zabuldon/teslajsonpy/commit/150f0bd5ae280fa109ea13441ee2eb5aee70d4ff))

## v2.4.0 (2022-08-05)
### Feature
* Add grid and load sensors ([#333](https://github.com/zabuldon/teslajsonpy/issues/333)) ([`697ff64`](https://github.com/zabuldon/teslajsonpy/commit/697ff64cbe884591bf94ca5fc88323049014f943))

## v2.3.0 (2022-07-10)
### Feature
* Update endpoints and agent to v4.10 ([`ba11467`](https://github.com/zabuldon/teslajsonpy/commit/ba114674c80c1f1a7dfe004684c5c59ae0e44c2b))

### Fix
* Switch to json request ([#321](https://github.com/zabuldon/teslajsonpy/issues/321)) ([`5bf943d`](https://github.com/zabuldon/teslajsonpy/commit/5bf943d18ffebd3c50702098990a8266f68eab6a))

## v2.2.1 (2022-05-26)
### Fix
* Improve handling on 0 Watts spurious power reads ([#317](https://github.com/zabuldon/teslajsonpy/issues/317)) ([`213a8e2`](https://github.com/zabuldon/teslajsonpy/commit/213a8e2c212e0abe55098099f3114e99c2a98761))

## v2.2.0 (2022-05-02)
### Feature
* Update endpoints.json to app version 4.7.0 ([#314](https://github.com/zabuldon/teslajsonpy/issues/314)) ([`4296ec2`](https://github.com/zabuldon/teslajsonpy/commit/4296ec2148e678a27b439e0e4d9c0e52e8577fc2))

## v2.1.0 (2022-04-26)
### Feature
* Add 3rd row heated seats ([#310](https://github.com/zabuldon/teslajsonpy/issues/310)) ([`3f65d02`](https://github.com/zabuldon/teslajsonpy/commit/3f65d0225d58d02bd54469fb234462ee1e24b3b9))

## v2.0.3 (2022-04-24)
### Fix
* Fix error for cars without heated steering wheels and seats ([`b5cf9bb`](https://github.com/zabuldon/teslajsonpy/commit/b5cf9bb2b1416364d921fcd533a55f52f8e92282))

## v2.0.2 (2022-04-24)
### Fix
* Remove duplicate ChargeStateDataSensor ([#306](https://github.com/zabuldon/teslajsonpy/issues/306)) ([`965bd9e`](https://github.com/zabuldon/teslajsonpy/commit/965bd9e831aa2cf77b49da2d3411c57b1f7a4638))

## v2.0.1 (2022-04-04)
### Fix
* Add enabled_by_default to EnergySiteDevice ([`4a098a0`](https://github.com/zabuldon/teslajsonpy/commit/4a098a04a69043111afe27faff79b8ec2ecffdc0))

## v2.0.0 (2022-03-27)
### Feature
* Add homelink support for HA ([`242eb35`](https://github.com/zabuldon/teslajsonpy/commit/242eb35603dc1872d7b3806fb59f340423ad055e))

### Fix
* Create json sensors for vehicle data ([#299](https://github.com/zabuldon/teslajsonpy/issues/299)) ([`d692a15`](https://github.com/zabuldon/teslajsonpy/commit/d692a154dd4165b3f24ba29abd6f76a78858e0b7))

### Breaking
* Online sensor will no longer have json vehicle data. Any scripts that relied on that json data will need to use the newer sensors. They will need to be enabled. ([`d692a15`](https://github.com/zabuldon/teslajsonpy/commit/d692a154dd4165b3f24ba29abd6f76a78858e0b7))

## v1.10.0 (2022-03-25)
### Feature
* Force update on next poll on enable update ([`2b6bd5d`](https://github.com/zabuldon/teslajsonpy/commit/2b6bd5d3c411e3ecd39f7ec9bb61d0de85ebdd4c))

### Fix
* Fix last_reset calculation to reset only if new value is lower ([#297](https://github.com/zabuldon/teslajsonpy/issues/297)) ([`6103eb4`](https://github.com/zabuldon/teslajsonpy/commit/6103eb4a35459abd1461da64c0ff05655c18aaa2))

## v1.9.0 (2022-03-23)
### Feature
* Update endpoints.json for version 4.5 ([#286](https://github.com/zabuldon/teslajsonpy/issues/286)) ([`c9bc30b`](https://github.com/zabuldon/teslajsonpy/commit/c9bc30ba1d5182a16c1e62946df33c6f54de3929))

### Fix
* Remove get_bearer_token step ([`e22ebf3`](https://github.com/zabuldon/teslajsonpy/commit/e22ebf377f2e7d0639cd00a9ffd1d9fb36ff904b))
* Remove get_bearer_token step ([`48dcae5`](https://github.com/zabuldon/teslajsonpy/commit/48dcae548c8653e66a94d831ad2c5f3889b5967e))

## v1.8.0 (2022-02-20)
### Feature
* Add per vehicle polling interval ([#281](https://github.com/zabuldon/teslajsonpy/issues/281)) ([`3e66dc1`](https://github.com/zabuldon/teslajsonpy/commit/3e66dc1a5a66b00e5a289271be729e4eb76779b5))

## v1.7.0 (2022-02-11)
### Feature
* Provide all data in home assistant sensor as json string ([#279](https://github.com/zabuldon/teslajsonpy/issues/279)) ([`8c2a1f3`](https://github.com/zabuldon/teslajsonpy/commit/8c2a1f38aea8e1c74e80abd9c2282bd8d0263c86))

## v1.6.0 (2022-01-18)
### Feature
* Report installed_version in update_sensor ([#274](https://github.com/zabuldon/teslajsonpy/issues/274)) ([`cf0c17d`](https://github.com/zabuldon/teslajsonpy/commit/cf0c17d287ec419b20d9812de6969e7d37cdbcb7))

### Fix
* Fix get_location() so it updates if car facing north ([#277](https://github.com/zabuldon/teslajsonpy/issues/277)) ([`784a4ed`](https://github.com/zabuldon/teslajsonpy/commit/784a4edd5e89a9035341309708c8e5ab9506e1b2))

## v1.5.0 (2022-01-14)
### Feature
* Sync endpoints.json with teslapy ([`faa4761`](https://github.com/zabuldon/teslajsonpy/commit/faa476179b6d198caaffc9dbec53a835cb496109))
* Add update_interval as an attribute ([#267](https://github.com/zabuldon/teslajsonpy/issues/267)) ([`9c622bb`](https://github.com/zabuldon/teslajsonpy/commit/9c622bba9b519cc4c4985f980dae7c5acdf9e587))
* Add polling policy flag ([#167](https://github.com/zabuldon/teslajsonpy/issues/167)) ([`43c74b0`](https://github.com/zabuldon/teslajsonpy/commit/43c74b069c288ce6eca19a832f1e2b24bab0dc8a))

## v1.4.2 (2021-12-28)
### Fix
* **vins:** Ensure vin is in saved state ([`77e2414`](https://github.com/zabuldon/teslajsonpy/commit/77e2414489088d390de81ef3eb02314f6a5921b9))
* **energysites:** Changing unknown grid status logic ([`5f92fc4`](https://github.com/zabuldon/teslajsonpy/commit/5f92fc4e466b78e78cf40bd1fb78d279bba1c09c))

### Documentation
* Update documentation ([`c5280e1`](https://github.com/zabuldon/teslajsonpy/commit/c5280e193ce4feb5148aa45efb6ac01818b5d87f))

## v1.4.1 (2021-12-08)
### Fix
* Allow specification of auth_domain ([`85babc8`](https://github.com/zabuldon/teslajsonpy/commit/85babc817c19b1274fd95c36ce059c4179d53a8c))

## v1.4.0 (2021-12-05)
### Feature
* Add Horn & FlashLight buttons ([#252](https://github.com/zabuldon/teslajsonpy/issues/252)) ([`38d644f`](https://github.com/zabuldon/teslajsonpy/commit/38d644f9d7cbc7ccfe94d5e7b2ce53ab917de073))

## v1.3.0 (2021-12-05)
### Feature
* Expose max charger variable ([#248](https://github.com/zabuldon/teslajsonpy/issues/248)) ([`9c3cce9`](https://github.com/zabuldon/teslajsonpy/commit/9c3cce90c07692e60869f18c2fd20cff043aca5d))

## v1.2.1 (2021-10-22)
### Fix
* Reduce api calls to energysite ([`ddbe6eb`](https://github.com/zabuldon/teslajsonpy/commit/ddbe6ebd001bc0c514db5f67dbd368a0046e6ece))
* Treat 408 exceptions as vehicle asleep ([`2f707d9`](https://github.com/zabuldon/teslajsonpy/commit/2f707d95e79e6f9635152baabd9d7ff4897833eb))
* Fix extraction of car_id from api call ([`4629b6f`](https://github.com/zabuldon/teslajsonpy/commit/4629b6f593ab92027440f66a7d31adfd6a9381b1))

## v1.2.0 (2021-10-20)
### Feature
* Add vin, id, and vehicle_id to online sensor ([`7f49f8f`](https://github.com/zabuldon/teslajsonpy/commit/7f49f8fd9d8931c50ff732c0fe83600fee8a4da6))

### Documentation
* Update documentation ([`e56b134`](https://github.com/zabuldon/teslajsonpy/commit/e56b13490da733fcbb874c62d4bd807cea7f8041))

## v1.1.2 (2021-10-19)
### Fix
* Exit wake_up attempt if car not identified ([`7336092`](https://github.com/zabuldon/teslajsonpy/commit/73360924d28274e7614f892da7802a7080935d17))
* Remove extraneous kwarg product_type ([`8a986eb`](https://github.com/zabuldon/teslajsonpy/commit/8a986eb6568a1960368bcdb8d137747ae9282daf))

### Documentation
* Update documentation ([`8c67ba6`](https://github.com/zabuldon/teslajsonpy/commit/8c67ba66db086b4113ce6b30be7cb8a77abd1257))
* Update documentation ([`006bc7a`](https://github.com/zabuldon/teslajsonpy/commit/006bc7a816721adfd6d4f116a2e8b7af57de240c))
* Update controller.command deprecation link ([`f17ad26`](https://github.com/zabuldon/teslajsonpy/commit/f17ad260c0e654c563a9461c8c7997374cff746e))
* Update formating of controller.api ([`186e1b1`](https://github.com/zabuldon/teslajsonpy/commit/186e1b18fdd7cb44625f1782091d4bcbe2b98010))
* Update documentation ([`54acac5`](https://github.com/zabuldon/teslajsonpy/commit/54acac549ff3045d925a7fe1a07a70380d5812e2))

## v1.1.1 (2021-10-17)
### Fix
* Fix bug when energy site name is null ([#227](https://github.com/zabuldon/teslajsonpy/issues/227)) ([`348a42b`](https://github.com/zabuldon/teslajsonpy/commit/348a42bc40f3f01863530e0eddba1b6385ebfc7c))

## v1.1.0 (2021-10-17)
### Feature
* Update to latest endpoints from 4.2.0 ([`074c35a`](https://github.com/zabuldon/teslajsonpy/commit/074c35a37cc97f27aac01181d72a13ddc3b478f1))

## v1.0.1 (2021-10-13)
### Fix
* Change product_type to kwarg ([`41ea289`](https://github.com/zabuldon/teslajsonpy/commit/41ea289cea7f83d8bc778ef017ac529754936fa0))

## v1.0.0 (2021-10-09)
### Feature
* Added support for energy sites ([#219](https://github.com/zabuldon/teslajsonpy/issues/219)) ([`e9798b7`](https://github.com/zabuldon/teslajsonpy/commit/e9798b7fdae70b177ce1537af3d2c14e6583a700))

### Breaking
* Product_type added to functions (get, post, command) to differentiate between vehicles or energy sites. data_request rename to vehicle_data_request.  ([`e9798b7`](https://github.com/zabuldon/teslajsonpy/commit/e9798b7fdae70b177ce1537af3d2c14e6583a700))

## v0.21.0 (2021-09-14)
### Feature
* Add id_token to connect() response and return correct refresh_token ([#217](https://github.com/zabuldon/teslajsonpy/issues/217)) ([`6d837ed`](https://github.com/zabuldon/teslajsonpy/commit/6d837ed1b3a9794f4e9ffc3a0c59afc33702137e))

## v0.20.0 (2021-09-04)
### Feature
* Add steering wheel and change heated seats to select ([`6ecd9df`](https://github.com/zabuldon/teslajsonpy/commit/6ecd9dfa73158b4b613aa2b26e032aea3162f10d))

### Fix
* Allow auth using refresh_token ([#211](https://github.com/zabuldon/teslajsonpy/issues/211)) ([`09b7fbe`](https://github.com/zabuldon/teslajsonpy/commit/09b7fbe1e4a5090f4620d1d3b52bf0c20de5f1f2))

## v0.19.1 (2021-09-03)
### Fix
* Update HA energy sensors ([`a14cc6f`](https://github.com/zabuldon/teslajsonpy/commit/a14cc6f9c919ef48e0bc6cbb679a5599378b2923))

## v0.19.0 (2021-08-13)
### Feature
* Add ChargingEnergySensor ([`3e3d1a3`](https://github.com/zabuldon/teslajsonpy/commit/3e3d1a384eb19cf13c07d78c2c46ea747c0c9be3))
* Add charger power ([`a5f8858`](https://github.com/zabuldon/teslajsonpy/commit/a5f885885b9586d406aef2800e613e55ff95b092))

### Fix
* Fix multiple cookies error ([`150f6e2`](https://github.com/zabuldon/teslajsonpy/commit/150f6e2d2eb880cd7ecf2306dc2ea4fe5a715f46))
* Fix multiple cookies error ([`8537158`](https://github.com/zabuldon/teslajsonpy/commit/8537158ee217e73a54592777a178abb9804906be))
* Fix casting of url for refresh_access_token ([`ba19cc1`](https://github.com/zabuldon/teslajsonpy/commit/ba19cc1d3182979d6ae49bb7606bf74853d586db))

## v0.18.3 (2021-05-01)
### Fix
* Check response before json ([#202](https://github.com/zabuldon/teslajsonpy/issues/202)) ([`2df733a`](https://github.com/zabuldon/teslajsonpy/commit/2df733a5401500298c54094de0f4e1430d600ee1))

## v0.18.2 (2021-05-01)
### Fix
* Fix attribute error in debug statement ([`48898f9`](https://github.com/zabuldon/teslajsonpy/commit/48898f9b2d981ab696dbcdfa16efa57faf10a1fd))
* Fix give up condition for command retries ([`8954299`](https://github.com/zabuldon/teslajsonpy/commit/8954299e17231e695a759abf1ba518ca0fc2b6ff))
* Fix get_authorization_code syntax ([`ef46aef`](https://github.com/zabuldon/teslajsonpy/commit/ef46aefa6e790c05d8d67f6b99329b5cec0d14ff))

## v0.18.1 (2021-05-01)
### Fix
* Fix syntax errors due to httpx ([`cea4135`](https://github.com/zabuldon/teslajsonpy/commit/cea4135aa913cdfad77fe69871e2d21e7aabc697))
* Loosen dependency requirements ([`598d600`](https://github.com/zabuldon/teslajsonpy/commit/598d60039244292cdb47bfd99f0b388c68264bb6))
* Fix initialization of heated seats ([#189](https://github.com/zabuldon/teslajsonpy/issues/189)) ([`ddde348`](https://github.com/zabuldon/teslajsonpy/commit/ddde34855635954c46269286178d8f2edfce8c19))

## v0.18.0 (2021-04-28)
### Feature
* Swap to httpx ([`5843932`](https://github.com/zabuldon/teslajsonpy/commit/58439327ab9aabf8d17b6abef45511ed3996d798))

## v0.17.1 (2021-04-03)
### Fix
* Fix china authentication ([`45dec97`](https://github.com/zabuldon/teslajsonpy/commit/45dec971b9dbeb3a70acbd96093ca5a4777be821))
* Catch keyerror for missing seatwarmers ([`9436684`](https://github.com/zabuldon/teslajsonpy/commit/9436684214be96aeedc276e859ee70e57d8e560e))

### Documentation
* Update docs ([`e9b149a`](https://github.com/zabuldon/teslajsonpy/commit/e9b149aee97c216e2f3c8cd23200152ca4a61b4f))

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
