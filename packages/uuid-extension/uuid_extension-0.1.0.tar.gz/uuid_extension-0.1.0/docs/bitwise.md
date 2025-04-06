# Understanding Bitwise Operations in Python

This guide explains bitwise operations with a focus on the expression `(uuid_int >> 80) & 0xFFFFFFFFFFFF`. We'll break down each operation, provide examples with visualization, and explore practical applications.

## Table of Contents
1. [Basic Concepts](#basic-concepts)
2. [Bitwise Operators](#bitwise-operators)
3. [Breaking Down Our Example](#breaking-down-our-example)
4. [Step-by-Step Execution](#step-by-step-execution)
5. [Common Use Cases](#common-use-cases)

## Basic Concepts

### Bits and Binary

A bit is the most basic unit of information in computing, representing either 0 or 1. Multiple bits form binary numbers:

```
Decimal: 13
Binary:  00001101
         ↑↑↑↑↑↑↑↑
         87654321 (bit positions)
```

### Hexadecimal Notation

Hexadecimal (base 16) uses 0-9 and A-F to represent 16 values:

```
Decimal:     0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
Hexadecimal: 0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F
```

Example: `0xFF` = 255 decimal = `11111111` binary

## Bitwise Operators

### Bitwise AND (`&`)

Compares each bit position; results in 1 only if both bits are 1.

```
    1101 (13)
  & 1010 (10)
    ----
    1000 (8)
```

Example:
```python
a = 13  # 1101 in binary
b = 10  # 1010 in binary
result = a & b
print(f"{a} & {b} = {result}")  # Output: 13 & 10 = 8
```

### Bitwise OR (`|`)

Compares each bit position; results in 1 if either bit is 1.

```
    1101 (13)
  | 1010 (10)
    ----
    1111 (15)
```

Example:
```python
a = 13  # 1101 in binary
b = 10  # 1010 in binary
result = a | b
print(f"{a} | {b} = {result}")  # Output: 13 | 10 = 15
```

### Bitwise XOR (`^`)

Compares each bit position; results in 1 only if exactly one bit is 1.

```
    1101 (13)
  ^ 1010 (10)
    ----
    0111 (7)
```

Example:
```python
a = 13  # 1101 in binary
b = 10  # 1010 in binary
result = a ^ b
print(f"{a} ^ {b} = {result}")  # Output: 13 ^ 10 = 7
```

### Bitwise NOT (`~`)

Inverts all bits (0 becomes 1, 1 becomes 0).

```
  ~ 1101 (13)
    ----
    0010 (-14 in two's complement)
```

Example:
```python
a = 13  # 1101 in binary
result = ~a
print(f"~{a} = {result}")  # Output: ~13 = -14
```

Note: In Python, NOT operates using two's complement, so ~n = -n-1

### Bitwise Left Shift (`<<`)

Shifts bits to the left by a specified number of positions, filling with 0s on the right.

```
13 << 2:
Before: 00001101 (13)
After:  00110100 (52)
```

Example:
```python
a = 13
shift = 2
result = a << shift
print(f"{a} << {shift} = {result}")  # Output: 13 << 2 = 52
```

### Bitwise Right Shift (`>>`)

Shifts bits to the right by a specified number of positions.

```
13 >> 2:
Before: 00001101 (13)
After:  00000011 (3)
```

Example:
```python
a = 13
shift = 2
result = a >> shift
print(f"{a} >> {shift} = {result}")  # Output: 13 >> 2 = 3
```

## Breaking Down Our Example

Let's analyze: `(uuid_int >> 80) & 0xFFFFFFFFFFFF`

This expression:
1. Takes a UUID integer value
2. Shifts it right by 80 bits
3. Performs a bitwise AND with `0xFFFFFFFFFFFF` (a 48-bit mask with all 1s)

## Step-by-Step Execution

### Example with a Sample UUID

Let's work with UUID: `123e4567-e89b-12d3-a456-426614174000`

As an integer: `0x123e4567e89b12d3a456426614174000`

#### Step 1: Understanding the Structure

This UUID integer in binary is 128 bits long:

```
UUID Integer:
0001 0010 0011 1110 0100 0101 0110 0111 1110 1000 1001 1011 0001 0010 1101 0011 1010 0100 0101 0110 0100 0010 0110 0110 0001 0100 0001 0111 0100 0000 0000 0000
```

#### Step 2: Right Shift by 80

`uuid_int >> 80` shifts all bits 80 positions to the right:

```
Before shift (simplified view of most significant bits):
0001 0010 0011 1110 0100 0101 0110 0111 1110 1000 1001 1011 0001 0010 1101 0011...

After shift (80 bits from right removed):
...0000 0000 0001 0010 0011 1110 0100 0101 0110 0111 1110 1000 1001 1011 0001 0010
```

Result: `0x123e4567e89b`

#### Step 3: Bitwise AND with Mask

The mask `0xFFFFFFFFFFFF` is 48 bits of all 1s:

```
Shifted value: 0000 0000 0001 0010 0011 1110 0100 0101 0110 0111 1110 1000 1001 1011 0001 0010
Mask:          0000 0000 1111 1111 1111 1111 1111 1111 1111 1111 1111 1111 1111 1111 1111 1111
Result:        0000 0000 0001 0010 0011 1110 0100 0101 0110 0111 1110 1000 1001 1011 0001 0010
```

The mask preserves the 48 least significant bits of the shifted value.

Final result: `0x123e4567e89b`

### Understanding Bit Shifting in Depth

Bit shifting is a fundamental operation that moves bits left or right within a binary representation:

#### Right Shift (`>>`)
- **Definition**: Moves all bits to the right by the specified number of positions
- **Effect**: Divides the number by 2^n (where n is the shift amount)
- **Lost Information**: Bits shifted beyond the right edge are discarded
- **Padding**: Most significant bits are filled with 0s (logical shift) or the sign bit (arithmetic shift)

**Visual Example**:
```
Decimal 173 (10101101 in binary) right-shifted by 3:
Before: 10101101
After:  00010101 (equals decimal 21)
        ↑↑↑ ← New 0s inserted on the left
```

Right shift by 80 bits effectively divides the uuid_int by 2^80, extracting only the higher bit positions.

### Masking Operations Explained

Bit masking uses bitwise AND to selectively filter bits:

#### Bitwise AND Mask
- **Purpose**: Keeps only the bits you want, zeros out the rest
- **Creation**: Set 1s in positions to keep, 0s in positions to clear
- **Formula**: `result = value & mask`
- **Common Masks**:
  - `0xFF`: Preserve only the lowest 8 bits
  - `0xFFFFFFFFFFFF`: Preserve 48 bits (as in our example)
  - `0x01`: Check if the least significant bit is set

**Mask Patterns**:
```
Keep lower 4 bits:   0000 1111 (0x0F)
Keep upper 4 bits:   1111 0000 (0xF0)
Keep specific bits:  0101 0101 (0x55)
```

### Why Use `0xFFFFFFFFFFFF` in Our Example?

The 48-bit mask (`0xFFFFFFFFFFFF`) serves a specific purpose:

1. **Size Limitation**: Ensures the result doesn't exceed 48 bits (6 bytes)
2. **Data Integrity**: Removes any potential higher bits that might exist after the shift
3. **Standardization**: Forces the result into a consistent bit-length format
4. **UUID Structure**: Targets specific segments of the UUID structure

This technique combines shifting and masking to precisely extract 48 bits from a specific position in the 128-bit UUID.

### Code Demonstration:

```python
# Example with the UUID: 123e4567-e89b-12d3-a456-426614174000
uuid_int = 0x123e4567e89b12d3a456426614174000
print(f"Original UUID integer: {uuid_int}")
print(f"Hexadecimal: 0x{uuid_int:032x}")

# Step 1: Right shift by 80
shifted = uuid_int >> 80
print(f"\nAfter shifting right by 80 bits: {shifted}")
print(f"Hexadecimal: 0x{shifted:x}")

# Step 2: Apply the mask with bitwise AND
mask = 0xFFFFFFFFFFFF
result = shifted & mask
print(f"\nMask: 0x{mask:x}")
print(f"After applying the mask: {result}")
print(f"Hexadecimal: 0x{result:x}")
```

Output:
```
Original UUID integer: 24197857161011715162171839636988778528768
Hexadecimal: 0x123e4567e89b12d3a456426614174000

After shifting right by 80 bits: 81985529216411
Hexadecimal: 0x123e4567e89b

Mask: 0xffffffffffff
After applying the mask: 81985529216411
Hexadecimal: 0x123e4567e89b
```

## Common Use Cases

1. **Extracting Fields from UUIDs**: As in our example, isolating specific bit fields
   - Example: Getting timestamp components from time-based UUIDs
   - Example: Extracting node identifiers from MAC address-based UUIDs

2. **Mask Operations**: Selectively preserving or clearing bits
   - Clearing specific flags: `status &= ~FLAG_BITS`
   - Setting specific flags: `status |= FLAG_BITS`
   - Toggling specific flags: `status ^= FLAG_BITS`
   - Checking if flags are set: `if (status & FLAG_BITS) == FLAG_BITS`

3. **Efficient Division/Multiplication**: Using shifts for powers of 2
4. **Flag Manipulation**: Setting, checking, and clearing flags in a single integer
5. **Low-Level Memory Operations**: Direct manipulation of memory contents

## Role-Based Access Control Example

Bitwise operations provide an elegant way to implement role-based access control systems. Here's a practical example demonstrating how to define, assign, and check user roles:

### Defining Roles Using Bit Flags

Each role is assigned a power of 2 so each bit position represents a distinct role:

```python
# Role definitions (each role is a distinct bit)
NOT_LOGGED_IN = 0       # 00000000
USER = 1                # 00000001
EDITOR = 2              # 00000010
ADMIN = 4               # 00000100
SUPER_ADMIN = 8         # 00001000
```

### Assigning Multiple Roles

Combining roles is achieved with the bitwise OR (`|`) operator:

```python
# User with multiple roles (both USER and EDITOR permissions)
user_roles = USER | EDITOR  # 00000011 (decimal 3)

# Admin with all permissions
admin_roles = USER | EDITOR | ADMIN | SUPER_ADMIN  # 00001111 (decimal 15)
```

### Checking for Roles

Testing for specific roles uses the bitwise AND (`&`) operator:

```python
def has_role(user_roles, role):
    """Check if the user has a specific role."""
    return (user_roles & role) == role

def check_access(user_roles):
    """Demonstrate role checking."""
    if user_roles == NOT_LOGGED_IN:
        print("Not logged in - access denied")
    elif has_role(user_roles, ADMIN):
        print("Admin access granted - full control")
    elif has_role(user_roles, EDITOR):
        print("Editor access granted - can edit content")
    elif has_role(user_roles, USER):
        print("User access granted - can view content")
    else:
        print("Unknown role configuration")

# Example usage
regular_user = USER                 # Just a regular user
content_editor = USER | EDITOR      # User with editor privileges
site_admin = USER | EDITOR | ADMIN  # User with admin privileges

check_access(regular_user)    # Output: User access granted - can view content
check_access(content_editor)  # Output: Editor access granted - can edit content
check_access(site_admin)      # Output: Admin access granted - full control
```

### Adding and Removing Roles

Dynamically modify permissions without affecting other roles:

```python
# Granting a role (using bitwise OR)
def grant_role(user_roles, role):
    return user_roles | role

# Revoking a role (using bitwise AND with complement)
def revoke_role(user_roles, role):
    return user_roles & ~role

# Example: Promote a regular user to editor
user_roles = USER
print(f"Initial roles: {user_roles:08b}")        # 00000001

user_roles = grant_role(user_roles, EDITOR)
print(f"After promotion: {user_roles:08b}")      # 00000011

# Example: Revoke editor role
user_roles = revoke_role(user_roles, EDITOR)
print(f"After demotion: {user_roles:08b}")       # 00000001
```

### Benefits of Bitwise Role Management

1. **Storage Efficiency**: Represents multiple roles in a single integer
2. **Performance**: Role checking is a simple bitwise operation
3. **Flexibility**: Easily add or remove roles without affecting others
4. **Scalability**: Supports up to 32 or 64 distinct roles (depending on integer size)
5. **Compatibility**: Works well with database storage and API transmission

This pattern is commonly used in:
- Operating system permission systems (read, write, execute)
- Web application authorization frameworks
- Database access control mechanisms
- Game development (character attributes, status effects)