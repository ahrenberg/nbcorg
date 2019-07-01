# nbcorg - A jupyter notebook to orgmode exporter for nbconvert

This is an [nbconvert](https://github.com/jupyter/nbconvert) exporter to convert an ipython/jupyter notebook to [orgmode](https://orgmode.org/) with multiple options for treating source code and output blocks.

## Installation and getting started

nbcorg can be installed from the command line with pip, e.g,
```
pip install nbcorg
```

This should install the software with dependencies, as well as create entry points for the orgmode exporters in nbconvert.

## Using nbcorg
Once installed, the orgmode exporters can be selected using the `nbconvert --to` switch, e.g,
```
jupyter nbconvert --to orgmode mynotebook.ipynb
```

If you'd rather run from source without installation, you may do so from the nbcorg directory using the full qualified name [as described in the nbconvert documentation](https://nbconvert.readthedocs.io/en/latest/external_exporters.html#using-a-custom-exporter-without-entrypoints), e.g,
```
jupyter nbconvert --to nbcorg.OrgmodeExporter mynotebook.ipynb
```

### Included exporters
nbcorg functionality can be tuned using command line switches, as described below, however for convenience the package includes a couple named exporters with different default values for these.

#### `orgmode` (`nbcorg.OrgmodeExporter`)
This is the base exporter with default values for options and switches as described below

#### `orgmode_babel` (`nbcorg.OrgmodeBabelExporter`)
Ignores all output and appends `:session :results output` to code blocks. Useful if a notebook should be converted to a literate programming org file. Note that the source code language is at the moment derived from notebook metadata, and for instance an ipython session is given as 'python', meaning that if you use cell magic you may need to do some tweaks to get it to work.

This a convenience exporter, running
```
jupyter nbconvert --to orgmode-babel mynotebook.ipynb
```
is the same as
```
jupyter nbconvert --to orgmode --OrgmodeExporter.src_block_options=':session :results output' --OrgmodeExporter.exclude_output=True
```

### Configuration options
For a list of nbconfig configuration options also applicable to the orgmode exporters see the nbconvert manual for [exporter](https://nbconvert.readthedocs.io/en/latest/config_options.html#exporter-options) and [preprocessor](https://nbconvert.readthedocs.io/en/latest/config_options.html#preprocessor-options) options. (In particular those applicable to `TemplateExporter` and `ExtractOutputPrecprocessor`.)

`nbcorg.OrgmodeExporter` defines also the following additional options:

#### `--OrgmodeExporter.exclude_execute_result=<Bool>`
Default: False

Do not include execution results in output data.
Execute results are special outputs separate from display data. The
`[matplotlib.Y.Z at 0x123456789ABCDEF]` kind of strings in the  notebook
when plotting a matplotlib figure is one example.

#### `--OrgmodeExporter.exclude_raw=<Bool>`
Default: False

This allows you to exclude raw cells from all templates if set to True.

#### `--OrgmodeExporter.html_data_as=<Unicode>`
Default: `export`

How HTML output data should be handled.

Allowed values: 
- `export` - Enclose HTML in `#+BEGIN_EXPORT html ...`-block.
- `example` - Enclose HTML in `#+BEGIN_EXAMPLE ... `-block.
- `import` - Use pandoc to convert HTML to org. Results may vary... Much of likely still returned as HTML by pandoc and enclosed in `+#BEGIN_HTML...`-blocks.

#### `--OrgmodeExporter.input_drawer_name=<Unicode>`
Default: `INPUT`

Drawer name for input cell content.
Only applicable if `OrgmodeExporter.use_input_drawer=True`. Input cell
content will be placed in an org drawer of this name.

#### `--OrgmodeExporter.javascript_data_as=<Unicode>`
Default: `html`

How javascript output data should be handled.

Allowed values: 
- `html` Place the js code in HTML <SCRIPT> tag and create placement <DIV> inside `#+BEGIN_EXPORT html ...` block.
- `source` Place js code inside `#+BEGIN_SRC js`-block.
- `example` Enclose javascript in `#+BEGIN_EXAMPLE ... `-block.
- `ignore` - Ignore javascript blocks.

#### `--OrgmodeExporter.latex_data_as=<Unicode>`
Default: `export`

How LaTeX output data should be handled.

Allowed values: 
- export  - Enclose LaTeX in `#+BEGIN_EXPORT latex ...`-block.
- example - Enclose LaTeX in `#+BEGIN_EXAMPLE ... `-block.
- import - Use pandoc to convert LaTeX to org. Results may vary... pandoc likely wraps it in `#+BEGIN_SRC latex`-blocks.

#### `--OrgmodeExporter.markdown_data_as=<Unicode>`
Default: `import`

How markdown output data should be handled.

Allowed values: 
- `example` - Enclose markdown in `#+BEGIN_EXAMPLE ... `-block.
- `import`  - Use pandoc to convert markdown to org.

#### `--OrgmodeExporter.output_drawer_name=<Unicode>`
Default: `RESULTS`

Drawer name for output cell content.
Only applicable if `OrgmodeExporter.use_output_drawer=True`. Output cell
content will be placed in an org drawer of this name.

#### `--OrgmodeExporter.src_block_options=<Unicode>`
Default: `` (empty string)

String of org src block extra options.
This string will be added after the language name in all input cell  source
code blocks. Input code will be wrapped in a block on the form
```
#+BEGIN_SRC {{ lang }} {{src_block_options}}
   {{ code }}
   #+END_SRC
```
where `lang` and `code` is given by the notebook.
This option is useful to add org-babel options so that source blocks can be
executed from org-mode as well.
E.g. `OrgmodeExporter.src_block_options=':session :results output'` which
will instruct org-babel to execute each source block in a session just like
a jupyter notebook.
(See org-babel for more information, and note that further configuration may
be needed to get ipython specifics, such as cell magic, to work.)

#### `--OrgmodeExporter.supported_raw_as_export=<Bool>`
Default: True

Wrap raw LaTeX and HTML cells in org export blocks.
Standard behaviour for nbconvert exporters when dealing with raw cells  is
to include mime types requiring no conversion verbatim, while  ignoring any
other ones.  The mime-types to include is given by the configuration option
`raw_mimetypes`, which for orgmode defaults to 'text/x-org' and ''
(corresponding to `None Raw NBConvert Format`). However, similar to the
jupyter notebook, orgmode has the ability to  mark blocks for inclusions
verbatim when exporting to a set of supported formats (currently HTML and
LaTeX). It therefore makes sense to convert raw cells in these formats to
the corresponding raw blocks. When `supported_raw_as_export` is set to
`True` the mime types  'text/html' and 'text/latex' are added to
`raw_mimetypes`, and HTML and  LaTeX raw cells are wrapped in export blocks
rather than included  verbatim (other raw cell content is still represented
verbatim). When `supported_raw_as_export` is set to `False` this
functionality is turned off and only cells with mime types in
`raw_mimetypes` are  included.

#### `--OrgmodeExporter.use_input_drawer=<Bool>`
Default: False

If True, input cell contents are placed in drawers.

#### `--OrgmodeExporter.use_output_drawer=<Bool>`
Default: False

If True, output cell contents are placed in drawers.

## Dependencies
nbcorg is dependent on the following software

- [nbconvert](https://github.com/jupyter/nbconvert)
- [pandoc](https://github.com/jgm/pandoc)

## Authors

- Lukas Ahrenberg

## License
This project is licensed under the Modified BSD License. See [LICENSE](LICENSE) for text.
