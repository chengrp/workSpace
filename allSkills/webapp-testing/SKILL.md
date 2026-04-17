---
name: webapp-testing
description: Guide for testing web applications with Claude Code. Provides workflows and best practices for testing web apps, including UI testing, API testing, and end-to-end testing.
license: MIT
---

# Web Application Testing Skill

This skill provides guidance for testing web applications using Claude Code and related tools.

## Overview

Web application testing involves verifying that web applications function correctly across different scenarios, browsers, and user interactions. This skill covers both manual and automated testing approaches.

## Testing Workflows

### 1. Manual Testing Workflow

**When to use**: Initial testing, exploratory testing, or when automation is not feasible.

**Steps**:
1. **Environment Setup**
   - Verify browser compatibility (Chrome, Firefox, Safari, Edge)
   - Check responsive design (mobile, tablet, desktop)
   - Test with different screen resolutions

2. **Functional Testing**
   - Test all user flows (registration, login, core features)
   - Validate form submissions and error handling
   - Test navigation and routing
   - Verify data persistence (localStorage, cookies, sessions)

3. **UI/UX Testing**
   - Check visual consistency and alignment
   - Test accessibility (keyboard navigation, screen readers)
   - Verify loading states and transitions
   - Test hover and focus states

### 2. Automated Testing Workflow

**When to use**: Regression testing, continuous integration, or repetitive test scenarios.

**Tools and Approaches**:
- **Playwright**: Cross-browser testing with automation
- **Cypress**: End-to-end testing framework
- **Jest**: Unit and integration testing
- **Selenium**: Browser automation (legacy)

### 3. API Testing Workflow

**When to use**: Testing backend services, REST APIs, or GraphQL endpoints.

**Steps**:
1. **Endpoint Validation**
   - Test all HTTP methods (GET, POST, PUT, DELETE, PATCH)
   - Validate request/response formats
   - Test authentication and authorization

2. **Data Validation**
   - Test with valid and invalid data
   - Verify error responses and status codes
   - Test edge cases and boundary conditions

3. **Performance Testing**
   - Measure response times
   - Test concurrent requests
   - Validate rate limiting

## Tool Integration

### Playwright Integration

```bash
# Install Playwright
npm init playwright@latest

# Run tests
npx playwright test

# Generate tests
npx playwright codegen http://localhost:3000
```

### Cypress Integration

```bash
# Install Cypress
npm install cypress --save-dev

# Open Cypress
npx cypress open

# Run tests headlessly
npx cypress run
```

### API Testing with curl

```bash
# Basic GET request
curl -X GET http://localhost:3000/api/users

# POST request with JSON
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com"}'

# With authentication
curl -X GET http://localhost:3000/api/protected \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Testing Strategies

### 1. Test Pyramid
- **Unit Tests** (70%): Test individual components/functions
- **Integration Tests** (20%): Test component interactions
- **End-to-End Tests** (10%): Test complete user flows

### 2. Test Data Management
- Use fixtures for consistent test data
- Implement test data cleanup
- Consider using test databases

### 3. Cross-Browser Testing
- Test on latest versions of major browsers
- Consider browser-specific quirks
- Test on mobile browsers

## Common Testing Scenarios

### Form Testing
```javascript
// Example: Form validation testing
1. Test required fields
2. Test input validation (email, phone, etc.)
3. Test form submission success
4. Test error messages
5. Test form reset functionality
```

### Authentication Testing
```javascript
// Example: Login flow testing
1. Test valid login credentials
2. Test invalid login credentials
3. Test password reset flow
4. Test session management
5. Test logout functionality
```

### E-commerce Testing
```javascript
// Example: Shopping cart testing
1. Test adding/removing items
2. Test quantity updates
3. Test price calculations
4. Test checkout process
5. Test payment integration
```

## Best Practices

### 1. Test Organization
- Group tests by feature or component
- Use descriptive test names
- Maintain test independence

### 2. Test Maintenance
- Update tests when features change
- Remove obsolete tests
- Monitor test flakiness

### 3. Performance Considerations
- Keep tests fast and efficient
- Use mocks for external services
- Implement parallel test execution

## Debugging Tips

### 1. Console Debugging
```javascript
// Use browser developer tools
console.log('Debug info:', data);
console.table(dataArray);
console.time('operation');
// ... code ...
console.timeEnd('operation');
```

### 2. Network Debugging
- Monitor network requests in DevTools
- Check response status codes
- Validate response data format

### 3. Visual Debugging
- Use browser extensions for CSS debugging
- Take screenshots for visual regression
- Use accessibility testing tools

## Resources

### Documentation
- [Playwright Documentation](https://playwright.dev/docs/intro)
- [Cypress Documentation](https://docs.cypress.io/)
- [Jest Documentation](https://jestjs.io/docs/getting-started)

### Testing Libraries
- [Testing Library](https://testing-library.com/) - DOM testing utilities
- [Mock Service Worker](https://mswjs.io/) - API mocking
- [Faker.js](https://fakerjs.dev/) - Test data generation

### Tools
- [BrowserStack](https://www.browserstack.com/) - Cross-browser testing
- [Lighthouse](https://developers.google.com/web/tools/lighthouse) - Performance auditing
- [axe-core](https://github.com/dequelabs/axe-core) - Accessibility testing