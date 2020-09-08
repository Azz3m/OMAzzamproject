{% if item.video_titles_linker %}
            related videos :
           {% for item in item.video_titles_linker %}
             {{ item }}  ,
           {% endfor %}
          {% endif %}
          {% if  item.video_specification_linker %}
          {% for item in item.video_specification_linker %}
          related video :
            {{ item }} ,
          {% endfor %}
          {% endif %}



  {% if item.8 and item.9 %}

<p class="card-text "title="{{ item.i }}">{{ item.0|highlightpredefined:item.8|highlightuser:item.9}}</p><br />
<p class="card-text" style="position:absolute;right:3px;bottom:5px;"><small class="text-muted">Last updated {{ item.4 }}</small></p>
<table style="position:absolute;right:3px;top:5px;">
{% if item.8 %}
{% for tag,repeat in item.6 %}
<thead>
<tr>
<td><span class="badge badge-pill badge-success" >{{tag}}</span> </td>
<td scope="row">{{repeat }} times</td>
</tr>

</thead>
{% endfor %}
{% endif %}
{% if item.9 %}
{% for tag,repeat in item.7 %}
<thead>
<tr>
<td><span class="badge badge-pill badge-secondary" >{{tag}}</span> </td>
<td scope="row">{{repeat }} times</td>
</tr>

</thead>
{% endfor %}
{% endif %}
</table>
{% elif item.8 %}

<p class="card-text " title="{{ item.i }}">{{ item.0|highlightpredefined:item.8}}</p><br />
<p class="card-text" style="position:absolute;right:3px;bottom:5px;"><small class="text-muted">Last updated {{ item.4 }}</small></p>
<table style="position:absolute;right:3px;top:5px;">
{% for tag,repeat in item.6 %}
<thead>
<tr>
<td><span class="badge badge-pill badge-success" >{{tag}}</span> </td>
<td scope="row">{{repeat }} times</td>
</tr>

</thead>
{% endfor %}
</table>

{%elif item.9 %}

<p class="card-text "title="{{ item.i }}">{{ item.0|highlightuser:item.9}}</p><br />
<p class="card-text" style="position:absolute;right:3px;bottom:5px;"><small class="text-muted">Last updated {{ item.4 }}</small></p>
<table style="position:absolute;right:3px;top:5px;">
{% for tag,repeat in item.7 %}
<thead>
<tr>
<td><span class="badge badge-pill badge-secondary" >{{tag}}</span> </td>
<td scope="row">{{repeat }} times</td>
</tr>

</thead>
{% endfor %}
</table>
{% else %}
<p class="card-text "title="{{ item.i }}">{{ item.0|slice:"0:50"}}</p><br />
<p class="card-text"style="position:absolute;right:3px;bottom:5px;" ><small class="text-muted">Last updated {{ item.4 }}</small></p>
{% endif %}

</div>
</div>
</div>
</div>
{% endfor %}
