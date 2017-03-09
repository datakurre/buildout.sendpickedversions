Changelog
=========

1.0.0rc3 (unreleased)
---------------------

- Fix data format for push
  [datakurre]


1.0.0rc2 (2017-03-09)
---------------------

- Add support for zc.buildout >= 2.2.5
  [datakurre]

- Add support for saving output to file with file:// -starting URL as
  *build-data-url*
  [datakurre]

- Change to use reuquests for posting to *build-data-url*
  [datakurre]


1.0-alpha.1 (2013-03-20)
------------------------

- Returns a lots of new information about buildout including whole buildout
  section (with defaults and computed values as well).
- Returns absolutely all package requirements with versions numbers (both
  picked version and fuzzy version requirement like zope.interface >= 3.8).
- Picks buildout name from directory name - no need to specify buildoutname
  to buildout config anymore (though you still can if you want to).


0.3 (2012-10-11)
----------------

- Performance optimizations (ported from zc.buildout).


0.2 (2011-10-16)
----------------

- Sends data urlencoded.


0.1 (2011-10-16)
----------------

- Initial import
