insert into {{ schema }}.historical_games (
    {% for column in columns %}
        {{ column.name }}{% if not loop.last %},{% endif %}
    {% endfor %}
)
values
{% for i, row in df.iterrows() %}
(
   {% for column in columns %}
   '{{ row[column.name] | safe }}'::{{ column.type }}{% if not loop.last %},{% endif %}
   {% endfor %}
)
{% if not loop.last %},{% endif %}
{% endfor %};