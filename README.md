Problem:

Often, the same columns exist in multiple layers (e.g., order_id, order_date are in staging, intermediate, and mart). These columns mean the same thing across layers, so their descriptions should also be identical.

Every time that a new model is build, you are manually copying descriptions from the previous layer

Tedious, we are manually coping many columns
Error-Prone, there could be many manual mistakes
Time-Consuming, As your project grows, the documentation could become a bottleneck

The reason that DBT can’t handle this is because it does not handle metadata, it is just a transform tool so we can get ready for the business application. Each YAML file is different so something in mart does not know about something in intermediate

Avoid manually copying column descriptions across multiple dbt models that share the same columns (e.g., staging models and marts). We need a tool to automatically copy the descriptions from a source model to a target model.

Solutions:
If a model is built on top of another model (upstream/downstream relationship) and it uses the same column (same data, same meaning), then that column should have:
The same name (column name should not change).
The same description (column meaning should not change).

Dbt power user extension does 2 things well	
Autocompleting model/column names.
Showing documentation previews
It DOES NOT auto generate/copy descriptions from one model to another
Python Script
When a new model is built (with overlapping columns), it should inherit descriptions automatically.
