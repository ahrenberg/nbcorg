""" Orgmode Exporter class """

# Copyright (c) Lukas Ahrenberg
# Distributed under the terms of the Modified BSD License

from traitlets import default, Bool, Unicode, TraitError, validate, observe
from traitlets.config import Config
from nbconvert.exporters import TemplateExporter
import os.path

class OrgmodeExporter(TemplateExporter):
    """
    Exports to Emacs orgmode document (.org).
    """
    export_from_notebook = "Orgmode"
    output_mimetype = 'text/x-org'


    @default('file_extension')
    def _file_extension_default(self):
        return '.org'
    
    @default('template_file')
    def _template_file_default(self):
        return 'base.tpl'

    @property
    def template_path(self):
        bp = super(OrgmodeExporter, self).template_path
        return bp  + [os.path.join(os.path.dirname(__file__), "templates")]

    @default('raw_mimetypes')
    def _raw_mimetypes_default(self):
        return ['text/x-org', '']

    @validate('raw_mimetypes')
    def _raw_mimetypes_validate(self,prop):
        mtypes = prop['value']
        # Check if there should be anything exported.
        if(self.supported_raw_as_export):
            mtypes = mtypes + ['text/html', 'text/latex']
        return mtypes

    exclude_execute_result = Bool(False,
        help="""
        Do not include execution results in output data.

        Execute results are special outputs separate from display data.
        The `[matplotlib.Y.Z at 0x123456789ABCDEF]` kind of strings in the 
        notebook when plotting a matplotlib figure is one example.
        """
    ).tag(config=True)

    supported_raw_as_export = Bool(True,
        help="""
        Wrap raw LaTeX and HTML cells in org export blocks.

        Standard behaviour for nbconvert exporters when dealing with raw cells 
        is to include mime types requiring no conversion verbatim, while 
        ignoring any other ones. 
        The mime-types to include is given by the configuration option
        `raw_mimetypes`, which for orgmode defaults to 'text/x-org' and '' 
        (corresponding to `None Raw NBConvert Format`).
        However, similar to the jupyter notebook, orgmode has the ability to 
        mark blocks for inclusions verbatim when exporting to a set of supported
        formats (currently HTML and LaTeX). It therefore makes sense to convert
        raw cells in these formats to the corresponding raw blocks.
        When `supported_raw_as_export` is set to `True` the mime types 
        'text/html' and 'text/latex' are added to `raw_mimetypes`, and HTML and 
        LaTeX raw cells are wrapped in export blocks rather than included 
        verbatim (other raw cell content is still represented verbatim).
        When `supported_raw_as_export` is set to `False` this functionality is
        turned off and only cells with mime types in `raw_mimetypes` are 
        included. 
        """
    ).tag(config=True)
    
    use_output_drawer = Bool(False,
        help="""
        If True, output cell contents are placed in drawers.
        """
    ).tag(config=True)
    
    output_drawer_name = Unicode('RESULTS',
        help="""
        Drawer name for output cell content.
        
        Only applicable if `OrgmodeExporter.use_output_drawer=True`.
        Output cell content will be placed in an org drawer of this name.
        """
    ).tag(config=True)

    use_input_drawer = Bool(False,
        help="""
        If True, input cell contents are placed in drawers.
        """
    ).tag(config=True)
    
    input_drawer_name = Unicode('INPUT',
        help="""
        Drawer name for input cell content.
        
        Only applicable if `OrgmodeExporter.use_input_drawer=True`.
        Input cell content will be placed in an org drawer of this name.
        """
    ).tag(config=True)   

    src_block_options = Unicode('',
        help = """
        String of org src block extra options.

        This string will be added after the language name in all input cell 
        source code blocks.
        Input code will be wrapped in a block on the form 
        
           #+BEGIN_SRC {{ lang }} {{src_block_options}}
           {{ code }}
           #+END_SRC

        where `lang` and `code` is given by the notebook.

        This option is useful to add org-babel options so that source blocks
        can be executed from org-mode as well.

        E.g. `OrgmodeExporter.src_block_options=':session :results output'`
        which will instruct org-babel to execute each source block in a session
        just like a jupyter notebook.

        (See org-babel for more information, and note that further configuration
        may be needed to get ipython specifics, such as cell magic, to work.)
        """
    ).tag(config=True)
    
    html_data_as = Unicode('export',
        help = """
        How HTML output data should be handled.
        
        Allowed values: 
           export  - Enclose HTML in `#+BEGIN_EXPORT html ...`-block.
           example - Enclose HTML in `#+BEGIN_EXAMPLE ... `-block.
           import  - Use pandoc to convert HTML to org. Results may vary... Much of likely still returned as HTML by pandoc and enclosed in `+#BEGIN_HTML...`-blocks.
        """
    ).tag(config=True)
    
    @validate('html_data_as')
    def _html_data_as_validate(self, prop):
        val = prop['value']
        if val.lower() not in ("import", "example", "export"):
            raise TraitError("Unrecognized option '{0}'; valid options for html_data_as: 'import', 'example', 'export'.".format(val))
        return val.lower()

    latex_data_as = Unicode('export',
        help = """
        How LaTeX output data should be handled.
        
        Allowed values: 
           export  - Enclose LaTeX in `#+BEGIN_EXPORT latex ...`-block.
           example - Enclose LaTeX in `#+BEGIN_EXAMPLE ... `-block.
           import  - Use pandoc to convert LaTeX to org. Results may vary... pandoc likely wraps it in `#+BEGIN_SRC latex`-blocks.
        """
    ).tag(config=True)
    
    @validate('latex_data_as')
    def _latex_data_as_validate(self, prop):
        val = prop['value']
        if val.lower() not in ("import", "example", "export"):
            raise TraitError("Unrecognized option '{0}'; valid options for latex_data_as: 'import', 'example', 'export'.".format(val))
        return val.lower()

    markdown_data_as = Unicode('import',
        help = """
        How markdown output data should be handled.
        
        Allowed values: 
           example - Enclose markdown in `#+BEGIN_EXAMPLE ... `-block.
           import  - Use pandoc to convert markdown to org. 
        """
    ).tag(config=True)
    
    @validate('markdown_data_as')
    def _markdown_data_as_validate(self, prop):
        val = prop['value']
        if val.lower() not in ("import", "example" ):
            raise TraitError("Unrecognized option '{0}'; valid options for markdown_data_as: 'import', 'example'.".format(val))
        return val.lower()

    javascript_data_as = Unicode('html',
        help = """
        How javascript output data should be handled.
        
        Allowed values: 
           html - Place the js code in HTML <SCRIPT> tag and create placement <DIV> 
                  inside `#+BEGIN_EXPORT html ...` block.
           source - Place js code inside `#+BEGIN_SRC js`-block.
           example - Enclose javascript in `#+BEGIN_EXAMPLE ... `-block.
           ignore - Ignore javascript blocks.
        """
    ).tag(config=True)
    
    @validate('javascript_data_as')
    def _javascript_data_as_validate(self, prop):
        val = prop['value']
        if val.lower() not in ("html", "source", "example", "ignore" ):
            raise TraitError("Unrecognized option '{0}'; valid options for javascript_data_as: 'html', 'source', 'example'.".format(val))
        return val.lower()


    
    @property
    def default_config(self):
        c = Config({
            'ExtractOutputPreprocessor': {'enabled': True},
            'NbConvertBase': {
                'display_data_priority': [
                    'text/latex',
                    'text/html',
                    'text/markdown',
                    'application/javascript',
                    'image/svg+xml',
                    'image/png',
                    'image/jpeg',
                    'text/plain'
                ]
            },
            'HighlightMagicsPreprocessor': {
                'enabled': True
                },
            })
        c.merge(super(OrgmodeExporter, self).default_config)
        return c
  
        
    def from_notebook_node(self, nb, resources=None, **kw):
        resources = self._init_resources(resources)
        if 'nbcorg'not in resources:
            resources['nbcorg'] = {}
        resources['nbcorg']['use_output_drawer'] = self.use_output_drawer
        resources['nbcorg']['output_drawer_name'] = self.output_drawer_name
        resources['nbcorg']['use_input_drawer'] = self.use_input_drawer
        resources['nbcorg']['input_drawer_name'] = self.input_drawer_name
        resources['nbcorg']['src_block_options'] = self.src_block_options
        resources['nbcorg']['html_data_as'] = self.html_data_as.lower()
        resources['nbcorg']['latex_data_as'] = self.latex_data_as.lower()
        resources['nbcorg']['markdown_data_as'] = self.markdown_data_as.lower()
        resources['nbcorg']['javascript_data_as'] = self.javascript_data_as.lower()
        resources['nbcorg']['include_execute_result'] = not self.exclude_execute_result
        
        return super(OrgmodeExporter, self).from_notebook_node(nb,
                                                               resources=resources,
                                                               **kw)

class OrgmodeBabelExporter(OrgmodeExporter):
    """
    Exports to Emacs orgmode document, ignoring output cells and adding babel
    execution block to code blocks.
    """
    export_from_notebook = "Orgmode babel"
    output_mimetype = 'text/x-org'

    @property
    def default_config(self):
        c = Config({
            'OrgmodeExporter' : {
                'src_block_options' : ':session :results output',
                'exclude_output' : True,
                },
        })
        c.merge(super(OrgmodeBabelExporter, self).default_config)
        return c
                   
