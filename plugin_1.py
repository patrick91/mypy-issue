from typing import Callable, Optional

from mypy.nodes import (
    Expression,
    GDEF,
    IndexExpr,
    NameExpr,
    SymbolTableNode,
    TupleExpr,
    TypeAlias,
)
from mypy.plugin import (
    DynamicClassDefContext,
    Plugin,
    SemanticAnalyzerPluginInterface,
)

from mypy.types import UnionType


def _get_type_for_expr(expr: Expression, api: SemanticAnalyzerPluginInterface):
    if isinstance(expr, NameExpr):
        return api.named_type(expr.name)

    if isinstance(expr, IndexExpr):
        type_ = _get_type_for_expr(expr.base, api)
        type_.args = [_get_type_for_expr(expr.index, api)]

        return type_

    raise ValueError(f"Unsupported expression f{type(expr)}")


def union_hook(ctx: DynamicClassDefContext) -> None:
    types = ctx.call.args[1]

    if isinstance(types, TupleExpr):
        type_ = UnionType(tuple(_get_type_for_expr(x, ctx.api) for x in types.items))

        type_alias = TypeAlias(
            type_,
            fullname=ctx.api.qualified_name(ctx.name),
            line=ctx.call.line,
            column=ctx.call.column,
        )

        ctx.api.add_symbol_table_node(
            ctx.name, SymbolTableNode(GDEF, type_alias, plugin_generated=False)
        )


class StrawberryPlugin(Plugin):
    def get_dynamic_class_hook(
        self, fullname: str
    ) -> Optional[Callable[[DynamicClassDefContext], None]]:
        if "strawberry.union" in fullname:
            return union_hook

        return None


def plugin(version: str):
    return StrawberryPlugin
