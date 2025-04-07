{% macro get_imported_databases() %}
    {%- set query %}
        SELECT database_name
        FROM snowflake.account_usage.databases
        WHERE type = 'IMPORTED DATABASE'
        AND database_owner IS NOT NULL
        AND deleted is null
    {%- endset %}

    {%- set results = run_query(query) -%}
    {%- if execute %}
        {%- set all_databases = results.rows | map(attribute=0) | list %}
        {{ log("Extracted Databases: " ~ all_databases, info=True) }}
    {{ return(all_databases) }}
    {%- else %}
    {%- set all_databases = [] %}
    {%- endif %}

    {{ return(all_databases) }}
{% endmacro %}
