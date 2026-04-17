---
name: n8n-skills
description: Guide for working with n8n workflow automation platform. This skill should be used when users need to create, manage, or troubleshoot n8n workflows, nodes, and automation tasks.
license: MIT
---

# n8n Skills Guide

This skill provides guidance for working with n8n workflow automation platform.

## About n8n

n8n is an open-source workflow automation tool that allows you to connect different apps and services to automate tasks. It uses a visual workflow editor with nodes representing different operations.

## Core Concepts

### Workflows
- **Workflow**: A sequence of nodes that process data
- **Node**: A single operation in a workflow (trigger, action, or logic)
- **Connection**: Link between nodes that passes data
- **Trigger**: Starting point of a workflow (webhook, schedule, etc.)
- **Action**: Operations that process data (HTTP request, database query, etc.)

### Common Node Types
1. **Trigger Nodes**: Webhook, Schedule, Manual Trigger
2. **Action Nodes**: HTTP Request, Database, Email, File Operations
3. **Logic Nodes**: If, Switch, Merge, Wait
4. **Data Transformation**: Set, Function, Spreadsheet File

## Basic Workflow Creation

### 1. Setting up a simple workflow
```
1. Add a Trigger node (e.g., Manual Trigger)
2. Add an Action node (e.g., HTTP Request)
3. Connect the nodes
4. Configure node parameters
5. Test the workflow
```

### 2. Common patterns
- **API Integration**: Manual Trigger → HTTP Request → Set (data transformation)
- **Scheduled Tasks**: Schedule Trigger → Database Query → Email
- **Webhook Processing**: Webhook Trigger → Function (validation) → Database

## Advanced Features

### Error Handling
- Use "Error Trigger" node to catch errors
- Implement retry logic with "Wait" nodes
- Log errors to external services

### Data Transformation
- Use "Function" node for custom JavaScript/TypeScript
- Use "Set" node to modify data structure
- Use "Spreadsheet File" for CSV/Excel operations

### Best Practices
1. **Modular Design**: Break complex workflows into sub-workflows
2. **Error Handling**: Always include error handling nodes
3. **Documentation**: Add notes to explain complex logic
4. **Testing**: Test each node individually before connecting
5. **Version Control**: Export workflows as JSON for version control

## Troubleshooting

### Common Issues
1. **Authentication Errors**: Check credentials and API keys
2. **Data Format Issues**: Verify data structure between nodes
3. **Rate Limiting**: Implement delays for API calls
4. **Node Configuration**: Double-check all node settings

### Debugging Tips
- Use "Debug" mode to see data flow
- Check node execution logs
- Test with sample data
- Use "Function" node to log intermediate data

## Integration Examples

### Example 1: Slack Notification
```
Schedule Trigger (daily at 9 AM)
↓
HTTP Request (fetch data from API)
↓
Function (format message)
↓
Slack Node (send notification)
```

### Example 2: Data Backup
```
Schedule Trigger (weekly)
↓
Database Node (query data)
↓
Function (format as CSV)
↓
Google Drive Node (upload file)
```

## Resources
- [n8n Documentation](https://docs.n8n.io/)
- [n8n Community](https://community.n8n.io/)
- [Node Reference](https://docs.n8n.io/integrations/)
- [Workflow Examples](https://n8n.io/workflows/)