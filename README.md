[![Build Status](https://travis-ci.org/RedHatSatellite/satellite-sanity.svg?branch=master)](https://travis-ci.org/RedHatSatellite/satellite-sanity)

satellite-sanity
================

Tooling to verify Red Hat Satellite health by checking for requirements, common issues, service status, etc.

Running the tool
----------------

If you have just cloned this GIT repo to your Red Hat Satellite, just run:

```sh
# cd satellite-sanity/
# ./satellite-sanity -h
# ./satellite-sanity --list-tags   # show available rule's tags
# ./satellite-sanity -t general,Satellite_5   # if you are on Satellite 5
# ./satellite-sanity -t general,Satellite_6   # if you are on Satellite 6
```

If you are running on system with rpm installed, just drop that `./` from above and run `satellite-sanity`.

Example output
--------------

```sh
$ ./satellite-sanity -t general
Selected tag(s): general
ERROR:satellite_sanity.config:Data not available for neighbour_table_overflow
[ PASS ] Check that hostname is configured properly (hostname_matches)
[ SKIP ] Check for ARP cache being full signs (neighbour_table_overflow)
[ FAIL ] Just a demo rule which keeps failing (example_fails)
         This text explains what is wrong, can use data returned by main()
         'dhcp131-38.brq.redhat.com' and provides howto and/or links to more info
```

In this example rule `hostname_matches` passed (see `satellite_sanity/rules/hostname_matches.py`), rule `neighbour_table_overflow` is skippet (because I have executed the tool as normal user so the tool was not able to read `/var/log/messages`, see `satellite_sanity/rules/neighbour_table_overflow.py`) and rule `example_fails` detected problem (well, it does all the time, see `satellite_sanity/rules/example_fails.py`) and provided some hints on what is going on.

Building rpm
------------

Assuming you are on a recent Fedora system:

```sh
$ ./makedist   # generate tarball
$ ls ~/rpmbuild/SOURCES/satellite-sanity-0.1.tar.gz   # ensure tarball is where we want it
$ rpmbuild -ba satellite-sanity.spec
```

Running internal tests
----------------------

```sh
# ./tests.py   # unit tests
# ./tests.sh   # kinda integration tests
```
