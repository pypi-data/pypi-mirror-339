# steno-python

## Usage

The most basic usage. Call the `steno.compress` function on your prompt. Get back a
shorter, functionally equilvalent version.

```python
import steno

prompt = "You crossed the line. People trusted you and they died. You gotta go down."
print(steno.compress(prompt))
You crossed line. People trusted you, died. Go down.
********************************************************************************
Original text: 17 tokens
Compressed text: 13 tokens
Compression: 23.53%
Compression took 615.38 ms
```

Use the `<literal>` tag to specify content you do not want modified.

```python
import steno
prompt = """
Yeah <literal>(You can't touch this)</literal>
Look, man <literal>(You can't touch this)</literal>
You better get hype, boy, because you know you can't <literal>(You can't touch this)</literal>
"""
print(steno.compress(prompt))
Yeah. (You can't touch this) (You can't touch this)
 Look man. (You can't touch this) You better get hype, know you.
```
