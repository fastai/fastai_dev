{% extends 'markdown.tpl' %}

<!-- Add Div for input area -->
{% block input %}
<div class="input_area">
{{ super() }}
</div>
{% endblock input %}

{% block data_text %}
{:.output_data_text}
```
{{ output.data['text/plain'] }}
```
{% endblock data_text %}


{% block traceback_line  %}
{:.output_traceback_line}
```
{{ line | strip_ansi }}
```
{% endblock traceback_line  %}

<!-- Tell Jekyll not to render HTML output blocks as markdown -->
{% block data_html %}
<div markdown="0">
{{ output.data['text/html'] }}
</div>
{% endblock data_html %}
