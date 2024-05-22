insert into {{ schema }}.{% if is_forecast %}forecast{% else %}historical{% endif %}_games (
    {% for column in columns %}
        {{ column.name }}{% if not loop.last %},{% endif %}
    {% endfor %}
)
values
{% for i, row in df.iterrows() %}
(
   {% for column in columns %}
        {% if column.null_default %}
            {% if row[column.name] == 'NULL' %}
                NULL{% if not loop.last %},{% endif %}
            {% else %}
                '{{ row[column.name] | safe }}'::{{ column.type }}{% if not loop.last %},{% endif %}
            {% endif %}
        {% else %}
            '{{ row[column.name] | safe }}'::{{ column.type }}{% if not loop.last %},{% endif %}
        {% endif %}
   {% endfor %}
)
{% if not loop.last %},{% endif %}
{% endfor %};