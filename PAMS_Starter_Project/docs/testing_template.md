# Testing Evidence Template

## Manual Test Cases

| Test Case ID | Description | Input | Expected Output | Actual Output | Result |
|---|---|---|---|---|---|
| TC01 | Add new tenant | Valid tenant details | Tenant added successfully | As expected | Pass |
| TC02 | Reject invalid email | Email without @ | Validation error | As expected | Pass |
| TC03 | Add apartment | Valid apartment data | Apartment created | As expected | Pass |
| TC04 | Record payment | Valid pending payment | Payment marked as paid and receipt generated | As expected | Pass |
| TC05 | Late payment detection | Overdue unpaid invoice | Invoice shown in late list | As expected | Pass |
| TC06 | Create maintenance request | Valid issue data | Request logged | As expected | Pass |
| TC07 | Reject negative maintenance cost | Cost = -5 | Validation error | As expected | Pass |
| TC08 | Role restriction | Front desk opens finance area | Access denied or hidden menu | As expected | Pass |

## Automated Tests
Run:
```bash
python -m unittest discover -s tests
```

Include screenshots of:
- passing test cases
- invalid input handling
- key GUI screens
- example reports
