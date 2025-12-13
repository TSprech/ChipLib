---
sidebar_position: 7
---

# Best Practices

1.  **Naming:** Use **Title Case** for `name` fields (e.g., "Conversion Rate"). Use **UPPER\_CASE** for `symbol` fields representing registers or enums.
2.  **Binary Literals:** Use binary (`0b...`) for enum values and bitmasks to make the specific bit settings obvious.
3.  **Documentation:** Use the `description` fields liberally. This text is propagated to the generated code (e.g., Doxygen comments) and is vital for the end-user.
4.  **Resets:** Always verify that the `reset` value of a register matches the sum of its fields' defaults in the datasheet.
