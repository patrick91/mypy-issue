# MyPy custom TypeAlias plugin issue

This repo reproduces a bug occurring when using a plugin that creates a new
typealias for a variable.

The plugin uses `get_dynamic_class_hook` to add a new symbol node, but it looks
like something goes wrong when the type is being used before it is declared.

To test the beahviour run:

```sh
poetry run mypy example.py
```

```txt
example.py:7: error: Cannot assign multiple types to name "MyUnion" without an explicit "Type[...]" annotation
example.py:10: note: Revealed type is 'builtins.object'
example.py:11: note: Revealed type is 'Union[builtins.str, builtins.int]'
Found 1 error in 1 file (checked 1 source file)
```

While this other example seems to work fine:

```sh
poetry run mypy example_ok.py
```

```txt
example_ok.py:9: note: Revealed type is 'builtins.object'
example_ok.py:10: note: Revealed type is 'Union[builtins.str, builtins.int]'
```
