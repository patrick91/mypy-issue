from __future__ import annotations

import strawberry

x: MyUnion

MyUnion = strawberry.union("Entity", types=(str, int))


reveal_type(MyUnion)
reveal_type(x)
