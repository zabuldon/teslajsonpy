# CHANGELOG



## v3.9.1 (2023-07-25)

### Build

* build(deps): bump aiohttp from 3.8.3 to 3.8.5 (#415)

Bumps [aiohttp](https://github.com/aio-libs/aiohttp) from 3.8.3 to 3.8.5.
- [Release notes](https://github.com/aio-libs/aiohttp/releases)
- [Changelog](https://github.com/aio-libs/aiohttp/blob/v3.8.5/CHANGES.rst)
- [Commits](https://github.com/aio-libs/aiohttp/compare/v3.8.3...v3.8.5)

---
updated-dependencies:
- dependency-name: aiohttp
  dependency-type: direct:production
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`5300af9`](https://github.com/zabuldon/teslajsonpy/commit/5300af99e739a0d6fe1593930ab67c51671b6748))

* build(deps): bump aiohttp from 3.8.3 to 3.8.5 in /docs (#414)

Bumps [aiohttp](https://github.com/aio-libs/aiohttp) from 3.8.3 to 3.8.5.
- [Release notes](https://github.com/aio-libs/aiohttp/releases)
- [Changelog](https://github.com/aio-libs/aiohttp/blob/v3.8.5/CHANGES.rst)
- [Commits](https://github.com/aio-libs/aiohttp/compare/v3.8.3...v3.8.5)

---
updated-dependencies:
- dependency-name: aiohttp
  dependency-type: direct:production
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`4aeb35a`](https://github.com/zabuldon/teslajsonpy/commit/4aeb35aa62124c562d67bd7187673b8348afdcf4))

* build(deps): bump pygments from 2.13.0 to 2.15.0 (#413)

Bumps [pygments](https://github.com/pygments/pygments) from 2.13.0 to 2.15.0.
- [Release notes](https://github.com/pygments/pygments/releases)
- [Changelog](https://github.com/pygments/pygments/blob/master/CHANGES)
- [Commits](https://github.com/pygments/pygments/compare/2.13.0...2.15.0)

---
updated-dependencies:
- dependency-name: pygments
  dependency-type: direct:production
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`d86130d`](https://github.com/zabuldon/teslajsonpy/commit/d86130d774ed21ee5a2ff0de18c15318cff33de9))

* build(deps): bump pygments from 2.13.0 to 2.15.0 in /docs (#412)

Bumps [pygments](https://github.com/pygments/pygments) from 2.13.0 to 2.15.0.
- [Release notes](https://github.com/pygments/pygments/releases)
- [Changelog](https://github.com/pygments/pygments/blob/master/CHANGES)
- [Commits](https://github.com/pygments/pygments/compare/2.13.0...2.15.0)

---
updated-dependencies:
- dependency-name: pygments
  dependency-type: direct:production
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`132b032`](https://github.com/zabuldon/teslajsonpy/commit/132b0328fcd723bd11d9e4ab2d738ca8a2f07f54))

### Fix

* fix: missing defaults in energysite (#417)

* Fix missing defaults in energysite

fixes
```
2023-07-24 12:56:40.749 ERROR (MainThread) [homeassistant.components.number] Error while setting up tesla_custom platform for number
Traceback (most recent call last):
  File &#34;/usr/src/homeassistant/homeassistant/helpers/entity_platform.py&#34;, line 370, in _async_setup_platform
    await asyncio.gather(*pending)
  File &#34;/usr/src/homeassistant/homeassistant/helpers/entity_platform.py&#34;, line 510, in async_add_entities
    await asyncio.gather(*tasks)
  File &#34;/usr/src/homeassistant/homeassistant/helpers/entity_platform.py&#34;, line 670, in _async_add_entity
    original_icon=entity.icon,
                  ^^^^^^^^^^^
  File &#34;/config/custom_components/tesla_custom/number.py&#34;, line 142, in icon
    return icon_for_battery_level(battery_level=self.native_value)
                                                ^^^^^^^^^^^^^^^^^
  File &#34;/config/custom_components/tesla_custom/number.py&#34;, line 122, in native_value
    return self._energysite.backup_reserve_percent
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File &#34;/usr/local/lib/python3.11/site-packages/teslajsonpy/energy.py&#34;, line 137, in backup_reserve_percent
    return self._battery_data.get(&#34;backup&#34;).get(&#34;backup_reserve_percent&#34;)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: NoneType object has no attribute get```

* fix: empty ([`47b0dc4`](https://github.com/zabuldon/teslajsonpy/commit/47b0dc45c1ec30eda9a1797e657903931095ec32))

* fix: Avoid retries when car is unavailable with wake_if_asleep=False (#416)

Curerntly we would retry on 408s even if wake_if_asleep was False which
slowed down startup a lot for cars we did not wake ([`60ede4e`](https://github.com/zabuldon/teslajsonpy/commit/60ede4eec0d9440ed17e8e30f8d707795f2d5cac))

### Performance

* perf(httpx): avoid bytes to text conversion overhead

orjson can decode bytes directly without the need to convert
it to text first ([`ed3ebe1`](https://github.com/zabuldon/teslajsonpy/commit/ed3ebe1c994d8289cfbefada964be0f1d7877345))

### Unknown

* Merge pull request #418 from zabuldon/dev

chore: release 2023-07-24 ([`2dc54e9`](https://github.com/zabuldon/teslajsonpy/commit/2dc54e9f870749bd9e79687e33270a04cb6e7293))


## v3.9.0 (2023-06-12)

### Build

* build(deps): bump requests from 2.28.2 to 2.31.0

Bumps [requests](https://github.com/psf/requests) from 2.28.2 to 2.31.0.
- [Release notes](https://github.com/psf/requests/releases)
- [Changelog](https://github.com/psf/requests/blob/main/HISTORY.md)
- [Commits](https://github.com/psf/requests/compare/v2.28.2...v2.31.0)

---
updated-dependencies:
- dependency-name: requests
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`1e9d686`](https://github.com/zabuldon/teslajsonpy/commit/1e9d686a409f6edc907440c30a4bbdf7fc2b6ef5))

### Feature

* feat: add new heated steering wheel controls (#408) ([`a8ec439`](https://github.com/zabuldon/teslajsonpy/commit/a8ec439eac3215b28712ec1d3bd45e16aae9ef7a))

### Unknown

* Merge pull request #409 from zabuldon/dev

chore: 2023-06-11 release ([`b8ad696`](https://github.com/zabuldon/teslajsonpy/commit/b8ad696a69ca5770c7f84506838f85b9b77fd6b7))

* Merge pull request #407 from zabuldon/dependabot/pip/requests-2.31.0

build(deps): bump requests from 2.28.2 to 2.31.0 ([`cd4f544`](https://github.com/zabuldon/teslajsonpy/commit/cd4f544522c422883667d07a5212ce4d42a05d5a))


## v3.8.1 (2023-04-25)

### Fix

* fix: handle missing climate_state (#404) ([`342a2ef`](https://github.com/zabuldon/teslajsonpy/commit/342a2ef03c2ccd8b4281fb815107d423f3c1bddc))

### Unknown

* Merge pull request #405 from zabuldon/dev

chore: release 2023-04-24 ([`ae39c92`](https://github.com/zabuldon/teslajsonpy/commit/ae39c92a974cd23bc35166e7a5bd71fa689c909f))


## v3.8.0 (2023-03-26)

### Feature

* feat: add energy_site_ids and vins to update to limit updating to specific devices (#402)

* Add energy_site_ids to update to limit updating to specific sites

* vins and energy_site_ids

* vins and energy_site_ids ([`e97ccaf`](https://github.com/zabuldon/teslajsonpy/commit/e97ccaf41dcc3df0dc526882a5b85c14480ac672))

### Unknown

* Merge pull request #403 from zabuldon/dev

feat: add energy_site_ids and vins to update to limit updating to spe… ([`eef70aa`](https://github.com/zabuldon/teslajsonpy/commit/eef70aa9e8ec6d7b937924a9e1f6d33cf8290038))


## v3.7.5 (2023-03-21)

### Fix

* fix: update endpoints.json for sharing (#399)

I believe this will fix the navigation issue highlighted by Brian Gates and documented at https://tesla-api.timdorr.com/vehicle/commands/sharing ([`e46d0d9`](https://github.com/zabuldon/teslajsonpy/commit/e46d0d968024107f7897dbb27387bf34a1fa0b87))

### Unknown

* Merge pull request #400 from zabuldon/dev

fix: update endpoints.json for sharing (#399) ([`ee8d8be`](https://github.com/zabuldon/teslajsonpy/commit/ee8d8be063b3191a3e2cc6fba290f463f5369b9b))


## v3.7.4 (2023-03-05)

### Fix

* fix: fix processing or httpx response for orjson ([`e34126f`](https://github.com/zabuldon/teslajsonpy/commit/e34126fa8c9b6f3264a77d6c6ed592d0c56a90f8))

### Unknown

* Merge pull request #397 from zabuldon/dev

2023-03-04a ([`92b4907`](https://github.com/zabuldon/teslajsonpy/commit/92b490730f84adcc7bd854f6e2a51e9ed6242697))

* Merge pull request #396 from alandtse/dev

fix: fix processing or httpx response for orjson ([`925c56e`](https://github.com/zabuldon/teslajsonpy/commit/925c56e0ef47bce4771e9a46d102a650dae58694))


## v3.7.3 (2023-03-05)

### Fix

* fix: convert to orjson ([`0f94eca`](https://github.com/zabuldon/teslajsonpy/commit/0f94ecab9c78f7151621a0194f7f7cbe57c331f5))

### Style

* style: fix pylint errors ([`8aea14a`](https://github.com/zabuldon/teslajsonpy/commit/8aea14a7396a4571fe9b81394c3e8bd62bc52fd0))

* style: isort and black ([`8ec7f91`](https://github.com/zabuldon/teslajsonpy/commit/8ec7f91972a8c333dd50671e3a37bb8c97140b1f))

### Test

* test: fix test docstrings ([`06a3a61`](https://github.com/zabuldon/teslajsonpy/commit/06a3a6102b9db90b388ea1792574806c68688239))

### Unknown

* Merge pull request #395 from zabuldon/dev

2023-03-04 ([`bfe7ac6`](https://github.com/zabuldon/teslajsonpy/commit/bfe7ac696ec3f221b4917b680d49ecb4d9d249d8))

* Merge pull request #394 from alandtse/dev

chore: sync Dev ([`e903cab`](https://github.com/zabuldon/teslajsonpy/commit/e903cab934eb9c71976bb4678cc9d54ec26b02ca))

* Merge branch &#39;dev&#39; of github.com:zabuldon/teslajsonpy into dev ([`cda2dba`](https://github.com/zabuldon/teslajsonpy/commit/cda2dba1066442bf04f74dada7a231fd9808ed26))


## v3.7.2 (2023-01-12)

### Fix

* fix: Replace charge_amps with charge_current_request in set_charging_amps (#392) ([`316b9e6`](https://github.com/zabuldon/teslajsonpy/commit/316b9e6ec63004520c171b9f6e58e0d9f091adb6))

### Unknown

* Merge pull request #393 from zabuldon/dev

fix: Replace charge_amps with charge_current_request in set_charging_… ([`01be973`](https://github.com/zabuldon/teslajsonpy/commit/01be97305b87a17dcfc31c47a9bf64cc5daa73b9))


## v3.7.1 (2022-12-29)

### Build

* build(deps): bump setuptools from 65.4.1 to 65.5.1 in /docs

Bumps [setuptools](https://github.com/pypa/setuptools) from 65.4.1 to 65.5.1.
- [Release notes](https://github.com/pypa/setuptools/releases)
- [Changelog](https://github.com/pypa/setuptools/blob/main/CHANGES.rst)
- [Commits](https://github.com/pypa/setuptools/compare/v65.4.1...v65.5.1)

---
updated-dependencies:
- dependency-name: setuptools
  dependency-type: direct:production
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`2c6a058`](https://github.com/zabuldon/teslajsonpy/commit/2c6a0584978c94b0aa8bb1b6fee04389825d9560))

### Fix

* fix: handle unavailable option codes (#390) ([`4e8a3a0`](https://github.com/zabuldon/teslajsonpy/commit/4e8a3a08966f21b4740cbfcf940998cdc1f8bc97))

### Unknown

* Merge pull request #391 from zabuldon/dev

2022-12-29 ([`66dbe95`](https://github.com/zabuldon/teslajsonpy/commit/66dbe95003f21f65ed4c4db89c5848a86256eeec))

* Merge branch &#39;dev&#39; of github.com:zabuldon/teslajsonpy into dev ([`9b7ddfc`](https://github.com/zabuldon/teslajsonpy/commit/9b7ddfc19177ff4776f93d688636870e22a8455b))

* Merge pull request #388 from zabuldon/dependabot/pip/docs/setuptools-65.5.1

build(deps): bump setuptools from 65.4.1 to 65.5.1 in /docs ([`f10c3b0`](https://github.com/zabuldon/teslajsonpy/commit/f10c3b0a772bc2e6208ce6af88e2864f5b26357b))


## v3.7.0 (2022-12-26)

### Feature

* feat: include TeslaExceptions for api retries (#382) ([`63700b9`](https://github.com/zabuldon/teslajsonpy/commit/63700b92dc57f05d99f38c51514146085519a636))

### Unknown

* Merge pull request #387 from zabuldon/dev

feat: include TeslaExceptions for api retries (#382) ([`8c2a45a`](https://github.com/zabuldon/teslajsonpy/commit/8c2a45a3fc9c0d6f86358664da633145926e9b2f))


## v3.6.0 (2022-12-21)

### Ci

* ci: change docs to dispatch ([`8477106`](https://github.com/zabuldon/teslajsonpy/commit/8477106ee19cf9fe4d77e26f8fb513e87cf3ad05))

### Documentation

* docs: update docs ([`c917165`](https://github.com/zabuldon/teslajsonpy/commit/c91716577a0d88e4107f1d63330b67b7321901ef))

### Feature

* feat: add pedestrian speaker and remote_boombox (#385) ([`81cbb13`](https://github.com/zabuldon/teslajsonpy/commit/81cbb136d2d928f0a09400ebe6e0f5db65c2f619))

### Unknown

* Merge pull request #386 from zabuldon/dev

2022-12-20 ([`a39a2b0`](https://github.com/zabuldon/teslajsonpy/commit/a39a2b05499d39934000ae81f243cb3eea505f36))


## v3.5.1 (2022-12-11)

### Fix

* fix: fix typo in wake_up call (#383) ([`5209e0a`](https://github.com/zabuldon/teslajsonpy/commit/5209e0a6ad6a3dc8eec1ea71536ad4fd41fe518f))

### Unknown

* Merge pull request #384 from zabuldon/dev

fix: fix typo in wake_up call (#383) ([`9c74948`](https://github.com/zabuldon/teslajsonpy/commit/9c74948a287de6e2cfdbcab239cf7d3d35c4a0d5))


## v3.5.0 (2022-12-10)

### Build

* build(deps): bump certifi from 2022.9.24 to 2022.12.7

Bumps [certifi](https://github.com/certifi/python-certifi) from 2022.9.24 to 2022.12.7.
- [Release notes](https://github.com/certifi/python-certifi/releases)
- [Commits](https://github.com/certifi/python-certifi/compare/2022.09.24...2022.12.07)

---
updated-dependencies:
- dependency-name: certifi
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`0f29df5`](https://github.com/zabuldon/teslajsonpy/commit/0f29df5da0e57a92e746ce5a2335f75b937c65f8))

### Feature

* feat: add active route properties (#376) ([`14b20d7`](https://github.com/zabuldon/teslajsonpy/commit/14b20d7a726b15f1a55d6e89213491f7d241cd6c))

* feat: add scheduled charging (#360)

closes #370 ([`f68b928`](https://github.com/zabuldon/teslajsonpy/commit/f68b928ba285a1aec48a3c3cd07128650c94a9cc))

### Fix

* fix: Improve wake up retry logic (#379)

* fix: Improve wake up retry logic

* fix get_vehicle_summary

* handle 408 if asleep for non-waking command ([`31de243`](https://github.com/zabuldon/teslajsonpy/commit/31de243afe5e3b568f8bd1fe389e09ee950af84f))

* fix: wake car only when necessary (#378)

This strategically checks if some commands would be pointless if the car is asleep, and sets wake_if_asleep accordingly. ([`20f309e`](https://github.com/zabuldon/teslajsonpy/commit/20f309e10817924f20adbbf0fbc296975f7bf633))

* fix: fix valet mode parameter (#377)

* wrong valet mode parameter name

* docstring ([`c419a04`](https://github.com/zabuldon/teslajsonpy/commit/c419a04c9988367e080b99ee45ad092e4f6d8b0e))

### Unknown

* Merge pull request #381 from zabuldon/dev

2022-12-09 ([`d6d90e4`](https://github.com/zabuldon/teslajsonpy/commit/d6d90e479e00179dbd341eab23bb860649ca4c20))

* Merge pull request #380 from zabuldon/dependabot/pip/certifi-2022.12.7

build(deps): bump certifi from 2022.9.24 to 2022.12.7 ([`5e22d8e`](https://github.com/zabuldon/teslajsonpy/commit/5e22d8e1bfee94814ed81fdf07a5f039be925dbc))


## v3.4.1 (2022-12-05)

### Fix

* fix: add Valet mode optional argument (#374)

* add valet mode command and property

* adj params

* add param test

* update valet_mode arguments

* duplicate test ([`535c988`](https://github.com/zabuldon/teslajsonpy/commit/535c988d4699d009b4fa6bfb3599463241d605fb))

### Unknown

* Merge pull request #375 from zabuldon/dev

fix: add Valet mode optional argument (#374) ([`b389fe2`](https://github.com/zabuldon/teslajsonpy/commit/b389fe2771c98a8f8409062ea90ec79313664ee8))


## v3.4.0 (2022-12-02)

### Feature

* feat: add auto seat climate command and properties (#371) ([`21c5ff3`](https://github.com/zabuldon/teslajsonpy/commit/21c5ff3306d3caee48fa5062bb6194be1471f51a))

### Unknown

* Merge pull request #372 from zabuldon/dev

feat: add auto seat climate command and properties (#371) ([`34a6e0d`](https://github.com/zabuldon/teslajsonpy/commit/34a6e0dd551a822e716b19dcc296cdab1748ae66))


## v3.3.0 (2022-11-30)

### Feature

* feat: add remote start command (#367)

* add window control

* add tests and update authors

* tweaks after testing

* missing s in function names

* fix boolean and lat lon parameters

* window open to window close

* add remote start command

* update command response, add parameter ([`350f48b`](https://github.com/zabuldon/teslajsonpy/commit/350f48b47fbd885c452081a1ecf6ecc71b491e11))

* feat: add valet mode command and property (#368)

* add valet mode command and property

* adj params

* add param test ([`5e7c69f`](https://github.com/zabuldon/teslajsonpy/commit/5e7c69f848515b0d72362daaac28824081751878))

### Unknown

* Merge pull request #369 from zabuldon/dev

2022-11-29 ([`a34e240`](https://github.com/zabuldon/teslajsonpy/commit/a34e24070f2d5870971f2546eb1fbf88f250496b))


## v3.2.2 (2022-11-22)

### Fix

* fix: handle unavailable sites/vehicles (#365) ([`2daef7b`](https://github.com/zabuldon/teslajsonpy/commit/2daef7b3a7fbdbceb082749abec2386f6d97d556))

### Unknown

* Merge pull request #366 from zabuldon/dev

fix: handle unavailable sites/vehicles (#365) ([`6e015d0`](https://github.com/zabuldon/teslajsonpy/commit/6e015d08ed56a9c0fa7d517e7d14121d6a42134b))


## v3.2.1 (2022-11-21)

### Fix

* fix: keep existing vehicle config when asleep/offline (#363) ([`92774e9`](https://github.com/zabuldon/teslajsonpy/commit/92774e975d9a5f3438d30c330f9e31481fc7b915))

### Unknown

* Merge pull request #364 from zabuldon/dev

fix: keep existing vehicle config when asleep/offline (#363) ([`63827ae`](https://github.com/zabuldon/teslajsonpy/commit/63827aecad25f5b666355002358e44aa8efd7abd))


## v3.2.0 (2022-11-20)

### Feature

* feat: Add usable_battery_level method in TeslaCar #361 ([`abf0d08`](https://github.com/zabuldon/teslajsonpy/commit/abf0d085ac1b6b26b85f081b838dc72abfe616b2))

### Unknown

* Merge pull request #362 from zabuldon/dev

feat: Add usable_battery_level method in TeslaCar #361 ([`6e72cd5`](https://github.com/zabuldon/teslajsonpy/commit/6e72cd5637467dae51a99f5d7094dfd82fff8eb1))


## v3.1.0 (2022-11-02)

### Build

* build: update deps ([`fc11ec1`](https://github.com/zabuldon/teslajsonpy/commit/fc11ec142b53f5c361471d117ef541ff792be994))

### Ci

* ci: add lint pr action ([`b35cd93`](https://github.com/zabuldon/teslajsonpy/commit/b35cd936b6e5060aa9b05bb53eb7970cfed08f19))

### Feature

* feat: Add window control and binary sensor (#357)

* add window control

* add tests and update authors

* tweaks after testing

* missing s in function names

* fix boolean and lat lon parameters

* window open to window close ([`29fabf7`](https://github.com/zabuldon/teslajsonpy/commit/29fabf726bc589dacf2c3fc6cd8432a776eaf6d9))

* feat: add tpms, door and window properties ([`e66ff45`](https://github.com/zabuldon/teslajsonpy/commit/e66ff45d817a1b2db705b3e00a5515e6ea46f733))

### Fix

* fix: check energysite_id in _grid_status_unknown

May resolve https://github.com/alandtse/tesla/issues/290 ([`d828ab4`](https://github.com/zabuldon/teslajsonpy/commit/d828ab4978e645094af9b595b99af4e20ce01ce1))

### Unknown

* Merge pull request #359 from zabuldon/dev

2022-11-01 ([`3e14ceb`](https://github.com/zabuldon/teslajsonpy/commit/3e14ceba85ace4f1ebd2e2dd6d144b9d2fda0f0a))

* Merge pull request #356 from shred86/add-tpms-doors-windows

feat: add tpms, door and window properties ([`3adef73`](https://github.com/zabuldon/teslajsonpy/commit/3adef7345e0dd781c4d046466d949add8ffaf2e0))

* Merge pull request #355 from alandtse/dev

fix: check energysite_id in _grid_status_unknown ([`e040387`](https://github.com/zabuldon/teslajsonpy/commit/e040387cc7258a78af8fe61184d15e4f6a1814f2))


## v3.0.0 (2022-10-12)

### Breaking

* feat!: add support for solar systems and powerwall (#341)

- New module `car.py` that contains a `TeslaCar` class.
- New module `energy.py` that contains energy site classes.
- New method `Controller.generate_car_objects` that generates `TeslaCar` objects and stores them into `self.cars` by vin.
- New method `Controller.generate_energysite_objects` that generates `SolarSite`, `PowerwallSite` or `SolarPowerwallSite` objects and stores them in the `self.energysites` dictionary by `energysite_id`.
- Modified `Controller.update` to now just send a single request to the `PRODUCT_LIST` endpoint (instead of both `PRODUCT_LIST` and `VEHICLE_LIST` to get all products on a Tesla account. From there, create a list of cars `self._vehicle_list` and energy sites `self._energysite_list`.
- Storing JSON responses as-is into their own dictionary by VIN for cars and energysite_id for energysites. These are then passed to `TeslaCar` and `EnergySite` when instantiated.
- Added `include_vehicles` and `include_energysites` arguments to `Controller.connect` which default to True. This provides the option to completely ignore vehicles or energysites.
- Removed `Controller.command`, `Controller.get` and `Controller.post` methods. Only `Controller._wake_up` was using `post` which now uses `Controller.api`.
- Removed all Home Assistant specific modules.
- Removed some unused code specific to energy sites.
- Changes to some naming to try to better align with what the Tesla API uses.

closes #348
closes #334 
closes #24 

BREAKING CHANGE: HomeAssistant specific code has been moved out. The API is now just a communication layer

Co-authored-by: Alan D. Tse &lt;alandtse@gmail.com&gt; ([`5827dc9`](https://github.com/zabuldon/teslajsonpy/commit/5827dc9bda57e47dc0dafa674aeca2551582f43c))

### Unknown

* Merge pull request #353 from zabuldon/dev

feat!: add support for solar systems and powerwall (#341) ([`085a6e1`](https://github.com/zabuldon/teslajsonpy/commit/085a6e12e61eee1650073347e7357d8147c33085))


## v2.4.5 (2022-10-09)

### Ci

* ci: fix name for build_docs ([`f19bc40`](https://github.com/zabuldon/teslajsonpy/commit/f19bc40841aefd8ca6a0f7894b5cd09047ee7aa1))

### Fix

* fix: fix key_error in version 2022.36 (#351)

* Add fix for api change in version 2022.36 (missing charge_to_max_range)

Version 2022.36 seems to not include charge_to_max_range.

This uses charge_limit_soc[_max] to determine it if charge_to_max_range is not available ([`4deda7f`](https://github.com/zabuldon/teslajsonpy/commit/4deda7fcd282c9b8d3cfbfc5fcbe145f5e261947))

### Unknown

* Merge pull request #352 from zabuldon/dev

2022-10-08 ([`07135a2`](https://github.com/zabuldon/teslajsonpy/commit/07135a2a625bde477ec0e1e4a6462e9c36f8e204))


## v2.4.4 (2022-08-29)

### Ci

* ci: seperate doc building ([`8fb1bef`](https://github.com/zabuldon/teslajsonpy/commit/8fb1bef175ab39dbfd483aae68c5e2ad88710f61))

### Fix

* fix: handle missing grid_status key(#346) ([`8c8f727`](https://github.com/zabuldon/teslajsonpy/commit/8c8f72728efedb29f027351caf407b1e73e914f0))

### Unknown

* Merge pull request #347 from zabuldon/dev

2022-08-29 ([`22eb604`](https://github.com/zabuldon/teslajsonpy/commit/22eb604f9cea14406328f97c3619c5fa7bdd2483))

* Merge pull request #345 from alandtse/ci_docs

ci: seperate doc building ([`129f78b`](https://github.com/zabuldon/teslajsonpy/commit/129f78b74119ba13068e111ab2aab69e304bbf30))


## v2.4.3 (2022-08-27)

### Fix

* fix: Fix grid status and load sensor issues (#343)

closes https://github.com/alandtse/tesla/issues/254 ([`d815446`](https://github.com/zabuldon/teslajsonpy/commit/d815446aaba5b17363ed6ca60c07243e027d564b))

### Unknown

* Merge pull request #344 from zabuldon/dev

2022-08-26 ([`bbcd735`](https://github.com/zabuldon/teslajsonpy/commit/bbcd735ed19c01c1f02e4526bb19974e96315b8a))

* Change to get method ([`0c2bca6`](https://github.com/zabuldon/teslajsonpy/commit/0c2bca6d81eada926b175990903424d9e85b1239))

* Fix grid status and check for load sensors ([`1707b4e`](https://github.com/zabuldon/teslajsonpy/commit/1707b4eb450283770cb64a74b3887942e4a1d3c1))


## v2.4.2 (2022-08-17)

### Ci

* ci: unfreeze PSR ([`02c17b7`](https://github.com/zabuldon/teslajsonpy/commit/02c17b755327dff8c19f9e5178a92800712daf03))

### Fix

* fix: use solar name from app (#339)

closes #338 ([`a1c3a41`](https://github.com/zabuldon/teslajsonpy/commit/a1c3a41f14b24bdeeb5206c7ad2afbaf81529fc6))

### Unknown

* Merge pull request #340 from zabuldon/dev

2022-07-16 ([`4597754`](https://github.com/zabuldon/teslajsonpy/commit/4597754128931301e0c168b0d78a59ab1635371a))


## v2.4.1 (2022-08-13)

### Documentation

* docs: update documentation ([`150f0bd`](https://github.com/zabuldon/teslajsonpy/commit/150f0bd5ae280fa109ea13441ee2eb5aee70d4ff))

### Fix

* fix: revert solar power name to prevent breaking change (#336) ([`bf02629`](https://github.com/zabuldon/teslajsonpy/commit/bf02629fc7e7359339890089f4c240cfa3f17636))

### Unknown

* Merge pull request #337 from zabuldon/dev

fix: revert solar power name to prevent breaking change (#336) ([`78f236e`](https://github.com/zabuldon/teslajsonpy/commit/78f236eade62bd8776b77233b33aeafe790bd98f))


## v2.4.0 (2022-08-05)

### Build

* build(deps): bump mistune from 0.8.4 to 2.0.3

Bumps [mistune](https://github.com/lepture/mistune) from 0.8.4 to 2.0.3.
- [Release notes](https://github.com/lepture/mistune/releases)
- [Changelog](https://github.com/lepture/mistune/blob/master/docs/changes.rst)
- [Commits](https://github.com/lepture/mistune/compare/v0.8.4...v2.0.3)

---
updated-dependencies:
- dependency-name: mistune
  dependency-type: direct:production
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`717afe1`](https://github.com/zabuldon/teslajsonpy/commit/717afe1c36b0e4c2f64d7f963c47d2574fca8440))

* build(deps): bump mistune from 0.8.4 to 2.0.3 in /docs

Bumps [mistune](https://github.com/lepture/mistune) from 0.8.4 to 2.0.3.
- [Release notes](https://github.com/lepture/mistune/releases)
- [Changelog](https://github.com/lepture/mistune/blob/master/docs/changes.rst)
- [Commits](https://github.com/lepture/mistune/compare/v0.8.4...v2.0.3)

---
updated-dependencies:
- dependency-name: mistune
  dependency-type: direct:production
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`d5e63ef`](https://github.com/zabuldon/teslajsonpy/commit/d5e63ef4adcdcb4c7407cb419b6a2035941da43a))

### Feature

* feat: add grid and load sensors (#333) ([`697ff64`](https://github.com/zabuldon/teslajsonpy/commit/697ff64cbe884591bf94ca5fc88323049014f943))

### Unknown

* Merge pull request #335 from zabuldon/dev

2022-08-05 ([`3905dda`](https://github.com/zabuldon/teslajsonpy/commit/3905ddab7b4afcd2de727d1aafda65fa072e0b77))

* Merge pull request #332 from zabuldon/dependabot/pip/mistune-2.0.3

build(deps): bump mistune from 0.8.4 to 2.0.3 ([`efd82bf`](https://github.com/zabuldon/teslajsonpy/commit/efd82bfc3770131e858140bea7e0eb32e5ceec07))

* Merge pull request #331 from zabuldon/dependabot/pip/docs/mistune-2.0.3

build(deps): bump mistune from 0.8.4 to 2.0.3 in /docs ([`37d0961`](https://github.com/zabuldon/teslajsonpy/commit/37d09619558f9392581edb1300ad9de6042d254b))


## v2.3.0 (2022-07-10)

### Build

* build: loosen dependencies ([`7f39622`](https://github.com/zabuldon/teslajsonpy/commit/7f39622321a02e7dfeb0ea7007cede8d6d8cea6f))

* build: bump deps ([`9f7b687`](https://github.com/zabuldon/teslajsonpy/commit/9f7b6879f4bf50ee4d1aacb41468d16d1cc5b0cb))

* build(deps): bump httpx from 0.22.0 to 0.23.0

Bumps [httpx](https://github.com/encode/httpx) from 0.22.0 to 0.23.0.
- [Release notes](https://github.com/encode/httpx/releases)
- [Changelog](https://github.com/encode/httpx/blob/master/CHANGELOG.md)
- [Commits](https://github.com/encode/httpx/compare/0.22.0...0.23.0)

---
updated-dependencies:
- dependency-name: httpx
  dependency-type: direct:production
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`ab78a20`](https://github.com/zabuldon/teslajsonpy/commit/ab78a204170497f8cb112c27a0d7d1600a483485))

### Ci

* ci: use strings for version ([`d8afdf8`](https://github.com/zabuldon/teslajsonpy/commit/d8afdf8c873b598cfd33eeb833c4f37aa89537eb))

* ci: bump python version ([`5a752e9`](https://github.com/zabuldon/teslajsonpy/commit/5a752e9530607ca657eb522a22b01d451f643e67))

* ci: update workflow to use actions ([`79c93b6`](https://github.com/zabuldon/teslajsonpy/commit/79c93b651df90d93a414a9c3cbb253a01324f5db))

* ci: pin psr to v7.28.1

relekang/python-semantic-release#442 ([`f1b97ae`](https://github.com/zabuldon/teslajsonpy/commit/f1b97ae7a28e9221c4614a6898cde9af0c4d4cf8))

### Documentation

* docs: update documentation ([`8445952`](https://github.com/zabuldon/teslajsonpy/commit/8445952897fba6f762d22db384bc1cf68b6b77f3))

### Feature

* feat: update endpoints and agent to v4.10

Based on https://github.com/tdorssers/TeslaPy/commit/572a5702ad0942b9687a2de31171212ebb7fc91c ([`ba11467`](https://github.com/zabuldon/teslajsonpy/commit/ba114674c80c1f1a7dfe004684c5c59ae0e44c2b))

### Fix

* fix: switch to json request (#321)

closes #320 
closes #316 ([`5bf943d`](https://github.com/zabuldon/teslajsonpy/commit/5bf943d18ffebd3c50702098990a8266f68eab6a))

### Refactor

* refactor: alphabetize endpoints.json ([`8b4b66e`](https://github.com/zabuldon/teslajsonpy/commit/8b4b66e1f50a68d930785235cff2dfd95903c9ad))

### Unknown

* Merge pull request #329 from alandtse/tesla_4.10

build: loosen dependencies ([`6f55562`](https://github.com/zabuldon/teslajsonpy/commit/6f55562c8857d2eaaabf6be61d136c7e270de4c4))

* Merge pull request #328 from alandtse/tesla_4.10

ci: use strings for version ([`6b976f6`](https://github.com/zabuldon/teslajsonpy/commit/6b976f6beebcae9383a0027495f3d894a9f0b887))

* Merge pull request #327 from alandtse/tesla_4.10

ci: update workflow to use actions ([`b85f53d`](https://github.com/zabuldon/teslajsonpy/commit/b85f53d2d4dd8fcef0b4e174f584f6eb4db6c6a4))

* Merge pull request #326 from zabuldon/dev

ci: pin psr to v7.28.1 ([`583dc81`](https://github.com/zabuldon/teslajsonpy/commit/583dc81ff8e01c5389cee2c84e6b672015658dd3))

* Merge pull request #325 from alandtse/tesla_4.10

ci: pin psr to v7.28.1 ([`5dda13d`](https://github.com/zabuldon/teslajsonpy/commit/5dda13dd41964f00cc09d4b2f62dfdcb5936fa1e))

* Merge pull request #324 from zabuldon/dev

2022-07-09 ([`8f366c6`](https://github.com/zabuldon/teslajsonpy/commit/8f366c6bf5169b05b546b34f979df4ff38c283c1))

* Merge pull request #323 from alandtse/tesla_4.10

build: bump deps ([`87ca426`](https://github.com/zabuldon/teslajsonpy/commit/87ca426216b487f17be4b48019f717dc9e786c7e))

* Merge pull request #322 from alandtse/tesla_4.10

Tesla 4.10 ([`c011df8`](https://github.com/zabuldon/teslajsonpy/commit/c011df81ceaa3f1f45e60f32ad5c297ba723f5b3))

* Merge pull request #319 from zabuldon/dependabot/pip/httpx-0.23.0

build(deps): bump httpx from 0.22.0 to 0.23.0 ([`d48472f`](https://github.com/zabuldon/teslajsonpy/commit/d48472f2feb742860d5dbd92bdc23055ee302714))


## v2.2.1 (2022-05-26)

### Fix

* fix: improve handling on 0 Watts spurious power reads (#317)

closes #287 ([`213a8e2`](https://github.com/zabuldon/teslajsonpy/commit/213a8e2c212e0abe55098099f3114e99c2a98761))

### Unknown

* Merge pull request #318 from zabuldon/dev

fix: improve handling on 0 Watts spurious power reads (#317) ([`00af374`](https://github.com/zabuldon/teslajsonpy/commit/00af37451d1d83f90ed6fe9ad408dcab332a4ca0))


## v2.2.0 (2022-05-02)

### Feature

* feat: update endpoints.json to app version 4.7.0 (#314) ([`4296ec2`](https://github.com/zabuldon/teslajsonpy/commit/4296ec2148e678a27b439e0e4d9c0e52e8577fc2))

### Unknown

* Merge pull request #315 from zabuldon/dev

feat: update endpoints.json to app version 4.7.0 (#314) ([`8bb50e6`](https://github.com/zabuldon/teslajsonpy/commit/8bb50e6d9a5df67c862836399fc23d9fd7d41cd5))


## v2.1.0 (2022-04-26)

### Feature

* feat: add 3rd row heated seats (#310)

3rd row is disabled by default and needs to be enabled to appear. ([`3f65d02`](https://github.com/zabuldon/teslajsonpy/commit/3f65d0225d58d02bd54469fb234462ee1e24b3b9))

### Refactor

* refactor: disable heated seats and steering wheel by default (#311) ([`7931cb5`](https://github.com/zabuldon/teslajsonpy/commit/7931cb555a10441a12153426dab1e59a7c8f2af2))

### Unknown

* Merge pull request #312 from zabuldon/dev

2022-04-26 ([`7899786`](https://github.com/zabuldon/teslajsonpy/commit/789978619388a287e9c1251a442ed612afc57534))


## v2.0.3 (2022-04-24)

### Fix

* fix: fix error for cars without heated steering wheels and seats ([`b5cf9bb`](https://github.com/zabuldon/teslajsonpy/commit/b5cf9bb2b1416364d921fcd533a55f52f8e92282))

### Unknown

* Merge pull request #309 from zabuldon/dev

fix: fix error for cars without heated steering wheels and seats ([`6969dda`](https://github.com/zabuldon/teslajsonpy/commit/6969ddad6e72f3df632c69a8749c3551e680c6e7))


## v2.0.2 (2022-04-24)

### Fix

* fix: Remove duplicate ChargeStateDataSensor (#306)

Closes https://github.com/alandtse/tesla/issues/193 ([`965bd9e`](https://github.com/zabuldon/teslajsonpy/commit/965bd9e831aa2cf77b49da2d3411c57b1f7a4638))

### Unknown

* Merge pull request #307 from zabuldon/dev

fix: Remove duplicate ChargeStateDataSensor (#306) ([`fe22a9c`](https://github.com/zabuldon/teslajsonpy/commit/fe22a9c34318e9ce0288999fc95a85e40704789d))


## v2.0.1 (2022-04-04)

### Fix

* fix: add enabled_by_default to EnergySiteDevice

EnergySiteDevice ([`4a098a0`](https://github.com/zabuldon/teslajsonpy/commit/4a098a04a69043111afe27faff79b8ec2ecffdc0))

### Unknown

* Merge pull request #305 from zabuldon/dev

fix: add enabled_by_default to EnergySiteDevice ([`4be4eec`](https://github.com/zabuldon/teslajsonpy/commit/4be4eec8fd9f88aee59cbedb6030ae6d0441d8a1))


## v2.0.0 (2022-03-27)

### Breaking

* fix!: create json sensors for vehicle data (#299)

Remove json attributes from online sensor and move to separate sensors.

BREAKING CHANGE: Online sensor will no longer have json vehicle data. Any scripts that relied on that json data will need to use the newer sensors. They will need to be enabled.

closes #298 ([`d692a15`](https://github.com/zabuldon/teslajsonpy/commit/d692a154dd4165b3f24ba29abd6f76a78858e0b7))

### Feature

* feat: add homelink support for HA

Adds default-disabled homelink buttons to HA. Because Tesla now sells homelink
as optional, you will need to enable the buttons in HA to access them.

closes #295 ([`242eb35`](https://github.com/zabuldon/teslajsonpy/commit/242eb35603dc1872d7b3806fb59f340423ad055e))

### Style

* style: use typing.List for typehint to support python &lt; 3.9

This fixes a breaking change for users running python 3.8 and lower that was introduced in #299
Type-hinting the contents of a list require importing List from typing on python versions prior to 3.9 ([`af7019d`](https://github.com/zabuldon/teslajsonpy/commit/af7019d490bfb5aa71d879a64185c1c0d007682a))

### Unknown

* Merge pull request #303 from zabuldon/dev

2022-03-26 ([`b8bf18a`](https://github.com/zabuldon/teslajsonpy/commit/b8bf18a36faa18a4878c4e79d5340ff71c2a261f))


## v1.10.0 (2022-03-25)

### Build

* build(deps): bump deps (#294) ([`bfd6e34`](https://github.com/zabuldon/teslajsonpy/commit/bfd6e3483e9a206078a8db93cedbc907e98099a4))

### Feature

* feat: force update on next poll on enable update

* docs: update documentation

* style: black

* refactor: fix shifted comments

* refactor: show polling status in debug logs

* feat: force update on next poll on enable update

When set_updates enables a vehicle for controller updates. The vehicle
will update on next poll.

* build: bump deps

Co-authored-by: semantic-release &lt;semantic-release@GitHub&gt; ([`2b6bd5d`](https://github.com/zabuldon/teslajsonpy/commit/2b6bd5d3c411e3ecd39f7ec9bb61d0de85ebdd4c))

### Fix

* fix: fix last_reset calculation to reset only if new value is lower (#297)

* If the value was the same as the last update last_reset would be set
* If unknown set to None per https://developers.home-assistant.io/docs/core/entity/sensor?_highlight=last_reset#properties ([`6103eb4`](https://github.com/zabuldon/teslajsonpy/commit/6103eb4a35459abd1461da64c0ff05655c18aaa2))

### Unknown

* Merge pull request #301 from zabuldon/dev

2022-03-24 ([`f5e155b`](https://github.com/zabuldon/teslajsonpy/commit/f5e155b7d42ddb5067f5ae9f2d8588d7365f8d98))


## v1.9.0 (2022-03-23)

### Ci

* ci: add black step ([`ba0fcd9`](https://github.com/zabuldon/teslajsonpy/commit/ba0fcd9a9d36c189e7ebc0bfddb81b508fab004b))

### Feature

* feat: update endpoints.json for version 4.5 (#286)

https://github.com/tdorssers/TeslaPy/commit/f6b250edddabe1c1938665f47bfb14d54ee131f0 ([`c9bc30b`](https://github.com/zabuldon/teslajsonpy/commit/c9bc30ba1d5182a16c1e62946df33c6f54de3929))

### Fix

* fix: remove get_bearer_token step ([`e22ebf3`](https://github.com/zabuldon/teslajsonpy/commit/e22ebf377f2e7d0639cd00a9ffd1d9fb36ff904b))

* fix: remove get_bearer_token step ([`48dcae5`](https://github.com/zabuldon/teslajsonpy/commit/48dcae548c8653e66a94d831ad2c5f3889b5967e))

### Style

* style: fix typing ([`d65f988`](https://github.com/zabuldon/teslajsonpy/commit/d65f988415e50640981a135e63e02b356e5310da))

* style: fix typing ([`0bdc5a5`](https://github.com/zabuldon/teslajsonpy/commit/0bdc5a5470df9491b1b2d724bfbf98e8f93f9f67))

### Unknown

* Merge pull request #293 from zabuldon/dev

2022-03-22 ([`9c8a908`](https://github.com/zabuldon/teslajsonpy/commit/9c8a908e34d03d8223b828b1b0a383fbf20ea184))

* Merge pull request #292 from alandtse/no_bearer_token_step

No bearer token step ([`27ed3c0`](https://github.com/zabuldon/teslajsonpy/commit/27ed3c0efc2c7ae8e3a2c7726017529ad7d3d900))

* Merge pull request #291 from zabuldon/revert-289-no_bearer_token_step

Revert &#34;Remove get bearer token step&#34; ([`eb4c706`](https://github.com/zabuldon/teslajsonpy/commit/eb4c70649c461540a614e8c72a1d27d1069e8580))

* Revert &#34;Remove get bearer token step&#34; ([`ed9261b`](https://github.com/zabuldon/teslajsonpy/commit/ed9261b09f25f8b46287576e9595939710793c3e))

* Merge branch &#39;dev&#39; into master ([`aa362f5`](https://github.com/zabuldon/teslajsonpy/commit/aa362f58f0df748a5dc9df6a85e2ae436ed3c4c0))

* Merge pull request #289 from alandtse/no_bearer_token_step

Remove get bearer token step ([`a7c1190`](https://github.com/zabuldon/teslajsonpy/commit/a7c1190faf6c234540ba596532482531bc186259))


## v1.8.0 (2022-02-20)

### Feature

* feat: add per vehicle polling interval (#281)

* Add per vehicle polling interval

* Fixed lint/flake error

* Add polling interval tests

* Added tests for 2nd VIN

* Make update interval constant in const.py ([`3e66dc1`](https://github.com/zabuldon/teslajsonpy/commit/3e66dc1a5a66b00e5a289271be729e4eb76779b5))

* feat: add per vehicle polling interval (#281)

* Add per vehicle polling interval

* Fixed lint/flake error

* Add polling interval tests

* Added tests for 2nd VIN

* Make update interval constant in const.py ([`6f4d91c`](https://github.com/zabuldon/teslajsonpy/commit/6f4d91c513128be9493aff2663a1c20fdfa78078))


## v1.7.0 (2022-02-11)

### Feature

* feat: provide all data in home assistant sensor as json string (#279)

* New vehicle_data attribute for online sensor containing all the data returned as json string ([`8c2a1f3`](https://github.com/zabuldon/teslajsonpy/commit/8c2a1f38aea8e1c74e80abd9c2282bd8d0263c86))

### Unknown

* Merge pull request #280 from zabuldon/dev

feat: provide all data in home assistant sensor as json string (#279) ([`971d6be`](https://github.com/zabuldon/teslajsonpy/commit/971d6be6c0c4e9805ce0fe2c7a0fe01ab9294290))


## v1.6.0 (2022-01-18)

### Ci

* ci: allow sync with dev even with failure ([`ca7255f`](https://github.com/zabuldon/teslajsonpy/commit/ca7255fd87c0492bb61cda3f47549091c9f1bf78))

### Feature

* feat: report installed_version in update_sensor (#274)

* Always report installed_version in update_sensor

* Modify correct branch. Check for car_version ([`cf0c17d`](https://github.com/zabuldon/teslajsonpy/commit/cf0c17d287ec419b20d9812de6969e7d37cdbcb7))

### Fix

* fix: fix get_location() so it updates if car facing north (#277)

Test for changes to location were based on non-0 values which would fail if any value was 0 (such as heading north). Fix correctly treats 0 as a valid value.

closes #276 ([`784a4ed`](https://github.com/zabuldon/teslajsonpy/commit/784a4edd5e89a9035341309708c8e5ab9506e1b2))

### Unknown

* Merge pull request #278 from zabuldon/dev

2022-01-18 ([`d995784`](https://github.com/zabuldon/teslajsonpy/commit/d9957841c6a1a1b911952236f3ea3e3f50de836f))

* Merge pull request #273 from zabuldon/master

Master ([`faef3de`](https://github.com/zabuldon/teslajsonpy/commit/faef3de0f2c6c8855246708145bf14a051ee9a57))


## v1.5.0 (2022-01-14)

### Feature

* feat: sync endpoints.json with teslapy

https://github.com/tdorssers/TeslaPy/blob/7f8c86c7b501a7e59fb24e79eb8cae367b965b39/teslapy/endpoints.json ([`faa4761`](https://github.com/zabuldon/teslajsonpy/commit/faa476179b6d198caaffc9dbec53a835cb496109))

* feat: add update_interval as an attribute (#267)

* Add update_interval as an attribute

Adding &#34;update_interval&#34; as an attribute to the online-sensor, to be able to use it in automations for better control of polling

* Update tests as well ([`9c622bb`](https://github.com/zabuldon/teslajsonpy/commit/9c622bba9b519cc4c4985f980dae7c5acdf9e587))

* feat: add polling policy flag (#167)

* Adding a wake_up_policy

* Fix a few typos etc

* Rename wake_up_policy to polling_policy

* Try to be really sure that a charger is connected

* Removing backslashes (lint error)

* Removing trailing whitespace (lint warning)

* Merge with dev

* Move out calculate_interval to a helper function

* Adding tests for calculate interval

* Fix lint-complaint

* Add missing docstrings ([`43c74b0`](https://github.com/zabuldon/teslajsonpy/commit/43c74b069c288ce6eca19a832f1e2b24bab0dc8a))

### Refactor

* refactor: use helper functions (#271)

* Using helper for last_park_timestamp

* Using helper for last_wake_up_timestamp

* Update helper functions and create and update tests

* Use car_online helper functions

* Use real functions for get_drive_params in tests

* Use helper functions for climate, sentry mode and charging state

* Use helpers for id-vin mappings.  Update tests for better readability.

* Use helper function for shift_state

* Fix missing variable names and create in_gear helper

* More tests using real functions

* Missing function call

* Missing helper function

* State vs Status

* Dont reinitialize car_online on each update

* Also use set_car_online helper in wrapper

* Case insensitive wake_up

* More helper-functions in wake_up wrapper

* More debug in wake_up wrapper

* More debug in wake_up wrapper

* Fixing online-state in wrapper functions

* Debug to find missing updates

* Debug to find missing updates

* Debug to find missing updates

* Debug to find missing updates

* Better debugging

* Dont run extra wake_up if car is already awake

* More debug

* Helper functions in connect

* More debug info.  Small modification to polling policy connected

* More debug info.

* Rounding all timestamps to ints to ensure consistent behaviour

* Fix dangerous default empty dict

* Fix some tests

* Too many statements in wake_up wrapper

* Fix lint-errors

* Adding empty params to helper functions

* Rename &#34;in_gear&#34; to the more consistent &#34;is_in_gear&#34;

* Avoid using global variables in tests

* Start updating docstrings

* More docstrings

* Ensure DRIVING_INTERVAL is not overriding a low update_interval

* Fix failing test. If last_wake_up &gt;= now, the wake_up was successful ([`7ec0eb1`](https://github.com/zabuldon/teslajsonpy/commit/7ec0eb1144c3e5fdff6d5256f8fe2adf2a48e3fd))

### Unknown

* Merge pull request #272 from zabuldon/dev

2022-01-14 ([`b0e39e3`](https://github.com/zabuldon/teslajsonpy/commit/b0e39e3a3cf53cd724839da810d3c687493dd909))

* Merge pull request #270 from alandtse/teslapy_sync

feat: sync endpoints.json with teslapy ([`fc3f75e`](https://github.com/zabuldon/teslajsonpy/commit/fc3f75ec1ddb8654886bbaa6b15ff2116e775c78))

* Merge pull request #265 from zabuldon/master

Master ([`c448364`](https://github.com/zabuldon/teslajsonpy/commit/c4483640c35f6c86b6bee66cbd562c25732e4772))


## v1.4.2 (2021-12-28)

### Build

* build: bump deps ([`e644b74`](https://github.com/zabuldon/teslajsonpy/commit/e644b74b4f81102af27b18ea18f221dc4aa1c7ed))

### Documentation

* docs: update documentation ([`c5280e1`](https://github.com/zabuldon/teslajsonpy/commit/c5280e193ce4feb5148aa45efb6ac01818b5d87f))

### Fix

* fix(vins): ensure vin is in saved state ([`77e2414`](https://github.com/zabuldon/teslajsonpy/commit/77e2414489088d390de81ef3eb02314f6a5921b9))

* fix(energysites): changing unknown grid status logic ([`5f92fc4`](https://github.com/zabuldon/teslajsonpy/commit/5f92fc4e466b78e78cf40bd1fb78d279bba1c09c))

### Unknown

* Merge pull request #264 from zabuldon/dev

2021-12-27 ([`45d55aa`](https://github.com/zabuldon/teslajsonpy/commit/45d55aab7628d5740917c253cb651447cd9c26df))

* Merge pull request #262 from bassrock/fix-solarcity-energysite

fix(energysites): changing unknown grid status logic ([`5734c20`](https://github.com/zabuldon/teslajsonpy/commit/5734c20fd3915204839ed028864c8087497682d0))

* Merge pull request #263 from bassrock/fix-vin-lookup

fix(vins): ensure vin is in saved state before updating ([`52fb586`](https://github.com/zabuldon/teslajsonpy/commit/52fb58675589f5f05b93971e92dcb97ce385185c))

* Merge pull request #261 from zabuldon/dev

2021-12-12 ([`ca6b291`](https://github.com/zabuldon/teslajsonpy/commit/ca6b291dff8c317565c525c659f2fca965da382f))

* fix!(energy-sites): make name unique (#260)


BREAKING CHANGE: Sites without a name set will use the site_id instead of &#34;My Home&#34; ([`3237c1a`](https://github.com/zabuldon/teslajsonpy/commit/3237c1ae3d059f13545152e9e5cb0f63b63deb74))

* Merge pull request #258 from alandtse/auth_domain

build: bump deps ([`b46096a`](https://github.com/zabuldon/teslajsonpy/commit/b46096ab04d70dcd239bbc43943649e43c289f4d))

* Merge pull request #257 from zabuldon/master

Master ([`cc95c53`](https://github.com/zabuldon/teslajsonpy/commit/cc95c53ce6f150d0f4bb6501adb662326519f544))


## v1.4.1 (2021-12-08)

### Fix

* fix: allow specification of auth_domain

This allows China users to login with tokens. ([`85babc8`](https://github.com/zabuldon/teslajsonpy/commit/85babc817c19b1274fd95c36ce059c4179d53a8c))

### Unknown

* Merge pull request #256 from zabuldon/dev

2021-12-07 ([`ded1532`](https://github.com/zabuldon/teslajsonpy/commit/ded1532136b21eb42f44fba8ed3865ba02d401b7))

* Merge pull request #255 from alandtse/auth_domain

fix: allow specification of auth_domain ([`66b4d12`](https://github.com/zabuldon/teslajsonpy/commit/66b4d12f3542eea67abdb32ef3400ab968520412))

* Merge pull request #254 from zabuldon/master

Master ([`45db5d9`](https://github.com/zabuldon/teslajsonpy/commit/45db5d9f55e0f8494e0001c082e75a52353b045b))


## v1.4.0 (2021-12-05)

### Feature

* feat: add Horn &amp; FlashLight buttons (#252)

Co-authored-by: raphael &lt;raphael.dauchy@kwote.fr&gt; ([`38d644f`](https://github.com/zabuldon/teslajsonpy/commit/38d644f9d7cbc7ccfe94d5e7b2ce53ab917de073))

### Unknown

* Merge pull request #253 from zabuldon/dev

2021-12-05 ([`3093e34`](https://github.com/zabuldon/teslajsonpy/commit/3093e3486c67fee0b569354ca30ba0cc79a51a6c))

* Merge pull request #250 from zabuldon/master

Master ([`067f555`](https://github.com/zabuldon/teslajsonpy/commit/067f555bc97b4b1d083cc58c1408d51e2b72d190))


## v1.3.0 (2021-12-05)

### Feature

* feat: expose max charger variable (#248)

* Expose charge_current_request_max

* Update AUTHORS.md ([`9c3cce9`](https://github.com/zabuldon/teslajsonpy/commit/9c3cce90c07692e60869f18c2fd20cff043aca5d))

### Unknown

* Merge pull request #249 from zabuldon/dev

2021-12-04 ([`a7ec9d9`](https://github.com/zabuldon/teslajsonpy/commit/a7ec9d9fabb11b54c54abe7d6a9df930c0bf6345))

* Merge pull request #245 from zabuldon/master

Master ([`e57572c`](https://github.com/zabuldon/teslajsonpy/commit/e57572c98082849ecbbdbbfdc4956d4547891e15))


## v1.2.1 (2021-10-22)

### Fix

* fix: reduce api calls to energysite
Avoid spamming PRODUCT_LIST api. ([`ddbe6eb`](https://github.com/zabuldon/teslajsonpy/commit/ddbe6ebd001bc0c514db5f67dbd368a0046e6ece))

* fix: treat 408 exceptions as vehicle asleep ([`2f707d9`](https://github.com/zabuldon/teslajsonpy/commit/2f707d95e79e6f9635152baabd9d7ff4897833eb))

* fix: fix extraction of car_id from api call ([`4629b6f`](https://github.com/zabuldon/teslajsonpy/commit/4629b6f593ab92027440f66a7d31adfd6a9381b1))

### Refactor

* refactor: fix TESLA_DEFAULT_ENERGY_SITE_NAME
Fix spelling and move to const ([`2c037f2`](https://github.com/zabuldon/teslajsonpy/commit/2c037f29d879480afe10209facbf1c31813a13cc))

### Unknown

* Merge pull request #244 from zabuldon/dev

2021-10-21 ([`9d06f1f`](https://github.com/zabuldon/teslajsonpy/commit/9d06f1f2773a332383e9ebe119e4f6d8921911d7))

* Merge pull request #243 from alandtse/#408

#408 ([`e1ba0e2`](https://github.com/zabuldon/teslajsonpy/commit/e1ba0e214fc7a463443e89181f744fdafceb90a8))

* Merge pull request #242 from zabuldon/master

Master ([`363e2d0`](https://github.com/zabuldon/teslajsonpy/commit/363e2d09f87df5659b612114fa7e370f19256384))


## v1.2.0 (2021-10-20)

### Build

* build: update deps ([`69fd052`](https://github.com/zabuldon/teslajsonpy/commit/69fd052e0d637cc88fe13661c44812175df2cd26))

### Ci

* ci: add git pull ([`f75aaa3`](https://github.com/zabuldon/teslajsonpy/commit/f75aaa3c167152f09557001d3cb5e6170d18dd4c))

* ci: change order of docs build ([`f345e66`](https://github.com/zabuldon/teslajsonpy/commit/f345e66bcdd9c1159acaed9624570c1d9557868d))

### Documentation

* docs: update documentation ([`e56b134`](https://github.com/zabuldon/teslajsonpy/commit/e56b13490da733fcbb874c62d4bd807cea7f8041))

### Feature

* feat: add vin, id, and vehicle_id to online sensor ([`7f49f8f`](https://github.com/zabuldon/teslajsonpy/commit/7f49f8fd9d8931c50ff732c0fe83600fee8a4da6))

### Test

* test: add attribute tests for online sensors ([`ae6adc3`](https://github.com/zabuldon/teslajsonpy/commit/ae6adc3026765cee694519089348845aa8137606))

### Unknown

* Merge pull request #241 from zabuldon/dev

2021-10-19 ([`9846d03`](https://github.com/zabuldon/teslajsonpy/commit/9846d03b4717bb85d5820e553d54d4d02092091e))

* Merge pull request #240 from alandtse/vehicle_id

feat: add vin, id, and vehicle_id to online sensor ([`39d402d`](https://github.com/zabuldon/teslajsonpy/commit/39d402d8d801aaab36e7eddabfa4355d4dd0ad00))

* Merge pull request #239 from zabuldon/dev

2021-10-18 ci ([`99fb2a6`](https://github.com/zabuldon/teslajsonpy/commit/99fb2a6f55e00c121d0b24b5fbf6160c0abba46c))


## v1.1.2 (2021-10-19)

### Build

* build: bump deps ([`164981c`](https://github.com/zabuldon/teslajsonpy/commit/164981c129f208ba905a8c842dffaeb306af360b))

### Ci

* ci: add fetch-depth to checkout ([`9b600b4`](https://github.com/zabuldon/teslajsonpy/commit/9b600b4003b43d9d8443fa7d99787783004721a9))

* ci: add push ([`3b820ce`](https://github.com/zabuldon/teslajsonpy/commit/3b820ce3b359e6435ef2b58a6daba7afabf0f4cd))

* ci: commit doc changes ([`af15bf8`](https://github.com/zabuldon/teslajsonpy/commit/af15bf8f41ec8d49b3e9741d77360443ae158578))

### Documentation

* docs: update documentation ([`8c67ba6`](https://github.com/zabuldon/teslajsonpy/commit/8c67ba66db086b4113ce6b30be7cb8a77abd1257))

* docs: update documentation ([`006bc7a`](https://github.com/zabuldon/teslajsonpy/commit/006bc7a816721adfd6d4f116a2e8b7af57de240c))

* docs: update controller.command deprecation link ([`f17ad26`](https://github.com/zabuldon/teslajsonpy/commit/f17ad260c0e654c563a9461c8c7997374cff746e))

* docs: update formating of controller.api
Change style to work with readthedocs. ([`186e1b1`](https://github.com/zabuldon/teslajsonpy/commit/186e1b18fdd7cb44625f1782091d4bcbe2b98010))

* docs: update documentation ([`54acac5`](https://github.com/zabuldon/teslajsonpy/commit/54acac549ff3045d925a7fe1a07a70380d5812e2))

### Fix

* fix: exit wake_up attempt if car not identified
may solve https://github.com/alandtse/tesla/issues/70 ([`7336092`](https://github.com/zabuldon/teslajsonpy/commit/73360924d28274e7614f892da7802a7080935d17))

* fix: remove extraneous kwarg product_type
closes #235 ([`8a986eb`](https://github.com/zabuldon/teslajsonpy/commit/8a986eb6568a1960368bcdb8d137747ae9282daf))

### Refactor

* refactor: remove extraneous exception ([`ddbc366`](https://github.com/zabuldon/teslajsonpy/commit/ddbc36673c9774d8b024f4dfa82752d81c869f3f))

### Unknown

* Merge pull request #238 from zabuldon/master

Master ([`0e8b04f`](https://github.com/zabuldon/teslajsonpy/commit/0e8b04fd767b9b1b4fa04cb992089cf6a5992341))

* Merge pull request #237 from zabuldon/dev

2021-10-18 ([`7ebe8d6`](https://github.com/zabuldon/teslajsonpy/commit/7ebe8d672671d8e341ff9fe5c752d22b0668945f))

* Merge pull request #236 from alandtse/#235

#235 ([`61ed62d`](https://github.com/zabuldon/teslajsonpy/commit/61ed62d2cf629675fe4eaaa336c615f75bfb4adb))

* Merge pull request #234 from zabuldon/master

Master ([`05f1555`](https://github.com/zabuldon/teslajsonpy/commit/05f155546d41783adaaac14cd5ad0f00a3a00fb2))

* Merge pull request #233 from zabuldon/dev

ci: commit doc changes ([`eef272e`](https://github.com/zabuldon/teslajsonpy/commit/eef272e8aefc5c8b6475c6df0832a626cb1672d6))


## v1.1.1 (2021-10-17)

### Fix

* fix: fix bug when energy site name is null (#227)

closes https://github.com/alandtse/tesla/issues/62 ([`348a42b`](https://github.com/zabuldon/teslajsonpy/commit/348a42bc40f3f01863530e0eddba1b6385ebfc7c))

### Unknown

* Merge pull request #231 from zabuldon/dev

fix: fix bug when energy site name is null (#227) ([`47896ed`](https://github.com/zabuldon/teslajsonpy/commit/47896ed2626f2b9b56b2cb41a7f29e3f54f50a91))


## v1.1.0 (2021-10-17)

### Build

* build(deps): bump deps ([`b0df542`](https://github.com/zabuldon/teslajsonpy/commit/b0df542634fb6f4a43e2c6ed7d81c025820a8284))

### Feature

* feat: update to latest endpoints from 4.2.0

https://github.com/timdorr/tesla-api/commit/a3943cac5befd7f6b93b6e67cdd53a4b2158ac38#diff-679bae45f0015061192d880e34c9f85b835e3ba6b783b77e2b19a603b35a1773 ([`074c35a`](https://github.com/zabuldon/teslajsonpy/commit/074c35a37cc97f27aac01181d72a13ddc3b478f1))

### Refactor

* refactor: switch to api convenience function
Uses data from https://github.com/tdorssers/TeslaPy/blob/master/teslapy/endpoints.json

closes #216 ([`f40c6b3`](https://github.com/zabuldon/teslajsonpy/commit/f40c6b3d39df50a6cfd8d5c30a3c334f8fa6f701))

### Unknown

* Merge pull request #230 from zabuldon/dev

2021-10-16 ([`7903453`](https://github.com/zabuldon/teslajsonpy/commit/79034538d48ab2af458aba9152e4f1b76adc24d5))

* Merge pull request #229 from alandtse/api_convenience

Api convenience ([`b89911e`](https://github.com/zabuldon/teslajsonpy/commit/b89911e7a5b3c64fa446c3d3dab8c06eabf7524e))

* Merge pull request #228 from alandtse/api_convenience

refactor: switch to api convenience function ([`3e58c41`](https://github.com/zabuldon/teslajsonpy/commit/3e58c418a40078b4134d0da021ce92c5d37765ba))


## v1.0.1 (2021-10-13)

### Build

* build: bump deps ([`144b489`](https://github.com/zabuldon/teslajsonpy/commit/144b48970d29356a74233600d9ad4e5183d57903))

### Fix

* fix: change product_type to kwarg

Reverts API change. Sets product_type to default to vehicles and require
energy sites to specify keyword.

closes #224 ([`41ea289`](https://github.com/zabuldon/teslajsonpy/commit/41ea289cea7f83d8bc778ef017ac529754936fa0))

### Style

* style: fix lint errors (#222)

closes #221 ([`b2fa8fd`](https://github.com/zabuldon/teslajsonpy/commit/b2fa8fdd047424ed03382acaa85b5bf6b99a3024))

### Unknown

* Merge pull request #226 from zabuldon/dev

2021-10-12 ([`2e8b794`](https://github.com/zabuldon/teslajsonpy/commit/2e8b7949a927dcc72cb3dd0c30d92854563bd22c))

* Merge pull request #225 from alandtse/#224

#224 ([`74c5623`](https://github.com/zabuldon/teslajsonpy/commit/74c56231c54a7c0f29dcaafa3d2522a914fe205c))


## v1.0.0 (2021-10-09)

### Feature

* feat: added support for energy sites  (#219)

Add Solar Panel support.

BREAKING CHANGE: Product_type added to functions (get, post, command) to differentiate between vehicles or energy sites. data_request rename to vehicle_data_request. 

closes #49 
closes #212 ([`e9798b7`](https://github.com/zabuldon/teslajsonpy/commit/e9798b7fdae70b177ce1537af3d2c14e6583a700))

### Unknown

* Merge pull request #220 from zabuldon/dev

feat: added support for energy sites  (#219) ([`865283f`](https://github.com/zabuldon/teslajsonpy/commit/865283fec141190f1d0f81278052a801884a35b0))


## v0.21.0 (2021-09-14)

### Feature

* feat: add id_token to connect() response and return correct refresh_token (#217)

* Add id_token to connect() response

* Set refresh token to the one returned from auth-api and not owner api ([`6d837ed`](https://github.com/zabuldon/teslajsonpy/commit/6d837ed1b3a9794f4e9ffc3a0c59afc33702137e))

### Unknown

* Merge pull request #218 from zabuldon/dev

feat: add id_token to connect() response and return correct refresh_t… ([`694f779`](https://github.com/zabuldon/teslajsonpy/commit/694f77924df68aed810db44e5404ebd26b86766b))


## v0.20.0 (2021-09-04)

### Feature

* feat: add steering wheel and change heated seats to select

* add heating steering wheel

* Add heated steeringwheel to controller

* add type for steering wheel

* Move Heated Seats to a select

* Fix Linting, update Authors

closes #192 ([`6ecd9df`](https://github.com/zabuldon/teslajsonpy/commit/6ecd9dfa73158b4b613aa2b26e032aea3162f10d))

### Fix

* fix: allow auth using refresh_token (#211) ([`09b7fbe`](https://github.com/zabuldon/teslajsonpy/commit/09b7fbe1e4a5090f4620d1d3b52bf0c20de5f1f2))

### Unknown

* Merge pull request #215 from zabuldon/dev

2021-09-03 ([`667df48`](https://github.com/zabuldon/teslajsonpy/commit/667df4809332dad268447e2161b988e1f32b32b2))


## v0.19.1 (2021-09-03)

### Build

* build(deps): bump dependencies ([`305bc01`](https://github.com/zabuldon/teslajsonpy/commit/305bc0157bd35879ae91e8444d173f08b1305bfa))

### Fix

* fix: update HA energy sensors
Update to use state_class total_increasing based on changed api.
https://developers.home-assistant.io/blog/2021/08/16/state_class_total
Requires HA 2021.09.x ([`a14cc6f`](https://github.com/zabuldon/teslajsonpy/commit/a14cc6f9c919ef48e0bc6cbb679a5599378b2923))

### Style

* style: fix lint errors ([`71f8297`](https://github.com/zabuldon/teslajsonpy/commit/71f8297ac3282d32791bbb277572e9186e6b7bb2))

### Unknown

* Merge pull request #214 from zabuldon/dev

2021-09-03 ([`0de2755`](https://github.com/zabuldon/teslajsonpy/commit/0de2755cff1e9c646a8a97e1f5a3ab49d79cf54d))

* Merge pull request #213 from alandtse/ha_2021.09

Ha 2021.09 ([`ffbbb51`](https://github.com/zabuldon/teslajsonpy/commit/ffbbb51c3d20e77369bb1c8467159bc8a24ea8ce))


## v0.19.0 (2021-08-13)

### Feature

* feat: add ChargingEnergySensor ([`3e3d1a3`](https://github.com/zabuldon/teslajsonpy/commit/3e3d1a384eb19cf13c07d78c2c46ea747c0c9be3))

* feat: add charger power
closes #204 ([`a5f8858`](https://github.com/zabuldon/teslajsonpy/commit/a5f885885b9586d406aef2800e613e55ff95b092))

### Fix

* fix: fix multiple cookies error
Fix bug when logging in to China by proxy ([`150f6e2`](https://github.com/zabuldon/teslajsonpy/commit/150f6e2d2eb880cd7ecf2306dc2ea4fe5a715f46))

* fix: fix multiple cookies error
Fix bug when logging in to China by proxy ([`8537158`](https://github.com/zabuldon/teslajsonpy/commit/8537158ee217e73a54592777a178abb9804906be))

* fix: fix casting of url for refresh_access_token

Throws an exception when calling refresh_access_token that the URL parameter is nether a string nor a httpx.Url ([`ba19cc1`](https://github.com/zabuldon/teslajsonpy/commit/ba19cc1d3182979d6ae49bb7606bf74853d586db))

### Style

* style: fix lint errors ([`1c85c83`](https://github.com/zabuldon/teslajsonpy/commit/1c85c838db96e3ab6670fd5f39534620e1f98440))

* style: add exception for unused-private-member ([`4bd6ea8`](https://github.com/zabuldon/teslajsonpy/commit/4bd6ea8f5ce28860df3653e41794ab2360c25b9e))

### Unknown

* Merge pull request #209 from zabuldon/dev

2021-08-13 ([`d50fc46`](https://github.com/zabuldon/teslajsonpy/commit/d50fc467c00d7e6afec844f9504ff88bd13380f0))

* Merge pull request #208 from alandtse/bump_authproxy

Bump authproxy ([`570830a`](https://github.com/zabuldon/teslajsonpy/commit/570830ad4aa93bcd7d36288e7e8a22c1a32e675b))

* Merge pull request #207 from alandtse/bump_authproxy

fix: fix multiple cookies error ([`9feb45a`](https://github.com/zabuldon/teslajsonpy/commit/9feb45aefc4a5d56d4a8711aa74a0d28cdb0726f))


## v0.18.3 (2021-05-01)

### Ci

* ci: remove quotes from build command (#201) ([`e733a0a`](https://github.com/zabuldon/teslajsonpy/commit/e733a0af3ebd2e908a6d0ad215d7068dcada2af7))

### Fix

* fix: check response before json (#202)

Fixes

```
Traceback (most recent call last):
  File &#34;/usr/src/homeassistant/homeassistant/config_entries.py&#34;, line 264, in async_setup
    result = await component.async_setup_entry(hass, self)  # type: ignore
  File &#34;/usr/src/homeassistant/homeassistant/components/tesla/__init__.py&#34;, line 163, in async_setup_entry
    result = await controller.connect(
  File &#34;/usr/local/lib/python3.8/site-packages/teslajsonpy/controller.py&#34;, line 288, in connect
    cars = await self.get_vehicles()
  File &#34;/usr/local/lib/python3.8/site-packages/backoff/_async.py&#34;, line 133, in retry
    ret = await target(*args, **kwargs)
  File &#34;/usr/local/lib/python3.8/site-packages/teslajsonpy/controller.py&#34;, line 407, in get_vehicles
    return (await self.__connection.get(&#34;vehicles&#34;))[&#34;response&#34;]
  File &#34;/usr/local/lib/python3.8/site-packages/teslajsonpy/connection.py&#34;, line 90, in get
    return await self.post(command, &#34;get&#34;, None)
  File &#34;/usr/local/lib/python3.8/site-packages/teslajsonpy/connection.py&#34;, line 161, in post
    return await self.__open(
  File &#34;/usr/local/lib/python3.8/site-packages/teslajsonpy/connection.py&#34;, line 205, in __open
    data = resp.json()
  File &#34;/usr/local/lib/python3.8/site-packages/httpx/_models.py&#34;, line 1416, in json
    return jsonlib.loads(self.text, **kwargs)
  File &#34;/usr/local/lib/python3.8/json/__init__.py&#34;, line 357, in loads
    return _default_decoder.decode(s)
  File &#34;/usr/local/lib/python3.8/json/decoder.py&#34;, line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File &#34;/usr/local/lib/python3.8/json/decoder.py&#34;, line 355, in raw_decode
    raise JSONDecodeError(&#34;Expecting value&#34;, s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
``` ([`2df733a`](https://github.com/zabuldon/teslajsonpy/commit/2df733a5401500298c54094de0f4e1430d600ee1))

### Unknown

* Merge pull request #203 from zabuldon/dev

2021-05-01 ([`235f11b`](https://github.com/zabuldon/teslajsonpy/commit/235f11b0e463458e86c983e250ae3bcd910cb9dd))

* Merge pull request #200 from zabuldon/master

Master ([`0182a5d`](https://github.com/zabuldon/teslajsonpy/commit/0182a5dbc973b1500b7ad126a8485f40331435e9))


## v0.18.2 (2021-05-01)

### Ci

* ci: fix build command ([`1da98b6`](https://github.com/zabuldon/teslajsonpy/commit/1da98b6607e1f23d69d26fcc32281bcde8323314))

### Fix

* fix: fix attribute error in debug statement ([`48898f9`](https://github.com/zabuldon/teslajsonpy/commit/48898f9b2d981ab696dbcdfa16efa57faf10a1fd))

* fix: fix give up condition for command retries
Commands will no longer retry if we needs user interaction
(e.g., bad credentials) ([`8954299`](https://github.com/zabuldon/teslajsonpy/commit/8954299e17231e695a759abf1ba518ca0fc2b6ff))

* fix: fix get_authorization_code syntax ([`ef46aef`](https://github.com/zabuldon/teslajsonpy/commit/ef46aefa6e790c05d8d67f6b99329b5cec0d14ff))

### Unknown

* Merge pull request #199 from zabuldon/dev

2021-05-01 ([`e37c90d`](https://github.com/zabuldon/teslajsonpy/commit/e37c90d503a611d0573204a08171d04a5d2ced7b))

* Merge pull request #198 from alandtse/#ha_49939

fix: fix get_authorization_code syntax ([`20d356d`](https://github.com/zabuldon/teslajsonpy/commit/20d356d229b1bf3c2a6f452335341a91dcf56c21))


## v0.18.1 (2021-05-01)

### Ci

* ci: switch to semantic release action ([`4cb537f`](https://github.com/zabuldon/teslajsonpy/commit/4cb537f3bac513860c32a285462bbe36d5809f59))

### Fix

* fix: fix syntax errors due to httpx ([`cea4135`](https://github.com/zabuldon/teslajsonpy/commit/cea4135aa913cdfad77fe69871e2d21e7aabc697))

* fix: loosen dependency requirements ([`598d600`](https://github.com/zabuldon/teslajsonpy/commit/598d60039244292cdb47bfd99f0b388c68264bb6))

* fix: fix initialization of heated seats (#189)

* add heated seats switch

* fix linter errors

* add doc string

* fix linter error and add to components list

* fixing init error

* black formatting

* linter fixes ([`ddde348`](https://github.com/zabuldon/teslajsonpy/commit/ddde34855635954c46269286178d8f2edfce8c19))

### Unknown

* Merge pull request #197 from zabuldon/dev

2021-04-28 ([`024d4ec`](https://github.com/zabuldon/teslajsonpy/commit/024d4ec7f416e2b464e2003e0553c1b8401033e5))

* Merge pull request #196 from alandtse/dependencies

fix: fix syntax errors due to httpx ([`a34da72`](https://github.com/zabuldon/teslajsonpy/commit/a34da72b255dbd7817d545253fd3aaec046823eb))

* Merge pull request #195 from alandtse/dependencies

fix: loosen dependency requirements ([`11ef0fb`](https://github.com/zabuldon/teslajsonpy/commit/11ef0fbdc94d497c6d3f6f43d5fc3ce18aacce0e))

* Merge pull request #194 from alandtse/httpx

ci: switch to semantic release action ([`e5f93d1`](https://github.com/zabuldon/teslajsonpy/commit/e5f93d13ce4bed03131116f00ab64515004ec9f5))


## v0.18.0 (2021-04-28)

### Feature

* feat: swap to httpx

aiohttp appears to have issues related to Akamai Global Host.
https://github.com/aio-libs/aiohttp/issues/5643

Closes #190 ([`5843932`](https://github.com/zabuldon/teslajsonpy/commit/58439327ab9aabf8d17b6abef45511ed3996d798))

### Unknown

* Merge pull request #193 from zabuldon/dev

2021-04-28 ([`27f832f`](https://github.com/zabuldon/teslajsonpy/commit/27f832f0b4d3bec104e47feaefbb57e21c59589f))

* Merge pull request #191 from alandtse/httpx

feat: swap to httpx ([`e510361`](https://github.com/zabuldon/teslajsonpy/commit/e510361159ade24d8f01ef0373ff552d651ce65b))


## v0.17.1 (2021-04-03)

### Documentation

* docs: update docs ([`e9b149a`](https://github.com/zabuldon/teslajsonpy/commit/e9b149aee97c216e2f3c8cd23200152ca4a61b4f))

### Fix

* fix: fix china authentication ([`45dec97`](https://github.com/zabuldon/teslajsonpy/commit/45dec971b9dbeb3a70acbd96093ca5a4777be821))

* fix: catch keyerror for missing seatwarmers
#186 ([`9436684`](https://github.com/zabuldon/teslajsonpy/commit/9436684214be96aeedc276e859ee70e57d8e560e))

### Style

* style: fix lint and typing ([`f109ad8`](https://github.com/zabuldon/teslajsonpy/commit/f109ad865f972f628f6410e752c9eaa1d7522f41))

### Unknown

* Merge pull request #188 from zabuldon/dev

2021-04-03 ([`1cb8549`](https://github.com/zabuldon/teslajsonpy/commit/1cb85494dd966554b703992469ad8c10bf1d91e0))

* Merge pull request #187 from alandtse/china

fix: fix china authentication ([`22ae672`](https://github.com/zabuldon/teslajsonpy/commit/22ae67218d269a86df9fa2020904eb8c88fdfa6a))

* Merge pull request #185 from alandtse/poetry_build

docs: update docs ([`c5863a8`](https://github.com/zabuldon/teslajsonpy/commit/c5863a81eda76423f5e0c49c24150203da6d3c6b))


## v0.17.0 (2021-04-02)

### Build

* build: fix build command and republish ([`7d29af8`](https://github.com/zabuldon/teslajsonpy/commit/7d29af8f8a1fbed3493083946ef6c4215422fc6f))

* build: fix poetry building ([`148138f`](https://github.com/zabuldon/teslajsonpy/commit/148138f31f6a06db6793fbee74b947195994e66b))

* build(deps): bump requests from 2.15.1 to 2.20.0 in /docs

Bumps [requests](https://github.com/psf/requests) from 2.15.1 to 2.20.0.
- [Release notes](https://github.com/psf/requests/releases)
- [Changelog](https://github.com/psf/requests/blob/master/HISTORY.md)
- [Commits](https://github.com/psf/requests/compare/v2.15.1...v2.20.0)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`1e9a03a`](https://github.com/zabuldon/teslajsonpy/commit/1e9a03ab3061444110c5237fc73aa624c2c703ff))

* build: swap to poetry ([`a2f1725`](https://github.com/zabuldon/teslajsonpy/commit/a2f172542e69ee47dd9715dc5036dc2b21520f19))

* build: use pipenv-setup to sync ([`955aa49`](https://github.com/zabuldon/teslajsonpy/commit/955aa493a5aa512462303c4d6737868dc20b8546))

### Ci

* ci: remove sync_deps from publish ([`41a0c6e`](https://github.com/zabuldon/teslajsonpy/commit/41a0c6e7308403f456c679c546e86cd1bde02b84))

* ci: fix test and lint ([`67ba77b`](https://github.com/zabuldon/teslajsonpy/commit/67ba77bd7ddea7020ad316c235d389df5ca777cd))

* ci: change pipenv to poetry ([`78c8fe6`](https://github.com/zabuldon/teslajsonpy/commit/78c8fe6316af9f1f7bf93d8fbe9f1d9e98562ce6))

* ci: change timing of sync_deps ([`d299519`](https://github.com/zabuldon/teslajsonpy/commit/d29951923af8fad461ee37e5623beb3dfdd972df))

### Documentation

* docs: rebuild docs ([`7f9c154`](https://github.com/zabuldon/teslajsonpy/commit/7f9c15433195cea73f46bf903e55575fc4a75b67))

### Feature

* feat: add heated seats switch (#180)

* add heated seats switch

* fix linter errors

* add doc string

* fix linter error and add to components list ([`69599db`](https://github.com/zabuldon/teslajsonpy/commit/69599db08678066bbd78705147399435d9f9e90b))

### Unknown

* Merge pull request #184 from alandtse/poetry_build

build: fix build command and republish ([`5d4fe3e`](https://github.com/zabuldon/teslajsonpy/commit/5d4fe3eed0f50aae44704fde28225588f6c7589f))

* Merge pull request #183 from zabuldon/revert-182-poetry_fix

Revert &#34;build: fix poetry building&#34; ([`ee8cb58`](https://github.com/zabuldon/teslajsonpy/commit/ee8cb58143ca8db50ba0925eae5636c347491bab))

* Revert &#34;build: fix poetry building&#34; ([`7a0920e`](https://github.com/zabuldon/teslajsonpy/commit/7a0920e7fe786d892e8d1effdc9936e0517d56e5))

* Merge pull request #182 from alandtse/poetry_fix

build: fix poetry building ([`ac0e942`](https://github.com/zabuldon/teslajsonpy/commit/ac0e94285794f56debcf299712d22be8c9910761))

* Merge pull request #181 from zabuldon/dev

2021-04-01 ([`060b3be`](https://github.com/zabuldon/teslajsonpy/commit/060b3be052342a2ae4a75356a5002b254f4d23f2))

* Merge pull request #179 from zabuldon/dependabot/pip/docs/requests-2.20.0

build(deps): bump requests from 2.15.1 to 2.20.0 in /docs ([`6ab7a70`](https://github.com/zabuldon/teslajsonpy/commit/6ab7a70034d9d36ab05d268213a84bd3002ebbfa))

* Merge pull request #178 from alandtse/poetry

ci: remove sync_deps from publish ([`813da15`](https://github.com/zabuldon/teslajsonpy/commit/813da1513bd73226fd36cedee996f2e020dcecec))

* Merge pull request #177 from zabuldon/dev

2021-03-30 ([`e3eb7ba`](https://github.com/zabuldon/teslajsonpy/commit/e3eb7babcaa0570e006de67808f3092ba37e1a1b))

* Merge pull request #176 from alandtse/poetry

build: swap to poetry ([`a788e9b`](https://github.com/zabuldon/teslajsonpy/commit/a788e9b0dabbe34e65f21fbad64451cca0d73bc9))

* Merge pull request #175 from alandtse/auth.cn

ci: change timing of sync_deps ([`112c1e2`](https://github.com/zabuldon/teslajsonpy/commit/112c1e2a87ed2cdc18e1a9c2ffae67620aa2cb88))

* Merge pull request #174 from alandtse/auth.cn

Auth.cn ([`0dfee4d`](https://github.com/zabuldon/teslajsonpy/commit/0dfee4daaf930ae0eb476b4ca8abb9511a769925))


## v0.16.1 (2021-03-30)

### Fix

* fix: properly require updated authcaptureproxy ([`fb1b58e`](https://github.com/zabuldon/teslajsonpy/commit/fb1b58ed99697cd852b38089c420a3e52829674e))

### Unknown

* Merge pull request #173 from zabuldon/dev

2021-03-29 ([`97f3f18`](https://github.com/zabuldon/teslajsonpy/commit/97f3f183e6bf286a7d5d282307460a16d030935b))

* Merge pull request #172 from alandtse/auth.cn

fix: properly require updated authcaptureproxy ([`0a811d4`](https://github.com/zabuldon/teslajsonpy/commit/0a811d4c61494e1b5bddc5da1f25235d0087099c))


## v0.16.0 (2021-03-29)

### Feature

* feat: use auth.cn as initial start
Auth.cn should automatically redirect non-Chinese accounts ([`6b2ca52`](https://github.com/zabuldon/teslajsonpy/commit/6b2ca52f66c37fc2b8eb8b6ed07bb7bad1fa091e))

### Unknown

* Merge pull request #171 from zabuldon/dev

2021-03-29 ([`7be9d83`](https://github.com/zabuldon/teslajsonpy/commit/7be9d8375e5fbe4e82fd125c0cfbcad572f07e61))

* Merge pull request #170 from alandtse/auth.cn

feat: use auth.cn as initial start ([`3328de9`](https://github.com/zabuldon/teslajsonpy/commit/3328de9de52d5301dccfaa61625cf3e5636274c0))


## v0.15.1 (2021-03-20)

### Fix

* fix: bump deps
Fix issue where proxy receives non-matching host ([`601a237`](https://github.com/zabuldon/teslajsonpy/commit/601a2375c66353e5d2c5342404ef0ff8023e66c0))

### Unknown

* Merge pull request #169 from zabuldon/dev

2021-03-20 ([`bb2d0fa`](https://github.com/zabuldon/teslajsonpy/commit/bb2d0fade01830d09d2d104b69a1f00b227ad2b0))

* Merge pull request #168 from alandtse/#159

fix: bump deps ([`3be5f4a`](https://github.com/zabuldon/teslajsonpy/commit/3be5f4a7a39429b4f19842489915a737ea535001))


## v0.15.0 (2021-03-02)

### Build

* build(deps): bump aiohttp from 3.7.3 to 3.7.4 in /docs

Bumps [aiohttp](https://github.com/aio-libs/aiohttp) from 3.7.3 to 3.7.4.
- [Release notes](https://github.com/aio-libs/aiohttp/releases)
- [Changelog](https://github.com/aio-libs/aiohttp/blob/master/CHANGES.rst)
- [Commits](https://github.com/aio-libs/aiohttp/compare/v3.7.3...v3.7.4)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`f6b74a4`](https://github.com/zabuldon/teslajsonpy/commit/f6b74a4d3f256c43375caa1b9497fec5831c0097))

* build(deps): bump aiohttp from 3.7.3 to 3.7.4

Bumps [aiohttp](https://github.com/aio-libs/aiohttp) from 3.7.3 to 3.7.4.
- [Release notes](https://github.com/aio-libs/aiohttp/releases)
- [Changelog](https://github.com/aio-libs/aiohttp/blob/master/CHANGES.rst)
- [Commits](https://github.com/aio-libs/aiohttp/compare/v3.7.3...v3.7.4)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`3bd2ec6`](https://github.com/zabuldon/teslajsonpy/commit/3bd2ec675c88eba9ea5f78e915d041794519dabe))

### Feature

* feat: add support for domain redirection
China requires a different auth domain.
closes #159 ([`471ea16`](https://github.com/zabuldon/teslajsonpy/commit/471ea1609fc28890657362b06501fdfe082cddb5))

### Fix

* fix: fix mfa code handling ([`e005fcf`](https://github.com/zabuldon/teslajsonpy/commit/e005fcfe524fcba1f281ab826111eb92ff8f50e3))

* fix: increase time for waf retry ([`31b56cc`](https://github.com/zabuldon/teslajsonpy/commit/31b56cc67f1f4489119409fbc1f2470e6b850e44))

* fix: reset waf retry count on successful login ([`6202eed`](https://github.com/zabuldon/teslajsonpy/commit/6202eed44c7da8a492f4aa079035169765c16b22))

### Refactor

* refactor: fix lint errors ([`f43f2fe`](https://github.com/zabuldon/teslajsonpy/commit/f43f2fe934a9c450c4880bc316f7ae510c5f8320))

### Unknown

* Merge pull request #165 from zabuldon/dev

2021-03-01 ([`afcc0ad`](https://github.com/zabuldon/teslajsonpy/commit/afcc0adaef86b78c88bf4a643aab8745dd5c1d13))

* Merge pull request #164 from alandtse/#159

Signed-off-by: Alan Tse &lt;alandtse@gmail.com&gt; ([`395d641`](https://github.com/zabuldon/teslajsonpy/commit/395d6413c1eb3c61391200a344e1cd20db7c5849))

* Merge pull request #162 from zabuldon/dependabot/pip/aiohttp-3.7.4

Signed-off-by: Alan Tse &lt;alandtse@gmail.com&gt; ([`9653971`](https://github.com/zabuldon/teslajsonpy/commit/9653971a6df157a698d3bd183605e9af088501b4))

* Merge pull request #163 from zabuldon/dependabot/pip/docs/aiohttp-3.7.4

Signed-off-by: Alan Tse &lt;alandtse@gmail.com&gt; ([`ddd9066`](https://github.com/zabuldon/teslajsonpy/commit/ddd9066a5a57314af57dc25034ad9288f3e78aba))


## v0.14.0 (2021-02-25)

### Build

* build(deps): bump authcaptureproxy to 0.5.0 ([`dc19d15`](https://github.com/zabuldon/teslajsonpy/commit/dc19d15a91ad738cbd3cb546e11ac7639e5aa8f6))

### Feature

* feat: allow reset of proxy ([`2218c57`](https://github.com/zabuldon/teslajsonpy/commit/2218c570fb35b26a962cfff8287ac66d126fe3ab))

### Fix

* fix: catch code even without redirect ([`37207ce`](https://github.com/zabuldon/teslajsonpy/commit/37207cea14b19d7961f2d6f774d2ba4ffadce043))

### Refactor

* refactor: change waf firewall timing ([`09f490c`](https://github.com/zabuldon/teslajsonpy/commit/09f490c254a5c6e2f6c41bf1aff4b62296b84e88))

### Style

* style: fix lint error ([`dbab983`](https://github.com/zabuldon/teslajsonpy/commit/dbab9832f0ada36d89beb66ad9198b0eaa9ba64a))

### Unknown

* Merge pull request #161 from zabuldon/dev

2021-02-25 ([`55a5a22`](https://github.com/zabuldon/teslajsonpy/commit/55a5a225a21d163c909a127f3842c4b4afa7b805))

* Merge pull request #160 from alandtse/proxy_reset

Signed-off-by: Alan Tse &lt;alandtse@gmail.com&gt; ([`9712057`](https://github.com/zabuldon/teslajsonpy/commit/97120577fd2e306420fd8725e45076041bb3b15b))


## v0.13.0 (2021-02-20)

### Build

* build: remove deprecated isort setting ([`4965fac`](https://github.com/zabuldon/teslajsonpy/commit/4965fac7add0e9e1092016449d4c8a0776b650d6))

### Ci

* ci: add pipenv install ([`4b41e12`](https://github.com/zabuldon/teslajsonpy/commit/4b41e12c03bac160c3bfd5587726476de0668652))

* ci: add teslajsonpy as requirements.txt ([`fd67179`](https://github.com/zabuldon/teslajsonpy/commit/fd671791a770e2d2dbb0ff562c2327ae5562ee3e))

* ci: auto generate docs/requirements.txt ([`c32aeae`](https://github.com/zabuldon/teslajsonpy/commit/c32aeae6ccefaa195464810098a2b52650ae6052))

* ci: add docs/requirements ([`2f7d36d`](https://github.com/zabuldon/teslajsonpy/commit/2f7d36da01e15141ad7515baa9c48ee3f4a2ae6a))

### Documentation

* docs: add sphinx support ([`483ddd0`](https://github.com/zabuldon/teslajsonpy/commit/483ddd099df0ecffaa7397b1dfb70d875d1d4161))

### Feature

* feat: add mfa support
This is untested but is based on a working example.
https://github.com/timdorr/tesla-api/discussions/258 ([`413b585`](https://github.com/zabuldon/teslajsonpy/commit/413b585b306304e970cefd6c71182f47bdd95b52))

### Fix

* fix: process i18n urls ([`a4a40fd`](https://github.com/zabuldon/teslajsonpy/commit/a4a40fdf896e99fd9deea711e4aacc5e5a846f1e))

### Refactor

* refactor: move spdx-id into docstring ([`56704b8`](https://github.com/zabuldon/teslajsonpy/commit/56704b8d7920487301828dd7393065567a9304be))

### Style

* style: fix lint errors ([`7263df4`](https://github.com/zabuldon/teslajsonpy/commit/7263df42331abe681dedb85f2ba8c70e1b8206f3))

### Unknown

* Merge pull request #158 from alandtse/sphinx

ci: add pipenv install ([`12bc9a9`](https://github.com/zabuldon/teslajsonpy/commit/12bc9a9fa826661d8fca4e4e0b199989f8841bcf))

* Merge pull request #157 from zabuldon/dev

Signed-off-by: Alan Tse &lt;alandtse@gmail.com&gt; ([`d1a17ab`](https://github.com/zabuldon/teslajsonpy/commit/d1a17ab876a467f553af49d2cdc4d1b13ec35209))

* Merge pull request #156 from alandtse/sphinx

Signed-off-by: Alan Tse &lt;alandtse@gmail.com&gt; ([`351fc34`](https://github.com/zabuldon/teslajsonpy/commit/351fc34a2c8584f117a14bb60427ac395f851db3))

* bump(deps): update to authcaptureproxy==0.4.2 ([`6980d67`](https://github.com/zabuldon/teslajsonpy/commit/6980d67710a7141db40730065b17b308c4907532))

* tests: isolate mock data between tests (#155)

Mock data was previously static dictionaries shared across all TeslaMock
instances, so accidental dependencies were introduced between the tests.  Now
each mock instance has its own deep copy. ([`12c02bc`](https://github.com/zabuldon/teslajsonpy/commit/12c02bc9b394e4fc87b34536ee43cd99a8f5c6eb))

* Merge pull request #153 from alandtse/sphinx

Signed-off-by: Alan Tse &lt;alandtse@gmail.com&gt; ([`1432c04`](https://github.com/zabuldon/teslajsonpy/commit/1432c04d7039e485a36cde360ee94e505d9a5b47))

* Merge pull request #152 from alandtse/sphinx

ci: add docs/requirements ([`b26c5d9`](https://github.com/zabuldon/teslajsonpy/commit/b26c5d9a817835a1c2254920225c4d4db662f7c3))

* Merge pull request #150 from alandtse/sphinx

docs: add sphinx support ([`a0f020d`](https://github.com/zabuldon/teslajsonpy/commit/a0f020ddae7a31e6103a1a5dc9dde8784e2ef46f))


## v0.12.3 (2021-02-14)

### Build

* build(deps): update deps
typing-extension markers appeared somehow. That was breaking the ci. ([`b64602a`](https://github.com/zabuldon/teslajsonpy/commit/b64602aa9edf7ceb8cf89d5e7f0acd57ef912d3f))

### Fix

* fix: increase delay for refresh and update message
With a delay below 10 seconds, it would be a login could be interrupted
by the refresh. Increased to a minimum of 10 seconds. ([`af78a8b`](https://github.com/zabuldon/teslajsonpy/commit/af78a8b9eed4630a0ec4889280a26403c86be09f))

### Unknown

* Merge pull request #149 from zabuldon/dev

2021-02-14 ([`28f139b`](https://github.com/zabuldon/teslajsonpy/commit/28f139b3ce2de84aa0df0a51ebd0a6d4da5d4000))

* Merge pull request #148 from alandtse/ci_fix

Signed-off-by: Alan Tse &lt;alandtse@gmail.com&gt; ([`1d592ac`](https://github.com/zabuldon/teslajsonpy/commit/1d592ac83d1e759213bda0c19bdb8e54b4c656d4))

* Merge pull request #147 from alandtse/ci_fix

fix: increase delay for refresh and update message ([`7b52bd6`](https://github.com/zabuldon/teslajsonpy/commit/7b52bd649bbf4893ec6f54e46382283c9e2ecfb7))


## v0.12.2 (2021-02-14)

### Fix

* fix: fix requirement for authcaptureproxy ([`bfaccc7`](https://github.com/zabuldon/teslajsonpy/commit/bfaccc732423e37f2c1b9b97fb896cf0c1b6fd10))

### Unknown

* Merge pull request #146 from zabuldon/dev

Signed-off-by: Alan Tse &lt;alandtse@gmail.com&gt; ([`713cd00`](https://github.com/zabuldon/teslajsonpy/commit/713cd00a063d5b0c28ee580f843298bf4250899d))

* Merge pull request #145 from alandtse/ci_fix

fix: fix requirement for authcaptureproxy ([`c54561d`](https://github.com/zabuldon/teslajsonpy/commit/c54561dd296c4a546aa3fde280a738973d320bc3))


## v0.12.1 (2021-02-13)

### Ci

* ci: add typing_extensions ([`8d3565b`](https://github.com/zabuldon/teslajsonpy/commit/8d3565bb250d7f35cea0c9d7ec64f41cbb878ad9))

* ci: rename test workflow ([`97b677e`](https://github.com/zabuldon/teslajsonpy/commit/97b677e5149ec296793c120dc84680f53b34d3ee))

* ci: change pipenv install step ([`c47f17a`](https://github.com/zabuldon/teslajsonpy/commit/c47f17a41a70e66d52a48f34d7c9b951e8441185))

* ci: set timeout for tests ([`1287029`](https://github.com/zabuldon/teslajsonpy/commit/12870297c0c32278f19834ce3ac826c3f11bf92a))

* ci: add push to dev after release ([`4b6f0d6`](https://github.com/zabuldon/teslajsonpy/commit/4b6f0d6a971c417e8aeb1db4291ec0c2c9391acf))

### Fix

* fix: bump authcaptureproxy ([`2a6635f`](https://github.com/zabuldon/teslajsonpy/commit/2a6635fb3822f04ba3e9b8ad84b0e01f2a2eae32))

### Unknown

* Merge pull request #144 from zabuldon/dev

2021-02-13 ([`2f4a7b6`](https://github.com/zabuldon/teslajsonpy/commit/2f4a7b6516b8d8dae1c67b96fb4ccfd1c02c9404))

* Merge pull request #143 from alandtse/ci_fix

Signed-off-by: Alan Tse &lt;alandtse@gmail.com&gt; ([`53996e0`](https://github.com/zabuldon/teslajsonpy/commit/53996e0753ebbbd8cb1f3439f0ef91a8a7bde9ff))

* Merge pull request #142 from zabuldon/master

Signed-off-by: Alan Tse &lt;alandtse@gmail.com&gt; ([`fe30dd9`](https://github.com/zabuldon/teslajsonpy/commit/fe30dd9ee5e9f5087b9e6a4365ac2d5e11aee286))


## v0.12.0 (2021-02-13)

### Build

* build(deps): change pipfile.lock to python 3.7 ([`b5b38b1`](https://github.com/zabuldon/teslajsonpy/commit/b5b38b1da40d69c7d64ebecddb6eefa2527bf9cd))

* build(deps): update pipfile.lock ([`e6d38cc`](https://github.com/zabuldon/teslajsonpy/commit/e6d38cc3c9764b341b620c452dac08e4a5844c30))

* build(deps): bump bleach from 3.1.4 to 3.3.0 (#137) ([`623863f`](https://github.com/zabuldon/teslajsonpy/commit/623863f3758fb6c1c814d6f09b7d5d068f6b2c96))

* build(deps): don&#39;t use dummy bs4 module (#138) ([`69aab5f`](https://github.com/zabuldon/teslajsonpy/commit/69aab5ff902bca7e0bfa365d0d3b9e8de7ae2439))

### Ci

* ci: change tests to py3.7 and remove py3.9

py 3.9 has issues within Typing. ([`8a6b5a7`](https://github.com/zabuldon/teslajsonpy/commit/8a6b5a7dadff8bffd2aee734838f3e34a9067371))

### Documentation

* docs: add badges ([`02b583b`](https://github.com/zabuldon/teslajsonpy/commit/02b583b3ab4a53579bf8c68c03f03ee4405f6559))

### Feature

* feat: add teslaproxy to capture oauth credentials
BREAKING CHANGE: Change return of connect and get_tokens to return
expiration time. ([`dd209d9`](https://github.com/zabuldon/teslajsonpy/commit/dd209d9c9f7d78b6cc2e2ca0da083054a58f0bc1))

### Style

* style: fix lint error ([`9bcdf6e`](https://github.com/zabuldon/teslajsonpy/commit/9bcdf6eee86cd2a2ae09beeccd4d43df5502cfd7))

### Unknown

* Merge pull request #141 from zabuldon/dev

2021-02-13 ([`9cd6009`](https://github.com/zabuldon/teslajsonpy/commit/9cd6009a484bc4393470c6240a22c1b7f1793025))

* Merge pull request #140 from alandtse/ci_fix

Signed-off-by: Alan Tse &lt;alandtse@gmail.com&gt; ([`b33b750`](https://github.com/zabuldon/teslajsonpy/commit/b33b750eaa836ca562e1dd227224296bc64383bc))

* Merge pull request #139 from alandtse/ci_fix

docs: add badges ([`a026a94`](https://github.com/zabuldon/teslajsonpy/commit/a026a94813d0ca530a7ae1889bc65a88b2603139))

* Merge pull request #136 from zabuldon/master

Signed-off-by: Alan Tse &lt;alandtse@gmail.com&gt; ([`631636f`](https://github.com/zabuldon/teslajsonpy/commit/631636f7fd2007493c86caede8e6436f154d317d))


## v0.11.5 (2021-02-02)

### Fix

* fix: address attribute error properly for form ([`11f59ea`](https://github.com/zabuldon/teslajsonpy/commit/11f59eaa398d70e1444151414cc5235ce68584d9))

### Unknown

* Merge pull request #135 from alandtse/ci_fix

fix: address attribute error properly for form ([`442fbaf`](https://github.com/zabuldon/teslajsonpy/commit/442fbaff55c904c2d4bee617156d9a4347b42f5c))


## v0.11.4 (2021-02-02)

### Fix

* fix: check for existence of input field in form ([`613406e`](https://github.com/zabuldon/teslajsonpy/commit/613406e4f6bc95f7306b18e54ba47ea718b63fd8))

### Unknown

* Merge pull request #134 from alandtse/ci_fix

Signed-off-by: Alan Tse &lt;alandtse@gmail.com&gt; ([`3b3a5c2`](https://github.com/zabuldon/teslajsonpy/commit/3b3a5c207aa37a3350bdd81a3a99ec6ad5652847))

* Merge pull request #133 from zabuldon/master

Master ([`b326d37`](https://github.com/zabuldon/teslajsonpy/commit/b326d374c6e2a2ad30ff3e537de8e479bb3b8ebd))


## v0.11.3 (2021-01-31)

### Fix

* fix: detect missing name/password ([`c4f8c54`](https://github.com/zabuldon/teslajsonpy/commit/c4f8c54d0149fa0b22dfcb299cb4ae6b4cbffaa3))

### Test

* test: remove generate_oauth test ([`fba3f92`](https://github.com/zabuldon/teslajsonpy/commit/fba3f924e1c000315314e404206452fe5b392a19))

### Unknown

* Merge pull request #132 from alandtse/ci_fix

Signed-off-by: Alan Tse &lt;alandtse@gmail.com&gt; ([`ff99a2f`](https://github.com/zabuldon/teslajsonpy/commit/ff99a2fda4ffa4410a2b2da591ff55d1c867edee))


## v0.11.2 (2021-01-31)

### Ci

* ci: run tests on pull to dev ([`6707f14`](https://github.com/zabuldon/teslajsonpy/commit/6707f14277cb63106bad7b2a0fee934a70ff6308))

### Fix

* fix: add bs4 as dependency for install ([`2a3c154`](https://github.com/zabuldon/teslajsonpy/commit/2a3c15488b26f116a40156bdd8e3ae0b6d24ec01))

### Style

* style: fix lint error ([`ed20a43`](https://github.com/zabuldon/teslajsonpy/commit/ed20a4398595355a8880e9502f6f995aa63876e9))

* style: fix lint error ([`0c2a0c2`](https://github.com/zabuldon/teslajsonpy/commit/0c2a0c27a2d5bb72ddcfb745ddaf15179c87bfad))

* style: fix lint error ([`ec1b1e6`](https://github.com/zabuldon/teslajsonpy/commit/ec1b1e6a8ea20f6933830e6b0fe97af0bb9e198b))

### Unknown

* Merge pull request #131 from zabuldon/dev

2021-01-30 - 2 ([`13fee5c`](https://github.com/zabuldon/teslajsonpy/commit/13fee5c6290088734568282e54483603e9b25f01))

* Merge pull request #130 from alandtse/ci_fix

Ci fix ([`e980381`](https://github.com/zabuldon/teslajsonpy/commit/e98038109247f51748d133895d5094ac22e8af15))

* Revert &#34;style: fix lint error&#34;

This reverts commit ec1b1e6a8ea20f6933830e6b0fe97af0bb9e198b. ([`9fd7298`](https://github.com/zabuldon/teslajsonpy/commit/9fd729823162681dcd34942713d3616732a8e726))

* Merge pull request #129 from alandtse/ci_fix

Ci fix ([`ec1f18e`](https://github.com/zabuldon/teslajsonpy/commit/ec1f18e6f7688078dc4941703855b7a286e1b057))

* Merge branch &#39;ci_fix&#39; of github.com:alandtse/teslajsonpy into ci_fix ([`ed7a355`](https://github.com/zabuldon/teslajsonpy/commit/ed7a355046ce0d27e2d09e2daf19a574ba332e26))

* Merge pull request #128 from zabuldon/master

Signed-off-by: Alan Tse &lt;alandtse@gmail.com&gt; ([`bb4283a`](https://github.com/zabuldon/teslajsonpy/commit/bb4283afb64e834f8383b922dc012af073bb469f))


## v0.11.1 (2021-01-31)

### Ci

* ci: fix tests ([`c5ffd96`](https://github.com/zabuldon/teslajsonpy/commit/c5ffd969d3fd9440d72e3928d02337bc923abb32))

* ci: add make tests

* Update test_charging_sensor.py

* make sure attr name and cls att is the same

* Run tests with github action

* Use make ([`7348af1`](https://github.com/zabuldon/teslajsonpy/commit/7348af1883c8ccbf70ec09f24988071dacd3925b))

### Fix

* fix: use oauth3 login ([`487c7b4`](https://github.com/zabuldon/teslajsonpy/commit/487c7b4d3ff2cddf3bf3fdd099dc8a51ae2d4e5d))

* fix: fix header passing in __open ([`f193c64`](https://github.com/zabuldon/teslajsonpy/commit/f193c6439b3b6bc682e8884ec6950b44e0f0303c))

### Unknown

* Merge pull request #127 from zabuldon/dev

2021-01-30 ([`320ad6c`](https://github.com/zabuldon/teslajsonpy/commit/320ad6cabbcc5e325155fa3b6e0758df0bc560cf))

* Merge pull request #126 from alandtse/ci_fix

ci: fix tests ([`d763414`](https://github.com/zabuldon/teslajsonpy/commit/d763414c42dc23f77dd95534f8bf34d4b16e19c5))

* Merge pull request #125 from alandtse/oauthv3

Signed-off-by: Alan Tse &lt;alandtse@gmail.com&gt; ([`c6fe2b3`](https://github.com/zabuldon/teslajsonpy/commit/c6fe2b3d94d5d4c492659272d353ba45760dc542))

* Merge pull request #123 from zabuldon/master

Master ([`f4b8988`](https://github.com/zabuldon/teslajsonpy/commit/f4b8988ba3e7bd5a9683a84c02f56fe777175b71))


## v0.11.0 (2021-01-12)

### Feature

* feat: add charge limit soc (#120)

closes #114 ([`441a72a`](https://github.com/zabuldon/teslajsonpy/commit/441a72a9f25b71cd9aecba10dab358a7f37f513f))

### Fix

* fix: tests.* (subpackage) exclusion from installs (#116) ([`2d3ae90`](https://github.com/zabuldon/teslajsonpy/commit/2d3ae907506c8f59e32ef38fdd5b4902c2a7ab29))

### Unknown

* Merge pull request #122 from zabuldon/dev

2020-01-12 ([`5dd9716`](https://github.com/zabuldon/teslajsonpy/commit/5dd971668ca9ed0c4fba4915728c933d843a75f7))

* Merge pull request #113 from zabuldon/master

Master ([`a6dae2d`](https://github.com/zabuldon/teslajsonpy/commit/a6dae2d54f2a2702faf8bf40327f050a6d67b6b4))


## v0.10.4 (2020-08-08)

### Fix

* fix: return None for _sensor_type
This is needed to fix a change in HA where device_class will overwrite
ICON settings if it exists ([`d5901c7`](https://github.com/zabuldon/teslajsonpy/commit/d5901c74f51ec582ebb5a767bb82073f92b8b7b4))

### Style

* style: add typing to binary_sensor ([`3272bd6`](https://github.com/zabuldon/teslajsonpy/commit/3272bd667be4898a07ef435bc104e68e76adce4f))

### Unknown

* Merge pull request #112 from zabuldon/dev

2020-08-07 ([`e05e49d`](https://github.com/zabuldon/teslajsonpy/commit/e05e49dced77f336bb333708368a67e2dad665bf))

* Merge pull request #111 from alandtse/device_class

fix: fix sensor_type for binary_sensor ([`e070c05`](https://github.com/zabuldon/teslajsonpy/commit/e070c05c6905b05f26baac2329c1d08bde77e45e))

* Merge pull request #109 from zabuldon/master

Master ([`4c48045`](https://github.com/zabuldon/teslajsonpy/commit/4c4804547f73561f72ec8e70ee87d6efe8fb589c))


## v0.10.3 (2020-07-31)

### Fix

* fix: allow sentry mode to return None ([`8250fca`](https://github.com/zabuldon/teslajsonpy/commit/8250fca9df95315f9f1d4ca8c09e883a81d7aebb))

* fix: set default lock state to None
If no information is available, the component can return None ([`7c44581`](https://github.com/zabuldon/teslajsonpy/commit/7c44581be9bd4778be81b3819008cf70fd68f016))

### Style

* style: add typing hints to sentry mode ([`1942205`](https://github.com/zabuldon/teslajsonpy/commit/1942205a667496eb4f276badcb73819d5432b654))

### Unknown

* Merge pull request #108 from zabuldon/dev

2020-07-30 ([`77cc9b7`](https://github.com/zabuldon/teslajsonpy/commit/77cc9b7611a72cdfc1a47375fa582c69a3cc7426))

* Merge pull request #107 from alandtse/tesla_update_sensor

2020-07-30 ([`b3ebc39`](https://github.com/zabuldon/teslajsonpy/commit/b3ebc3923181daac7674bdf0fca3fc0fc99ef467))

* Merge pull request #106 from zabuldon/master

Master ([`4f1afd6`](https://github.com/zabuldon/teslajsonpy/commit/4f1afd6c0fa6d69e6017ae6f4bd2c9cb85d9aee2))


## v0.10.2 (2020-07-29)

### Fix

* fix: expose UpdateSensor ([`1a1b0fe`](https://github.com/zabuldon/teslajsonpy/commit/1a1b0fe4c033ed72ebc099d0aa7e9f431a3acf6e))

### Refactor

* refactor: reorganize homeassistant specific files ([`f1f5994`](https://github.com/zabuldon/teslajsonpy/commit/f1f5994da0c57c9eaa49a9216f2b1f164bbd43a8))

* refactor: break out non IO operations to refresh
This is to support callback functions for the HA coordinator ([`9793ee0`](https://github.com/zabuldon/teslajsonpy/commit/9793ee09c297cdc6dc05e6b67bc826ac11d3394f))

### Unknown

* Merge pull request #105 from zabuldon/dev

2020-07-28 ([`ff7bdd3`](https://github.com/zabuldon/teslajsonpy/commit/ff7bdd3ea1886518e1edf21c456f3aace3fbb9af))

* Merge pull request #104 from alandtse/tesla_update_sensor

Refactor for HA data coordinator ([`a397af1`](https://github.com/zabuldon/teslajsonpy/commit/a397af1d18808c994dba9a96a8c682b822a8093b))

* Merge pull request #103 from zabuldon/master

Master ([`3cbc17a`](https://github.com/zabuldon/teslajsonpy/commit/3cbc17a06469e549b460a181f32c002d1ddce7e5))


## v0.10.1 (2020-07-23)

### Fix

* fix: change sensor_type of update sensor to None
Required for HA inclusion. ([`e8bfca7`](https://github.com/zabuldon/teslajsonpy/commit/e8bfca743186acb2396ce0a4979bae1b9289b5cb))

### Unknown

* Merge pull request #102 from zabuldon/dev

2020-07-22 ([`42f211f`](https://github.com/zabuldon/teslajsonpy/commit/42f211ff07f1849d9cdcdb98151e6ca2c69a7a40))

* Merge pull request #101 from alandtse/tesla_update_sensor

fix: change sensor_type of update sensor to None ([`ad7fc7c`](https://github.com/zabuldon/teslajsonpy/commit/ad7fc7ce3d2137f7c4184137279dbba0438bb37b))

* Merge pull request #100 from zabuldon/master

Master ([`72fb306`](https://github.com/zabuldon/teslajsonpy/commit/72fb30697b9b70a6123e8f5a081e54ddd34ce65f))


## v0.10.0 (2020-07-19)

### Feature

* feat: add update availability sensor
closes #75 ([`44eeda4`](https://github.com/zabuldon/teslajsonpy/commit/44eeda4b6558ca7c79d20cc1efa3d7a5c741d46c))

### Style

* style: fix linting errors ([`7ac9c0b`](https://github.com/zabuldon/teslajsonpy/commit/7ac9c0b04463cbc574ca41e5e620bb5beb1b8479))

### Unknown

* Merge pull request #99 from zabuldon/dev

2020-07-18 ([`bd8d1f5`](https://github.com/zabuldon/teslajsonpy/commit/bd8d1f5280cc79e74d45c79bd0072ac9ad6307d3))

* Merge pull request #98 from alandtse/tesla_update_sensor

Tesla update sensor ([`d2df26d`](https://github.com/zabuldon/teslajsonpy/commit/d2df26d9a683a0efe979d3d5404acfedf3ef4e83))

* Merge pull request #97 from zabuldon/master

Master ([`1c9a41c`](https://github.com/zabuldon/teslajsonpy/commit/1c9a41c37095f0f30f0600dd518c66ec795b67c4))


## v0.9.3 (2020-07-12)

### Fix

* fix: change controller_lock to be a function lock
The wake_up command was stuck in a deadlock waiting for the update lock
to release. Renamed controller_lock to make it clear it&#39;s for access to
the update function instead. Will evaluate whether a lock needs to be
placed on the self.car_online array. ([`23e7de5`](https://github.com/zabuldon/teslajsonpy/commit/23e7de52c2c4f384a05379ad8404fb7f9e2e4a52))

### Unknown

* Merge pull request #96 from zabuldon/dev

2020-07-11 ([`1ed6060`](https://github.com/zabuldon/teslajsonpy/commit/1ed6060a069ca783a0293873dc0884659df26c19))

* Merge pull request #95 from alandtse/#ha37684

fix: change controller_lock to be a function lock ([`1059202`](https://github.com/zabuldon/teslajsonpy/commit/1059202e7e99228b78b166d78de06a7b859ff303))

* Merge pull request #94 from zabuldon/master

Master ([`dc993dc`](https://github.com/zabuldon/teslajsonpy/commit/dc993dcc674d28886e2fecbca0ca015ecc678281))


## v0.9.2 (2020-07-03)

### Fix

* fix: fix indentation of sleep_interval ([`4bc743f`](https://github.com/zabuldon/teslajsonpy/commit/4bc743f2e214a26806d3e43424786b50a1d57da5))

### Unknown

* Merge pull request #93 from zabuldon/dev

fix: fix indentation of sleep_interval ([`f10a493`](https://github.com/zabuldon/teslajsonpy/commit/f10a493cd5e7879e5c13613d3dd56ec254779180))

* Merge pull request #92 from alandtse/#ha37340

fix: fix indentation of sleep_interval ([`96ab248`](https://github.com/zabuldon/teslajsonpy/commit/96ab24838b4c3504912e2b930c0384aabd9e58d7))

* Merge pull request #91 from zabuldon/master

Sync dev with Master ([`74c49ab`](https://github.com/zabuldon/teslajsonpy/commit/74c49aba9d063c807f33e025586f7ae5f6bb93fd))


## v0.9.1 (2020-07-03)

### Fix

* fix: use max of update_interval and SLEEP_INTERVAL
This should resolve a situation where a user chooses a bigger
update_interval.
Addresses #HA37340 ([`f34df60`](https://github.com/zabuldon/teslajsonpy/commit/f34df60b3089efa548f385aeff229a9784ea488e))

### Unknown

* Merge pull request #90 from zabuldon/dev

2020-07-03 ([`f0c2310`](https://github.com/zabuldon/teslajsonpy/commit/f0c23105af426012188cb27bccd722761fbb5f80))

* Merge pull request #89 from alandtse/#ha37340

fix: use max of update_interval and SLEEP_INTERVAL ([`0033c27`](https://github.com/zabuldon/teslajsonpy/commit/0033c27b97c992956a4e374c7058ff95e1739779))

* Merge pull request #88 from zabuldon/master

Sync dev with Master ([`228dd89`](https://github.com/zabuldon/teslajsonpy/commit/228dd89ac3ebda6a1995d47c9aacd54127851fa9))


## v0.9.0 (2020-06-26)

### Feature

* feat: add option for filtering cars by VIN to connect (#85) ([`dafffb0`](https://github.com/zabuldon/teslajsonpy/commit/dafffb023eaa9376e9f3d29cc6e4e8662a93c1da))

### Fix

* fix: add check that data exists when http 401 ([`1d4c107`](https://github.com/zabuldon/teslajsonpy/commit/1d4c1070a3ba46e8a2ec6c8cdab86864dde80c51))

* fix: place car updates behind main lock
Fixes a race condition where different entities could modify the
online state. ([`a8bf497`](https://github.com/zabuldon/teslajsonpy/commit/a8bf497082d258fd4d3f4ab3e8f24df67f40699f))

### Unknown

* Merge pull request #87 from zabuldon/dev

2020-06-26 ([`c714dbd`](https://github.com/zabuldon/teslajsonpy/commit/c714dbddaa6a1b7b73b75b0819edf0bf416468c9))

* Merge pull request #86 from alandtse/#HA37106

Address HA report #37106 ([`d40c8f3`](https://github.com/zabuldon/teslajsonpy/commit/d40c8f3977d6490e8d9c30bb6a1b620382bf326b))

* Merge pull request #83 from alandtse/408_errors

fix: place car updates behind main lock ([`e1534b9`](https://github.com/zabuldon/teslajsonpy/commit/e1534b9cbdaf702923d3cd9b5843dc2edc2e87d5))


## v0.8.1 (2020-05-31)

### Fix

* fix: add retry to get_vehicles
get_vehicles is the first command used by the controller. In case of a
transient connection error, it will retry for up to 10 seconds. ([`1b6660d`](https://github.com/zabuldon/teslajsonpy/commit/1b6660d8097d97e048a36b94a5fe469659b8db9f))

### Unknown

* Merge pull request #81 from zabuldon/dev

fix: add retry to get_vehicles ([`aeaeb04`](https://github.com/zabuldon/teslajsonpy/commit/aeaeb04d4cbb87d74a221a7640cde540607f7a15))

* Merge pull request #80 from alandtse/retry_init

fix: add retry to get_vehicles ([`9c440c8`](https://github.com/zabuldon/teslajsonpy/commit/9c440c8329638eae82a14bafaa05102c0c3b947f))


## v0.8.0 (2020-04-16)

### Feature

* feat: add trunk and frunk management (#71)

* add trunk sensor

* add frunk sensor

* add frunk sensor

* add frunk sensor

* add trunk switch

* add frunk switch

* add trunk lock

* add frunk lock

* fix lint R0915 too-many-statements

* rename open_trunk to open, same for close

* fix some attributes to work with HA integration

* 0.7.0

Automatically generated by python-semantic-release

* remove unecessary sensors and switches

* add last update handling

Co-authored-by: Alan Tse &lt;alandtse@users.noreply.github.com&gt;
Co-authored-by: semantic-release &lt;semantic-release&gt; ([`142e44b`](https://github.com/zabuldon/teslajsonpy/commit/142e44b18cebe3fda04d5d64a6aa48cfb3bacb37))

### Unknown

* Merge pull request #79 from zabuldon/dev

0.8.0 ([`153af49`](https://github.com/zabuldon/teslajsonpy/commit/153af49754208cf50414be98af02a45171a1b27f))

* Merge pull request #78 from zabuldon/master

Sync dev with master ([`ca180de`](https://github.com/zabuldon/teslajsonpy/commit/ca180de08689986cecbbe73bca13a01224043ffe))


## v0.7.0 (2020-04-14)

### Build

* build(deps): bump bleach from 3.1.3 to 3.1.4

Bumps [bleach](https://github.com/mozilla/bleach) from 3.1.3 to 3.1.4.
- [Release notes](https://github.com/mozilla/bleach/releases)
- [Changelog](https://github.com/mozilla/bleach/blob/master/CHANGES)
- [Commits](https://github.com/mozilla/bleach/compare/v3.1.3...v3.1.4)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`684f9fe`](https://github.com/zabuldon/teslajsonpy/commit/684f9fe451cb09941d5aa6d696be7fe32cf9f1ca))

* build: streamline tox ([`2966a47`](https://github.com/zabuldon/teslajsonpy/commit/2966a4748f3e79f7c6d045b0ef9de485fd64d3bc))

* build(deps): bump bleach from 3.1.1 to 3.1.2 (#69)

Bumps [bleach](https://github.com/mozilla/bleach) from 3.1.1 to 3.1.2.
- [Release notes](https://github.com/mozilla/bleach/releases)
- [Changelog](https://github.com/mozilla/bleach/blob/master/CHANGES)
- [Commits](https://github.com/mozilla/bleach/compare/v3.1.1...v3.1.2)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`2be197d`](https://github.com/zabuldon/teslajsonpy/commit/2be197d383c41914904d4adfabd2a0ae8eec2b69))

### Documentation

* docs: expose data for post to logs ([`3e3dd07`](https://github.com/zabuldon/teslajsonpy/commit/3e3dd077aa9fd0e5477b92a6ed111f5a6baefc5a))

### Feature

* feat: add defrost mode
closes #62 ([`9657222`](https://github.com/zabuldon/teslajsonpy/commit/96572224d6b1642a7c031b47a86a2bc21dd91d0e))

### Fix

* fix: fix failing climate tests ([`8144a3a`](https://github.com/zabuldon/teslajsonpy/commit/8144a3a307ae2ab96959292074ab569e3cd6f25e))

* fix: fix type for vin ([`88d288c`](https://github.com/zabuldon/teslajsonpy/commit/88d288c571126e1d0aba98b5ea88dc1c41115c7e))

* fix: fix failure to update all cars with update ([`76df2f1`](https://github.com/zabuldon/teslajsonpy/commit/76df2f11d296fc4d35279ae254d55ac482cb2a9a))

* fix: fix update when car_id is None
The for loop on online cars was improperly using car_id instead of the
vin from within the loop. ([`92907ae`](https://github.com/zabuldon/teslajsonpy/commit/92907ae597bed2b997775a51b5b4a0056287898b))

* fix: force update of climate on preset_mode set ([`a4f61d0`](https://github.com/zabuldon/teslajsonpy/commit/a4f61d0777cafb6348e4eb3d103108b0f2438e51))

* fix: addres flake errors ([`579155d`](https://github.com/zabuldon/teslajsonpy/commit/579155dbcc9b659eb74638129674a2acb8039967))

### Performance

* perf: allow parallel car updates ([`4ce4269`](https://github.com/zabuldon/teslajsonpy/commit/4ce426955183927b235930ef815f0ff2c35d4e7e))

### Test

* test: fix bad mode preset_test ([`e33d2df`](https://github.com/zabuldon/teslajsonpy/commit/e33d2df08b5bd7d7047ee229ed1967d5a421d7f9))

* test: add pytest and coverage (#68)

* initialize pytest framework

* Fix initialization of _sentry_mode_available flag

* fix initialization of sentry_mode flag

remove sentry_mode_available flag to use the property from vehicle

* add tests for sentry mode

add a mock for Tesla server communications

* add .vscode to .gitignore

* add async tests for sentry mode switch

* add unit tests for gps and odometer

* increase gps test coverage

* add unit tests for battery and range sensors

* fix test name in documentation

* add unit tests for binary sensors

* add unit tests for charger switches and sensors

* rename test files

* refactor variable names

* add unit tests for climate and temp sensor

* add unit tests for door lock and charge lock

* add unit tests for vehicle device

* increase test coverage for sensors

* add unit tests for tesla exception

closes #26 ([`a0cf7e1`](https://github.com/zabuldon/teslajsonpy/commit/a0cf7e1cac42a7e245a9167648735411d11c1a4f))

### Unknown

* Merge pull request #77 from zabuldon/dev

0.7.0 ([`c279388`](https://github.com/zabuldon/teslajsonpy/commit/c27938883d47c7ee0ceac8e868a6c317de257f8e))

* Merge pull request #76 from alandtse/#62

feat: add defrost mode ([`0b29e2f`](https://github.com/zabuldon/teslajsonpy/commit/0b29e2f9711eb69729be6ebfd660ac1893367a0d))

* Merge pull request #73 from zabuldon/dependabot/pip/bleach-3.1.4

build(deps): bump bleach from 3.1.3 to 3.1.4 ([`dafafc7`](https://github.com/zabuldon/teslajsonpy/commit/dafafc72692dc5816094084aa9a43c98cb71cc82))

* Merge pull request #70 from alandtse/tox

build: streamline tox ([`8ce336c`](https://github.com/zabuldon/teslajsonpy/commit/8ce336c09ec7bdbc19ebebb79237dddf2f13aa65))


## v0.6.0 (2020-03-22)

### Documentation

* docs: add initial developer info ([`1d0a5cb`](https://github.com/zabuldon/teslajsonpy/commit/1d0a5cbbc05805a479774510000998c54e5ee9e4))

### Feature

* feat: add sentry mode availability flag (#66) ([`d1f9199`](https://github.com/zabuldon/teslajsonpy/commit/d1f9199c0c30a61521004db859a782d45d8126c3))

### Unknown

* Merge pull request #65 from alandtse/developers

docs: add initial developer info ([`ab89698`](https://github.com/zabuldon/teslajsonpy/commit/ab89698819ed69aaff88c998a1bfbcdaecbacd41))


## v0.5.1 (2020-03-15)

### Unknown

* Merge pull request #60 from zabuldon/dependabot/pip/bleach-3.1.1

build(deps): bump bleach from 3.1.0 to 3.1.1 ([`a7bcc07`](https://github.com/zabuldon/teslajsonpy/commit/a7bcc07106e3f4f39910fdac307af93404a87d44))

* Merge pull request #64 from alandtse/relocking

fix: remove checks for state for lock/unlock ([`9c826ad`](https://github.com/zabuldon/teslajsonpy/commit/9c826ad98be306cf4084c5b2a7eeb71753b899e7))


## v0.5.0 (2020-03-15)

### Build

* build(deps): bump bleach from 3.1.0 to 3.1.1

Bumps [bleach](https://github.com/mozilla/bleach) from 3.1.0 to 3.1.1.
- [Release notes](https://github.com/mozilla/bleach/releases)
- [Changelog](https://github.com/mozilla/bleach/blob/master/CHANGES)
- [Commits](https://github.com/mozilla/bleach/compare/v3.1.0...v3.1.1)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`715b915`](https://github.com/zabuldon/teslajsonpy/commit/715b91559ad09de5dae55eb142422c1b4202cec7))

### Feature

* feat: add sentry mode switch to fix issue #43 ([`1aadef3`](https://github.com/zabuldon/teslajsonpy/commit/1aadef3896a66bb308c5d479b78bbd0a420a6a37))

### Fix

* fix: remove checks for state for lock/unlock
Tesla will automatically relock so the lock state may not match the internal known
state and prevent a lock/unlock. ([`bc0dca9`](https://github.com/zabuldon/teslajsonpy/commit/bc0dca92694d3d1e7876c3dc4a127b7098f1afa4))

### Unknown

* Merge pull request #61 from hobbe/feat/sentry-mode

feat: add sentry mode switch
closes #43 ([`c574ab0`](https://github.com/zabuldon/teslajsonpy/commit/c574ab0ff725fbc6855949ddc34e6c14c445356e))


## v0.4.0 (2020-02-28)

### Documentation

* docs: fix property documentation ([`c414ae7`](https://github.com/zabuldon/teslajsonpy/commit/c414ae7712053e8a2114b8efe3d7c994bd42a16f))

* docs: streamline debug messages ([`3342d67`](https://github.com/zabuldon/teslajsonpy/commit/3342d67a52a4c0ef88ef22858f58a5e47ee07384))

* docs: add additional websocket logging ([`690af0e`](https://github.com/zabuldon/teslajsonpy/commit/690af0e9fae925d388d2d8fb508a2c784e4c7b68))

* docs: fix typos ([`f38d2e6`](https://github.com/zabuldon/teslajsonpy/commit/f38d2e69b9145b1dcc945fa19215814205a4e0ff))

* docs: update websocket_connect documentation ([`91546aa`](https://github.com/zabuldon/teslajsonpy/commit/91546aab04091cbfcf2f16bc35d938ec79e59178))

### Feature

* feat: expose expiration for oauth ([`0e116c3`](https://github.com/zabuldon/teslajsonpy/commit/0e116c366bc3ac4fdd8300f6781e2da8c551cf00))

* feat: expose charge_energy_added ([`249a25c`](https://github.com/zabuldon/teslajsonpy/commit/249a25c1aeb1c4650de0d25a096c9b8292ae946d))

* feat: add wake_if_asleep param to update ([`500968a`](https://github.com/zabuldon/teslajsonpy/commit/500968a04b5773e4c2e63a49192dd4fc5c935a7a))

* feat: add option to enable websockets ([`b2717e8`](https://github.com/zabuldon/teslajsonpy/commit/b2717e8906ec118baa62450ff2c7317b2d9d0028))

* feat: expose charger_phases ([`07c69e3`](https://github.com/zabuldon/teslajsonpy/commit/07c69e3d2ed002ecdd90b794adb0b87277661100))

* feat: change to adaptive algorithm based updates
Instead of polling for a set SCAN_INTERVAL, the new algorithm will
determine if the car has recently parked and update normally for the
IDLE_INTERVAL (600). After the idle period is complete, updates are
throttled to the SLEEP_INTERVAL until the car is asleep. There is now a
regular ONLINE_INTERVAL (60) check which does not query the car and
will immediately detect if a car has become awake to resume updates. ([`d7b1f5c`](https://github.com/zabuldon/teslajsonpy/commit/d7b1f5c9bf83935940cf0d7ef4d2cf0f04d6feda))

* feat: add callback register for websocket ([`a9e33c1`](https://github.com/zabuldon/teslajsonpy/commit/a9e33c1af7109081097a726738c6fdb186f6cc7e))

* feat: add websocket connection
Closes #25 ([`7719abb`](https://github.com/zabuldon/teslajsonpy/commit/7719abb5103fd862707eeab7fada783f8993f07c))

### Fix

* fix: enable native_type gps ([`21c919e`](https://github.com/zabuldon/teslajsonpy/commit/21c919eff33cedc5ca8148e51300c5c5f69055cc))

* fix: update websocket subscribe and retry
This is the subscribe command from the latest app ([`d3afe61`](https://github.com/zabuldon/teslajsonpy/commit/d3afe61fea7c216a509fd630dea85dff0728a081))

* fix: force further delay in backoff ([`4d07e07`](https://github.com/zabuldon/teslajsonpy/commit/4d07e07723deb35e1ce9ca4ba4c8ab4052cdae79))

* fix: handle malformed websocket data ([`95badc2`](https://github.com/zabuldon/teslajsonpy/commit/95badc278846bbfede21a63846b77dd16a2fd05f))

* fix: add vehicle_unavailable exception ([`166013c`](https://github.com/zabuldon/teslajsonpy/commit/166013ca75bcb45962113f2a58982af54bacf4dd))

* fix: prevent update for in_service cars ([`606c11e`](https://github.com/zabuldon/teslajsonpy/commit/606c11ee0571e7cdc57b199e6409106a531340d1))

* fix: fix handling of could_not_wake_buses ([`990ee3d`](https://github.com/zabuldon/teslajsonpy/commit/990ee3d497d49110421592e52a3b3551a815eb1e))

* fix: further fine tune adaptive checking ([`5f1e34d`](https://github.com/zabuldon/teslajsonpy/commit/5f1e34d351a5e9268924bfb591730752b7b01b25))

* fix: fix saving of websocket battery level ([`8907238`](https://github.com/zabuldon/teslajsonpy/commit/890723838316c352573c9f7c1ced3dba667696c0))

* fix: export OnlineSensor ([`8483a20`](https://github.com/zabuldon/teslajsonpy/commit/8483a2078b4cb3c8263447eba3c7b06a20793823))

* fix: increase minimum retry delay to 15 seconds ([`fad88bc`](https://github.com/zabuldon/teslajsonpy/commit/fad88bc11337c6517a99db28154a668b2e506caa))

* fix: save raw_online_state on updates ([`5cf5c17`](https://github.com/zabuldon/teslajsonpy/commit/5cf5c178704527c5fd4fcc65f77b3de8c60bbc53))

### Refactor

* refactor: change default value to None ([`4ec8d9b`](https://github.com/zabuldon/teslajsonpy/commit/4ec8d9b24a7d1d020372ae20ea5bf86d748a3f01))

* refactor: change wake_if_asleep option for connect ([`d381d53`](https://github.com/zabuldon/teslajsonpy/commit/d381d53e446c481aabfc0384260d3e66e769b04c))

* refactor: change backoff behavior to commands only ([`383ce46`](https://github.com/zabuldon/teslajsonpy/commit/383ce46cc89608054e83cbdf0d840d7e95b88727))

* refactor: convert to wrapt ([`c0907b2`](https://github.com/zabuldon/teslajsonpy/commit/c0907b24640d89930099eab909481aea2ecb6c4d))

* refactor: add handling of upstream_timeout ([`eddfa32`](https://github.com/zabuldon/teslajsonpy/commit/eddfa32440cec00e8097d010d720f2bd99be540e))

* refactor: black ([`a3728e5`](https://github.com/zabuldon/teslajsonpy/commit/a3728e59738778e1edf3b529c42467a7e7d4932c))

* refactor: switch to backoff for retries ([`cbe539e`](https://github.com/zabuldon/teslajsonpy/commit/cbe539e929c330bb6ded74d9392f55d09481dfbf))

* refactor: save car_state from get_vehicles ([`2445d5b`](https://github.com/zabuldon/teslajsonpy/commit/2445d5b6a44a7b93fd11c8b52786c1cabd2af6a2))

* refactor: add attributes to charger connection ([`e0631e1`](https://github.com/zabuldon/teslajsonpy/commit/e0631e10fffba6f3d7180fa9e97fcad305eaa843))

* refactor: move attributes to vehicle class ([`9739117`](https://github.com/zabuldon/teslajsonpy/commit/9739117f9bc1cb0dabd63b7ef8da9609206d9792))

* refactor: sleep only when sentry mode off ([`9d0d6fd`](https://github.com/zabuldon/teslajsonpy/commit/9d0d6fd09032c00160996705dfecb1f471ea1738))

* refactor: migrate to non-legacy update url ([`ac08435`](https://github.com/zabuldon/teslajsonpy/commit/ac084353989330d3e3cdfab775aa04fe4363ce05))

* refactor: only allow updates if car isn&#39;t offline ([`2c85b80`](https://github.com/zabuldon/teslajsonpy/commit/2c85b804b7a7f8d73dffc603cadaa00dc8315089))

* refactor: simplify kwargs logic ([`d463420`](https://github.com/zabuldon/teslajsonpy/commit/d463420f9c2ff4c305841f4bcfb5d9b570607858))

### Style

* style: black ([`468df5a`](https://github.com/zabuldon/teslajsonpy/commit/468df5a24e97ab0c1901b334b6a9772fabf86f42))

### Unknown

* Merge pull request #57 from alandtse/websocket

feat: add websocket support ([`9a13d89`](https://github.com/zabuldon/teslajsonpy/commit/9a13d890cf9c9e17e95929a4471530ea93c48db7))


## v0.3.0 (2020-01-27)

### Feature

* feat: add state attributes for binary sensors ([`46e89be`](https://github.com/zabuldon/teslajsonpy/commit/46e89beab8410b48a0970d1ddefb18e550e804d3))

* feat: add attrs to online sensor ([`02cec5b`](https://github.com/zabuldon/teslajsonpy/commit/02cec5b245d5f93097587e153097452441b42cd7))

* feat: add online binary sensor ([`08d6961`](https://github.com/zabuldon/teslajsonpy/commit/08d6961328f2184c7136f77a15a9486f00518ab2))

### Fix

* fix: avoid recursion in wake_up wrapper ([`b2e74d1`](https://github.com/zabuldon/teslajsonpy/commit/b2e74d1b31db2d3996db4aa92738bd0ef075e6eb))

* fix: properly save refresh_token for login ([`2926b34`](https://github.com/zabuldon/teslajsonpy/commit/2926b34045890dfa5366b9caeddd13ba53180461))

* fix: add HA battery properties to battery sensor ([`2355139`](https://github.com/zabuldon/teslajsonpy/commit/235513920841d7bf8b16a0c641369001032c86f6))

* fix: fix wake up decorator to avoid recursion ([`e3c7c17`](https://github.com/zabuldon/teslajsonpy/commit/e3c7c17ffd783f364bba2c4b3f0b5b8a7dc07759))

* fix: fix forced wake up in initial update ([`0892b91`](https://github.com/zabuldon/teslajsonpy/commit/0892b914085b3900653a7a8d4b45c13331a73e8e))

### Refactor

* refactor(exceptions): add logging and cleanup ([`267f8c0`](https://github.com/zabuldon/teslajsonpy/commit/267f8c02b237998d560f69bcaed5fc8e32ef0892))

* refactor: improve incomplete credentials message ([`047e529`](https://github.com/zabuldon/teslajsonpy/commit/047e529fe4c888196c995ebc78c9354220a50a9b))

* refactor: add additional debug messages ([`b7750d7`](https://github.com/zabuldon/teslajsonpy/commit/b7750d77f557783ca7b4fe239c93e03094022112))

* refactor: add device_class to sensors ([`948b438`](https://github.com/zabuldon/teslajsonpy/commit/948b438b7cd53685e196573186eb2fc56dcd3fde))

* refactor: rename online sensor ([`97a40ff`](https://github.com/zabuldon/teslajsonpy/commit/97a40ff35d34e04b94d57e30be1e61e090030b37))

* refactor: change logging to vin ([`9bd66b9`](https://github.com/zabuldon/teslajsonpy/commit/9bd66b9cfa7a20bf04495554a4df3e6581496f7c))

### Unknown

* Merge pull request #56 from alandtse/online_sensor

feat: add online sensor ([`948a6e1`](https://github.com/zabuldon/teslajsonpy/commit/948a6e15cd3ae705f28bf837d05b78422aaa8e55))


## v0.2.3 (2020-01-14)

### Fix

* fix(setup.py): update required libraries
Closes #54 ([`1c423a3`](https://github.com/zabuldon/teslajsonpy/commit/1c423a312cca6199dfc6bba05f9b8190e9d74b0c))

### Unknown

* Merge pull request #55 from alandtse/#54

fix(setup.py): update required libraries ([`c3ad2dd`](https://github.com/zabuldon/teslajsonpy/commit/c3ad2ddbd535adcb99d6f91858755be70efeb688))


## v0.2.2 (2020-01-06)

### Fix

* fix(controller): convert old ids for commands ([`5aae7c4`](https://github.com/zabuldon/teslajsonpy/commit/5aae7c41e8c705f964a42ff39294c7c689aa7812))

* fix(controller): handle changing id from api
In some cases it appears the id will change. The controller now
transparently handles those changes. All internal dictionaries use the
vin to store data. ([`d8d11ed`](https://github.com/zabuldon/teslajsonpy/commit/d8d11ed94e201cfe7628ee1f30a1879977036f6c))

### Style

* style: rename vehicle_id to car_id
The use of vehicle_id was confusing as it is a separate field in the
Tesla api ([`b1c9588`](https://github.com/zabuldon/teslajsonpy/commit/b1c958824099df66afc5681940473236dc653963))


## v0.2.1 (2019-12-26)

### Chore

* chore: update docstyle for init ([`64466df`](https://github.com/zabuldon/teslajsonpy/commit/64466dfc61991fb4047a91e5c3830cf52e7188e6))

### Fix

* fix(controller): add lock for get_vehicles in update ([`4eb2855`](https://github.com/zabuldon/teslajsonpy/commit/4eb2855da23fdc86e0f96791f44d51c077046bb3))


## v0.2.0 (2019-11-13)

### Build

* build(pylintrc): lint tests directory ([`1e40a1a`](https://github.com/zabuldon/teslajsonpy/commit/1e40a1a98df6127d07edfe5afaf0f104d06e930f))

* build: add black ([`6c94425`](https://github.com/zabuldon/teslajsonpy/commit/6c94425255379d39cfbccd93f9cbead876b2459d))

### Ci

* ci: enable semantic-release

Signed-off-by: Alan Tse &lt;alandtse@gmail.com&gt; ([`79dc833`](https://github.com/zabuldon/teslajsonpy/commit/79dc833eae861e902a3c63402af4ff8149ce3488))

* ci: add pypi token

Signed-off-by: Alan Tse &lt;alandtse@gmail.com&gt; ([`4d2abb4`](https://github.com/zabuldon/teslajsonpy/commit/4d2abb4a166002cad7ef1ca4efccf6bf6d08471f))

* ci: enable upload to pypi ([`ff4938e`](https://github.com/zabuldon/teslajsonpy/commit/ff4938e1e151176016830a093c5657ddf0dfaa61))

* ci: add semantic-release.yaml

Signed-off-by: Alan Tse &lt;alandtse@gmail.com&gt; ([`ad276b5`](https://github.com/zabuldon/teslajsonpy/commit/ad276b503de55daa9926cca633aac18131bd8fae))

### Feature

* feat: add update_interval setting ([`c85f30c`](https://github.com/zabuldon/teslajsonpy/commit/c85f30cbdac47b2072f9e0de2f6d39feae9fbcac))

* feat: add charger current and voltage ([`96f0bfe`](https://github.com/zabuldon/teslajsonpy/commit/96f0bfef4a12ba658897b8c0446c6d5cf321a7a5))

* feat: convert to async
This version contains numerous changes in addition to the async conversion. It includes a new charging sensor, support for oauth, performance tweaks, and incorporation of black for formatting.
BREAKING CHANGE: API calls now require async
Closes #44, #47 ([`3bc94ad`](https://github.com/zabuldon/teslajsonpy/commit/3bc94adc4990c45507c9b457aa129e39c3176d9a))

### Performance

* perf: convert unnecessary async calls to sync ([`a827301`](https://github.com/zabuldon/teslajsonpy/commit/a827301e1fb06aea62f11a5ff85352fb5733ab4f))

### Style

* style: black ([`8eaef85`](https://github.com/zabuldon/teslajsonpy/commit/8eaef8559b16c55ffe3c53532be30d9dade95c96))

* style: correct isort for teslajsonpy ([`7bd4ad1`](https://github.com/zabuldon/teslajsonpy/commit/7bd4ad112ce2a9ed80830523b987dd2acf58e14c))

### Unknown

* Merge pull request #48 from alandtse/async

feat: convert to async ([`5d6fd92`](https://github.com/zabuldon/teslajsonpy/commit/5d6fd9233c2033debfccaae8c04a0c16306fabef))


## v0.1.0 (2019-10-23)

### Build

* build: add semantic-release ([`df2aa18`](https://github.com/zabuldon/teslajsonpy/commit/df2aa18eb493abd4323a9c9dec3b43af53b7441f))

* build(setup.py): change required python to &gt;= 3.6 ([`e647257`](https://github.com/zabuldon/teslajsonpy/commit/e647257d05ae207a1844eab3622b21eb6434ba39))

### Feature

* feat: expose car_type and car_version for entities ([`7aa48d5`](https://github.com/zabuldon/teslajsonpy/commit/7aa48d5578631ffbdd2f739ec86ee3ccec5636b3))

* feat: add vehicle_config ([`15282e4`](https://github.com/zabuldon/teslajsonpy/commit/15282e40eea70b503350a9e00d9362abd2f629d3))

### Fix

* fix: change initial type from bool to dict ([`98b238b`](https://github.com/zabuldon/teslajsonpy/commit/98b238b68a2f5a1ae199fa8eb64035f402293032))

* fix: change behavior to wake cars on first update ([`6a0e433`](https://github.com/zabuldon/teslajsonpy/commit/6a0e4335f0682de9b4ca3253b3376562b7ea7f25))

### Style

* style: address pylint errors ([`e5d59a9`](https://github.com/zabuldon/teslajsonpy/commit/e5d59a9ef5ed1c1428e32aaed814af41da562100))

* style: fix pylint errors ([`749a8b3`](https://github.com/zabuldon/teslajsonpy/commit/749a8b3b83969eb631367d701ab90e089c0628a1))

### Unknown

* Merge pull request #46 from alandtse/config_entry

feat: add support for HA config flow ([`46596cc`](https://github.com/zabuldon/teslajsonpy/commit/46596ccb841b5edc93a63d436423c8f49762bb3c))

* doc: fix typo ([`d5c9336`](https://github.com/zabuldon/teslajsonpy/commit/d5c93363e158e369f9ae87782abef7001da1e720))


## v0.0.26 (2019-03-29)

### Unknown

* Update repo documents and complete linting (#41)

* Truncate VIN and add display_name **breaks HA entities**

* Add sensor_type

* Fix ChargerConnectionSensor to reflect cable connection

* Begin adding test suites and linting

* Rename filenames to fix pylint snake_case errors

* Fix pylint errors and add initial linting

* Flesh out documentation and setup.py

* Fix import errors caused by case rename

* Fix call for built-in id instead of id_

* Add more verbose debugging for wrapper

* Cleanup redundant import

* Fix bug where list of online vehicles not updated (#39)

* Bump version to 0.0.25 (#40)

* Change to Apache-2.0 from WTFPL

* Bump version to 0.0.26 ([`673ecdb`](https://github.com/zabuldon/teslajsonpy/commit/673ecdb5c9483160fb1b97e30e62f2c863761c39))


## v0.0.25 (2019-03-06)

### Unknown

* Bump version to 0.0.25 (#40)

* Bump version ([`d155358`](https://github.com/zabuldon/teslajsonpy/commit/d15535865dc1a46519d43cbd22fe46bf4cdbc296))

* Fix bug where list of online vehicles not updated (#39) ([`84c916c`](https://github.com/zabuldon/teslajsonpy/commit/84c916c120c4d0ce0be9e9f29adf2db0fa212f27))


## v0.0.24 (2019-03-05)

### Unknown

* Fix bugs where car would not wake for command (#35) ([`6768552`](https://github.com/zabuldon/teslajsonpy/commit/6768552ef9ba98a9f0ebd62546e227d589d883a7))

* Merge pull request #17 from ultratoto14/charger-door-patch

Adding charger door lock ([`43df0db`](https://github.com/zabuldon/teslajsonpy/commit/43df0db14fe856d0400078fcf45c8dcecf8f880c))

* Handle case when door is opened and cable is locked. ([`cb79274`](https://github.com/zabuldon/teslajsonpy/commit/cb79274421821c9f4d3875c25ccfbc11cfc668e2))

* Adding charge port door lock. ([`9bc21c6`](https://github.com/zabuldon/teslajsonpy/commit/9bc21c6577480ec57d0a62438c1d1c8b0532dce4))

* Merge pull request #10 from alandtse/patch-1

Removing extraneous . after sensor ([`63e6ffd`](https://github.com/zabuldon/teslajsonpy/commit/63e6ffd478ac70c4c1b91214b5d87c8ff397a7ed))

* Merge pull request #8 from alandtse/updatetoggle

Adding update toggle for vehicles ([`4404b96`](https://github.com/zabuldon/teslajsonpy/commit/4404b961e35c4a34bbedd0c690af8e08aaf66cf8))

* Adding update toggle for vehicles ([`4d3b9f8`](https://github.com/zabuldon/teslajsonpy/commit/4d3b9f8213298085d6c89442fbad9ff2c6784e0b))

* Removing extraneous . after sensor ([`71edce3`](https://github.com/zabuldon/teslajsonpy/commit/71edce357983784deb08a4d085e7aabb268b9497))

* version bump ([`7d22342`](https://github.com/zabuldon/teslajsonpy/commit/7d22342f611971d786bfa640cb21a0c252894b99))

* markdown fix ([`f8c2539`](https://github.com/zabuldon/teslajsonpy/commit/f8c253923681f64a405be027e86b7045510ee9cb))

* Interface unification ([`6c25e1a`](https://github.com/zabuldon/teslajsonpy/commit/6c25e1ad1586328377fbd30857671bea1a582d5c))

* Remove whitespaces ([`9453433`](https://github.com/zabuldon/teslajsonpy/commit/94534334aac33807f5b58103c26a64ec890e3565))

* Version bump ([`e122f99`](https://github.com/zabuldon/teslajsonpy/commit/e122f99c3b429667c3570938efd2c8b5050fbf46))

* Merge pull request #5 from alandtse/newsensors

Thank you for contributing. Haven&#39;t thought  someone will help me with that :) ([`0eec891`](https://github.com/zabuldon/teslajsonpy/commit/0eec891aa086a560b2f5bc0d344925fe9a19e50b))

* Adding switch for max charging and sensors for odometer and estimated range. ([`cf16466`](https://github.com/zabuldon/teslajsonpy/commit/cf164663cf87494f5771c32d202c2fa365fb7028))

* Adding additional data checks for unavailibility. ([`c5e5ef1`](https://github.com/zabuldon/teslajsonpy/commit/c5e5ef19895eef55381c92c47f84475d4d40ae28))

* Adding checks for valid vehicle data before updating values ([`f8012af`](https://github.com/zabuldon/teslajsonpy/commit/f8012affb89c6f48a29694fd807ed872441d9c32))

* Version bump ([`7d6a8aa`](https://github.com/zabuldon/teslajsonpy/commit/7d6a8aa5ab6c2f4175b351ba8c31a481fce2fe36))

* Removed too broad 408 error code ([`5fa6300`](https://github.com/zabuldon/teslajsonpy/commit/5fa630024448437d5b8e3644a4acf0cd801f5e63))

* Fixed inclorrect rlock usage. Extended exceptions handler ([`af83868`](https://github.com/zabuldon/teslajsonpy/commit/af838685979350e76318cf02a7480efe6d88eb35))

* Fix for possible deadlock. ([`ca05c9c`](https://github.com/zabuldon/teslajsonpy/commit/ca05c9c3f43ae3d9e80b71aa0cb6b8463a3b73ca))

* Merge branch &#39;master&#39; of https://github.com/zabuldon/teslajsonpy ([`4500018`](https://github.com/zabuldon/teslajsonpy/commit/450001886c1ad16af94e9048bc57403a91c4a6e0))

* Refactoring. Version bump ([`a1ba8db`](https://github.com/zabuldon/teslajsonpy/commit/a1ba8dbb690316d6ff9d3b7ff5d799f078d37137))

* Update README.rst ([`6325446`](https://github.com/zabuldon/teslajsonpy/commit/632544674ed7f6bbda2f3798d9a768d76aae81fd))

* Update README.rst ([`a4c1055`](https://github.com/zabuldon/teslajsonpy/commit/a4c1055204e46d792b55b81fd964df213f3be764))

* Logging fix. ([`3493085`](https://github.com/zabuldon/teslajsonpy/commit/3493085476e0e094628bd7b4c5f69f3a567d53cc))

* Logging fix. ([`7e1d9f6`](https://github.com/zabuldon/teslajsonpy/commit/7e1d9f6fd3b5a5574b2147c77cbdfe5bd0147a63))

* Version bump. ([`da19170`](https://github.com/zabuldon/teslajsonpy/commit/da191704ddd4cc6f9525e55cb787f62b918ed183))

* prevent &#34;too many requests error&#34; ([`4829df3`](https://github.com/zabuldon/teslajsonpy/commit/4829df31217eb53bca5c311903e9a999912230b2))

* prevent &#34;too many requests error&#34; ([`a59dc3e`](https://github.com/zabuldon/teslajsonpy/commit/a59dc3e412a95165830a0d9962fb1aedb96e8ecb))

* fixing slow execution ([`3274d78`](https://github.com/zabuldon/teslajsonpy/commit/3274d78bac3865d7567194faa6564570da7e6e60))

* fixing slow execution ([`3130f73`](https://github.com/zabuldon/teslajsonpy/commit/3130f732301ae1634eb6b7f5481705aa2c244632))

* fixing slow execution ([`d047de3`](https://github.com/zabuldon/teslajsonpy/commit/d047de351cd976a77067c10a41413eb51ebd47f6))

* Typo fix. Remove debug import. ([`65cadfd`](https://github.com/zabuldon/teslajsonpy/commit/65cadfdeb8f222e86729ba716d686dd32c2e46c6))

* Renamed Parking Sensor to Parking Brake Sensor.
Requested in #2 ([`84a465c`](https://github.com/zabuldon/teslajsonpy/commit/84a465c30dfdeba15961a3bd36d92aaebdeb53ad))

* Version bump. ([`9ccba55`](https://github.com/zabuldon/teslajsonpy/commit/9ccba555443a7eac27ec179adea5ddc39ce744ec))

* Added support for ChargerSwitch.
Issue: #1 ([`fc7bca2`](https://github.com/zabuldon/teslajsonpy/commit/fc7bca2daccdc70be9ae20bb8d9873dc52982f2c))

* Fix for issues like: &#34;tesla lock took longer than the scheduled update interval 0:00:30&#34; in HASS. ([`e777840`](https://github.com/zabuldon/teslajsonpy/commit/e777840345e74f32788a6d3021b8e637c59299db))

* hass_type not defined issue fix. Version bump. ([`071d290`](https://github.com/zabuldon/teslajsonpy/commit/071d290a1cec24ca07ed4950b67c3ddd1ab26625))

* Merge conflict fix ([`8ebd58f`](https://github.com/zabuldon/teslajsonpy/commit/8ebd58f249b34c2dedb0e8b2f023f692e5bfcd56))

* Binary type added. Version bump. ([`b910382`](https://github.com/zabuldon/teslajsonpy/commit/b91038229d11df98b77abc38aab36a46bba5454f))

* Update setup.py

Version change ([`63b6bc5`](https://github.com/zabuldon/teslajsonpy/commit/63b6bc56fb298ba2efcc9e632eb556ccd051fd0e))

* Version bump ([`5aad0e0`](https://github.com/zabuldon/teslajsonpy/commit/5aad0e02803fbf268a687fe6a328c920a34b04dd))

* Lint fix. ([`34449b8`](https://github.com/zabuldon/teslajsonpy/commit/34449b8a716b8f8b5b9e46b73a7c5b18c97f6587))

* Refactoring for HASS ([`4ac4d9c`](https://github.com/zabuldon/teslajsonpy/commit/4ac4d9ca275d1eef8a959dc79d75032b55ea1db3))

* Initial commit ([`4fe78e9`](https://github.com/zabuldon/teslajsonpy/commit/4fe78e9b7733f90f4d46f91b086352a7ebd836c2))
