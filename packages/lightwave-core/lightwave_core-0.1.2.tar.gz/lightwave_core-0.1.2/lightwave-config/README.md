# Lightwave YAML Configuration Standard

This document outlines the YAML configuration standard for the Lightwave ecosystem. YAML has been chosen as the standard configuration format for all Lightwave projects due to its readability, structure, and wide support across programming languages.

## Configuration File Structure

All Lightwave configuration files should follow this structure:

```yaml
# Title or description of the configuration
version: "1.0.0"
description: "Detailed description of what this configuration is for"
updated: "YYYY-MM-DD"
module: "module_name"  # e.g., cli, rules, sprint

# Main configuration sections follow
main_section:
  # Configuration content
  key: value
  nested_section:
    - item1
    - item2
```

## Naming Convention

Configuration files should be named according to this pattern:

```txt
lightwave-{module}-{purpose}.yaml
```

Examples:

- `lightwave-cli-config.yaml`
- `lightwave-rules-core.yaml`
- `lightwave-sprint-settings.yaml`

## Converting Existing Files

A conversion script is provided to help migrate existing configuration files to the YAML standard:

```bash
# Convert a single file
./scripts/convert_to_yaml.py --file lightwave-config/lightwave-cli-uv.json --output lightwave-config/lightwave-cli-config.yaml

# Convert all files in a directory
./scripts/convert_to_yaml.py --directory lightwave-config

# Show what would be converted without actually converting
./scripts/convert_to_yaml.py --directory lightwave-config --dry-run

# Add module metadata during conversion
./scripts/convert_to_yaml.py --file lightwave-config/some-file.txt --module sprint
```

## Standard Patterns for Different Types of Configurations

### Rules Configuration

Rules configurations should follow this structure:

```yaml
version: "1.0.0"
description: "Lightwave Rules Configuration"
updated: "YYYY-MM-DD"
module: "rules"

sections:
  - name: "RULE_NAME"
    description: "Description of rule purpose"
    globs: "**/*.ext"
    always_apply: true
    content:
      - heading: "Main Points in Bold"
        items:
          - "Sub-points with details"
          - "Examples and explanations"
        code: |
          // Example code block
          const example = true;
```

### CLI Configuration

CLI configurations should follow this structure:

```yaml
version: "1.0.0"
description: "Lightwave CLI Configuration"
updated: "YYYY-MM-DD"
module: "cli"

commands:
  command_name:
    description: "Command description"
    syntax: "Usage example"
    parameters:
      - name: "param_name"
        description: "Parameter description"
        required: true
        default: "default_value"
    examples:
      - "lightwave command_name --param=value"
```

### Sprint Context Configuration

Sprint context configurations should follow this structure:

```yaml
version: "1.0.0"
description: "Sprint context for Project X"
updated: "YYYY-MM-DD"
module: "sprint"

sprint:
  name: "sprint-name"
  description: "Sprint description"
  
  workflow:
    steps:
      - name: "Step name"
        description: "Step description"
        # Step-specific details
```

## Best Practices

1. **Use Snake Case for Keys**: All keys should use snake_case (e.g., `command_name` not `commandName`).

2. **Include Version Information**: Always include version information to track configuration changes.

3. **Document Your Configuration**: Add comments to explain complex configurations.

4. **Keep It Modular**: Split large configurations into logical modules.

5. **Validate Your YAML**: Use tools like yamllint to ensure your YAML is valid.

6. **Use Native YAML Types**: Use YAML's native types (lists, maps, strings, numbers, booleans) appropriately.

## Tools and Libraries

- **Python**: Use PyYAML for parsing YAML files
- **JavaScript/Node.js**: Use js-yaml for parsing YAML files
- **Validation**: Consider using JSON Schema with a YAML parser to validate your configuration files

## Additional Resources

- [YAML Official Specification](https://yaml.org/spec/1.2.2/)
- [Online YAML Validator](https://www.yamllint.com/)
- [YAML Best Practices](https://squarespace.engineering/yaml-best-practices.html)
