import xfox

@xfox.addfunc(xfox.funcs, name="abs")
async def absolute_value(number: str, **kwargs):
    try:
        num = float(number)
        return str(abs(num))
    except ValueError:
        return ":x: Invalid number value en `$abs[]`"
