# brand.yml Python Package


Create reports, apps, dashboards, plots and more that match your
company’s brand guidelines with a single `_brand.yml` file.

**brand.yml** is a simple, portable YAML file that codifies your
company’s brand guidelines into a format that can be used by
[Quarto](https://quarto.org), Python and R tooling to create branded
outputs. Our goal is to support unified, branded theming for all of
[Posit’s open source tools](https://posit.co/products/open-source/)—from
web applications to printed reports to dashboards and presentations—with
a consistent look and feel.

With a single `_brand.yml` file you can collect brand logos, colors,
fonts and typographic choices, typically found in your company’s brand
guidelines. This `_brand.yml` can be used [Quarto](https://quarto.org)
and [Shiny for Python](https://shiny.posit.co/py) to instantly basic
themes that match the brand guidelines.

## Example

``` python
from brand_yml import Brand

brand = Brand.from_yaml_str(
    # Typically, this file is stored in `_brand.yml`
    # and read with `Brand.from_yaml()`.
    """
    meta:
      name: Posit Software, PBC
      link: https://posit.co
    color:
      palette:
        pblue: "#447099"
        green: "#72994E"
        teal: "#419599"
        orange: "#EE6331"
        purple: "#9A4665"
        gray: "#707073"
      primary: blue
      secondary: gray
      success: green
      info: teal
      warning: orange
      danger: purple
    typography:
      base:
        family: Open Sans
        weight: 300
    """
)
```

``` python
brand.meta.name
```

    BrandMetaName(full='Posit Software, PBC')

``` python
brand.color.primary
```

    'blue'

``` python
brand.typography.base.model_dump()
```

    {'family': 'Open Sans', 'weight': 300, 'size': None, 'line_height': None}

## Installation

### From PyPI

``` bash
uv pip install brand_yml
```

### From GitHub

``` bash
uv pip install "git+https://github.com/posit-dev/brand-yml"
```
