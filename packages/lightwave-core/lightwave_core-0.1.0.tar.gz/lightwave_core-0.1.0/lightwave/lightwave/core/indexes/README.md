# LightWave Ecosystem Index Files

This directory contains structured index files that serve as the single source of truth for various aspects of the LightWave ecosystem. These files are provided in multiple formats (Markdown, YAML, and JSON) to support both human readability and machine processing.

## Available Indices

| Index Name | Description | Formats |
|------------|-------------|---------|
| [api-endpoints-index](api-endpoints-index.md) | Complete API endpoint reference across all LightWave services | [MD](api-endpoints-index.md), [YAML](api-endpoints-index.yaml), [JSON](api-endpoints-index.json) |
| [component-registry](component-registry.md) | Registry of all UI components in the LightWave Design System | [MD](component-registry.md), [YAML](component-registry.yaml), [JSON](component-registry.json) |
| [dependency-graph](dependency-graph.md) | Dependencies between LightWave repositories and build order | [MD](dependency-graph.md), [YAML](dependency-graph.yaml), [JSON](dependency-graph.json) |
| [email-index](email-index.md) | Standardized email addresses and communication channels | [MD](email-index.md), [YAML](email-index.yaml), [JSON](email-index.json) |
| [filesystem-conventions](filesystem-conventions.md) | Standardized project structures and filesystem conventions | [MD](filesystem-conventions.md), [YAML](filesystem-conventions.yaml), [JSON](filesystem-conventions.json) |
| [schema-registry](schema-registry.md) | Standardized data schemas for all objects in the ecosystem | [MD](schema-registry.md), [YAML](schema-registry.yaml), [JSON](schema-registry.json) |
| [url-index](url-index.md) | URL structures and naming conventions across all platforms | [MD](url-index.md), [YAML](url-index.yaml), [JSON](url-index.json) |

## Combined Index

A [combined-index.json](combined-index.json) file is also provided that references all individual indices, making it easier to programmatically discover and access the complete set of indices.

## Using These Indices

### For Humans

The Markdown (`.md`) files are designed for human readability and are best viewed directly in GitHub or any Markdown viewer. They provide comprehensive documentation with proper formatting, tables, and code examples.

### For Machines

The YAML (`.yaml`) and JSON (`.json`) files are designed for machine readability and can be used in various ways:

1. **API Documentation Tools**: Use the `api-endpoints-index.json` to generate API documentation or client libraries.
2. **Design Systems**: Use the `component-registry.json` for your design system tooling.
3. **CI/CD Pipelines**: Use the `dependency-graph.json` to determine build order and dependencies.
4. **Project Scaffolding**: Use the `filesystem-conventions.json` when generating new projects.
5. **Data Validation**: Use the `schema-registry.json` for validating data structures and generating type definitions.
6. **URL Management**: Use the `url-index.json` for routing, endpoint validation, or documentation generation.
7. **Email Configuration**: Use the `email-index.json` for setting up email addresses and managing communication channels.

## Updating the Indices

The indices are maintained in Markdown format and converted to YAML and JSON using scripts in the `scripts/` directory:

```bash
# Generate YAML files from Markdown
/path/to/scripts/generate_yaml_indexes.py

# Generate JSON files from YAML
/path/to/scripts/generate_json_indexes.py
```

Always update the Markdown files first, then generate the derived formats.

## Implementation Guidelines

1. **Single Source of Truth**: These indices should be considered the canonical reference for their respective domains.
2. **Consistency**: All systems, tools, and documentation should refer to these indices for standardization.
3. **Versioning**: The indices evolve with the ecosystem; refer to the file history for changes over time.
4. **Validation**: Use the structured formats (YAML/JSON) for validation where appropriate.

## Scripts

The following scripts are available in the `scripts/` directory for working with these indices:

- `generate_yaml_indexes.py`: Converts Markdown indices to YAML forma
- `generate_json_indexes.py`: Converts YAML indices to JSON format and creates the combined index

## Related Documentation

- [Documentation Strategy](../documentation-single-source-of-truth.md)
- [LightWave Project Starter](../lightwave-project-starter/project-starter-guide.md)
- [API Gateway Documentation](../lightwave-api-gateway/overview.md)