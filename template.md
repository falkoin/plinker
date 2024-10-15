+++
title = '{{title}}'
date = {{date_today}}
draft = false
+++

# Links
{% for description, link in links %}
{{description}} [[{{loop.index}}]]({{link}}) 
{% endfor %}
