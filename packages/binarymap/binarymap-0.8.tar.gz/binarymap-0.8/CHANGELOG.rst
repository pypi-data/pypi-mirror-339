=========
Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com>`_.

0.8
---
- When using ``sites_as_str``, sites can be arbitrary strings.

0.7
---
- Test with GitHub Actions rather than Travis, lint with ``ruff`` rather than ``flake8``.
- Switch ``scipy`` sparse matrices to arrays (see [this issue](https://github.com/jbloomlab/binarymap/issues/6)).

0.6
---
- Allow negative site numbers.

0.5
---
- Added ``sites_as_str`` option to ``BinaryMap`` to enable non-integer site numbers (e.g., "214a").

- ``black`` formatting of code.

0.4
---
- Gaps are now allowed in ``allowed_subs`` as a ``-`` character.

- Added ``AAS_NOSTOP_WITHGAP`` and ``AAS_WITHSTOP_WITHGAP``.

- Substitutions in ``BinaryMap`` now sorted according to input alphabet (before they were alphabetical).

0.3
---
Added ``binary_sites`` attribute.

0.2
----
Added ``allowed_subs`` parameter.

0.1
----
Initial version of code ported from `dms_variants version 0.8.10 <https://github.com/jbloomlab/dms_variants/tree/0.8.10>`_.

