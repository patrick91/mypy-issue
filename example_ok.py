from __future__ import annotations

import strawberry

MyUnion = strawberry.union("Entity", types=(str, int))

x: MyUnion

reveal_type(MyUnion)
reveal_type(x)
