{%- extends 'display_priority.tpl' -%}

{% block header %}
{%- set nb_title = nb.metadata.get('title', '') or resources['metadata']['name'] -%}
{%- if nb_title -%}
#+TITLE: {{ nb_title }}
{% endif -%}
{% if 'authors' in nb.metadata %}
#+AUTHOR: {{ ', '.join(nb.metadata.authors) }}
{% endif -%} 
{% endblock header %}

{%- block input scoped -%}
  {%- set bl_lang = cell.metadata.magics_language or nb.metadata.language_info.name or '' -%}
  {%- set bl_opts = resources.nbcorg.src_block_options or '' %}
#+BEGIN_SRC {{ bl_lang }} {{ bl_opts }}
{{ cell.source }}
#+END_SRC
{%- endblock input -%}


{%- block markdowncell scoped -%}
{{ cell.source | convert_pandoc(from_format="markdown", to_format="org")}} 
{%- endblock markdowncell -%}

{% block any_cell %}
{{ super() }}
{% endblock any_cell %}


{% block input_group scoped %} 
{% if resources.nbcorg.use_input_drawer %}
:{{ resources.nbcorg.get('input_drawer_name', 'INPUT') }}:
{%- endif -%}
{{- super() -}} 
{%- if resources.nbcorg.use_input_drawer %}
:END:
{% endif -%} 
{% endblock input_group %} 

{% block output_group scoped %}    
{% if resources.nbcorg.use_output_drawer %} 
:{{ resources.nbcorg.get('output_drawer_name', 'RESULTS') }}: 
{%- endif -%}     
{{- super() -}} 
{%- if resources.nbcorg.use_output_drawer %} 
:END:
{% endif -%}     
{% endblock output_group %} 

{% block outputs %}   
{{ super() }}  
{%- endblock outputs -%}   


{# Seems like execute_result block are redefined to look like display_data in #}
{# the templates for latex,markdown, and html (at least) in the nbconvert code #}
{# so I will do the same here. Think it makes sense, but just this note as it is #}
{# not indicated in the figures at #}
{# https://nbconvert.readthedocs.io/en/latest/customizing.html  #}

{%- block execute_result scoped -%}
{%- if resources.nbcorg.include_execute_result -%}
{%- block data_priority scoped -%}
{{- super() -}}
{%- endblock data_priority -%}
{%- endif -%}
{%- endblock execute_result -%}

{%- block stream -%}
#+BEGIN_EXAMPLE
{{ output.text }}
#+END_EXAMPLE
{%- endblock stream -%}

{%- block data_html scoped %}
{%- set d_opt = resources.nbcorg.get('html_data_as','export') -%}
{%- if d_opt == 'export' -%}
#+BEGIN_EXPORT html
{{ output.data['text/html'] }}
#+END_EXPORT
{%- elif d_opt == 'import' -%}
{{ output.data['text/html'] | convert_pandoc(from_format="html", to_format="org") }}
{%- else -%}
#+BEGIN_EXAMPLE
{{ output.data['text/html'] }}
#+END_EXAMPLE
{%- endif -%}
{% endblock data_html -%}


{# The js HTML wrapping is based on the code found in nbconvert's html template, #}
{# which in turns seems to be a bit of html magic. E.g. overriding `element`. #}
{# In this version the jquery $ function has been replaced with #}
{# document.getElementById. #}
{%- block data_javascript scoped %}
{%- set d_opt = resources.nbcorg.get('javascript_data_as','html') -%}
{%- if d_opt == 'html' %}
#+BEGIN_EXPORT html
{% set div_id = uuid4() %}
<div id="{{ div_id }}"></div>
<div>
<script type="text/javascript">
var element = document.getElementById('{{ div_id }}');
{{ output.data['application/javascript'] }}
</script>
</div>
#+END_EXPORT
{%- elif d_opt == 'source' -%}
{%- set bl_lang = cell.metadata.magics_language or nb.metadata.language_info.name or '' -%}
{%- set bl_opts = resources.nbcorg.src_block_options or '' %}
#+BEGIN_SRC js
{{ output.data['application/javascript'] }}
#+END_SRC
{%- elif d_opt == 'example' %}
#+BEGIN_EXAMPLE
{{ output.data['application/javascript'] }}
#+END_EXAMPLE
{%- else -%}
{# Nothing #}
{%- endif -%}
{% endblock data_javascript -%}

{%- block data_latex scoped %}
{%- set d_opt = resources.nbcorg.get('latex_data_as','export') -%}
{%- if d_opt == 'export' -%}
#+BEGIN_EXPORT latex
{{ output.data['text/latex'] }}
#+END_EXPORT
{%- elif d_opt == 'import' -%}
{{ output.data['text/latex'] | convert_pandoc(from_format="latex", to_format="org") }}
{%- else -%}
#+BEGIN_EXAMPLE
{{ output.data['text/latex'] }}
#+END_EXAMPLE
{%- endif -%}
{%- endblock data_latex -%}

{%- block data_markdown scoped %}
{%- set d_opt = resources.nbcorg.get('markdown_data_as','import') -%}
{%- if d_opt == 'import' -%}
{{ output.data['text/markdown'] | convert_pandoc(from_format="markdown", to_format="org") }}
{%- else -%}
#+BEGIN_EXAMPLE
{{ output.data['text/markdown'] }}
#+END_EXAMPLE
{%- endif -%}
{% endblock data_markdown -%}

{%- block data_text %}
#+BEGIN_EXAMPLE
{{ output.data['text/plain'] }}
#+END_EXAMPLE
{%- endblock data_text -%}


{# Bunch of file types handled the same, might be improved by overriding the
display_data_priority block. #}

{%- block data_svg %}
[[file:{{ output.metadata.filenames['image/svg+xml'] | path2url }}]] 
{%- endblock data_svg -%}

{%- block data_png %}
[[file:{{ output.metadata.filenames['image/png'] | path2url }}]] 
{%- endblock data_png -%}

{%- block data_jpg %}
[[file:{{ output.metadata.filenames['image/jpeg'] | path2url }}]] 
{%- endblock data_jpg -%}

{%- block data_pdf %}
[[file:{{ output.metadata.filenames['application/pdf'] | path2url }}]]
{%- endblock data_pdf -%}

{# Overriding rawcell in order to allow wrapping of HTML and LaTeX. #}
{%- block rawcell -%}
{%- set cmt = cell.metadata.get('raw_mimetype', '').lower() -%}
{%- if cmt in resources.get('raw_mimetypes', ['']) -%}
{%- if cmt == 'text/html' -%} #+BEGIN_EXPORT html
{%- elif cmt == 'text/latex' -%} #+BEGIN_EXPORT latex {%- endif %} 
{{ super() }}
{% if cmt in ['text/html', 'text/latex'] -%} #+END_EXPORT {%- endif -%}
{%- endif -%}
{%- endblock rawcell -%}

{% block unknowncell %}
# [nbcorg] unknown type {{ cell.type }}
{% endblock unknowncell %}

{% block error %}
#+BEGIN_EXAMPLE
{{ super() }}
#+END_EXAMPLE
{% endblock error %}

{% block traceback_line %}
{{ line | strip_ansi }}
{% endblock traceback_line %}
