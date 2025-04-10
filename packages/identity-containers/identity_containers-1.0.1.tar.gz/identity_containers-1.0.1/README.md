## Introduction

This module implements dicts and sets that compare items based on identity rather than value. This
allows them to store unhashable objects.

Usage example:

```python
from identity_containers import IdentitySet

foo = []
bar = []

id_set = IdentitySet([foo])

print(foo in id_set)  # True
print(bar in id_set)  # False
```

The following classes exist:

-   `IdentitySet`
-   `IdentityDict`
-   `IdentityDefaultDict`
