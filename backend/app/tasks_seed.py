"""
Validated C/C++ programming verification task set with known ground truth
and controlled annotations for Standard, Explanation-Based, and Verification-Guided interfaces.

Includes:
- VALIDATED_TASKS: 6 matched core tasks (Pair Groups A, B, C) for the main within-subjects study.
- SYSTEMS_COMPLEX_TASKS: 3 systems/kernel-flavored C++ tasks (including a 110-line SlabAllocator)
  for optional/separate evaluation without confounding the core 6-task study.
"""

VALIDATED_TASKS = [
    {
        "id": "task_max_value",
        "title": "Maximum Value in Vector",
        "difficulty": "Easy",
        "pair_group": "A",
        "task_set": "core",
        "problem_statement": (
            "Write a C++ function `int maxValue(const std::vector<int>& values)` that returns "
            "the largest integer in a non-empty vector `values`."
        ),
        "code": (
            "int maxValue(const std::vector<int>& values) {\n"
            "    int best = 0;\n"
            "    for (int x : values) {\n"
            "        if (x > best) {\n"
            "            best = x;\n"
            "        }\n"
            "    }\n"
            "    return best;\n"
            "}"
        ),
        "ground_truth_correct": False,
        "ground_truth_error_line": 2,
        "ground_truth_error_description": (
            "`best` is initialized to 0 instead of `values[0]` (or `INT_MIN`). "
            "If all elements in `values` are negative (e.g., {-5, -2, -9}), the function incorrectly returns 0."
        ),
        "ground_truth_test_case": "values = {-5, -2, -9} -> returns 0 instead of -2",
        "explanation_notes": [
            {
                "line": 2,
                "title": "Initialization",
                "text": "The starting candidate maximum `best` is initialized to 0 before scanning the vector.",
            },
            {
                "line": 3,
                "title": "Linear Scan",
                "text": "Iterates through every element `x` in `values` from start to end.",
            },
            {
                "line": 4,
                "title": "Comparison Update",
                "text": "Updates `best` whenever the current element `x` is strictly greater than `best`.",
            },
        ],
        "verification_guided": {
            "assumptions": [
                "Assumes `values` is non-empty.",
                "Assumes `best = 0` is a safe starting baseline for comparisons.",
            ],
            "suggested_edge_cases": [
                "All negative numbers: {-5, -2, -9}",
                "Single element vector: {-42}",
                "All zeros or mixed signs: {-3, 0, -1}",
            ],
            "attention_lines": [2, 4],
            "checklist": [
                "Check the initial value of the accumulator/best variable.",
                "Trace the loop with strictly negative inputs.",
                "Verify behavior on a single-element vector.",
            ],
            "expandable_hints": [
                {
                    "line": 2,
                    "label": "Inspect initialization of `best`",
                    "detail": "When `best` starts at 0, any element smaller than 0 will fail `x > best`.",
                },
                {
                    "line": 4,
                    "label": "Trace update condition",
                    "detail": "If `x > best` is never true during the loop, the initial value is returned unchanged.",
                },
            ],
        },
    },
    {
        "id": "task_binary_search",
        "title": "Binary Search Index",
        "difficulty": "Medium",
        "pair_group": "A",
        "task_set": "core",
        "problem_statement": (
            "Write a C++ function `int binarySearch(const std::vector<int>& arr, int target)` that returns "
            "the 0-based index of `target` in a sorted ascending vector `arr`, or `-1` if not found."
        ),
        "code": (
            "int binarySearch(const std::vector<int>& arr, int target) {\n"
            "    int left = 0;\n"
            "    int right = static_cast<int>(arr.size()) - 1;\n"
            "    while (left <= right) {\n"
            "        int mid = left + (right - left) / 2;\n"
            "        if (arr[mid] == target) {\n"
            "            return mid;\n"
            "        } else if (arr[mid] < target) {\n"
            "            left = mid + 1;\n"
            "        } else {\n"
            "            right = mid - 1;\n"
            "        }\n"
            "    }\n"
            "    return -1;\n"
            "}"
        ),
        "ground_truth_correct": True,
        "ground_truth_error_line": None,
        "ground_truth_error_description": None,
        "ground_truth_test_case": None,
        "explanation_notes": [
            {
                "line": 3,
                "title": "Search Bounds",
                "text": "Sets inclusive bounds `[left, right]` covering `0` to `arr.size() - 1`.",
            },
            {
                "line": 5,
                "title": "Overflow-Safe Midpoint",
                "text": "Computes `mid` using `left + (right - left) / 2` to avoid signed integer overflow.",
            },
            {
                "line": 9,
                "title": "Boundary Narrowing",
                "text": "Moves `left` to `mid + 1` or `right` to `mid - 1` so the search space strictly shrinks each step.",
            },
        ],
        "verification_guided": {
            "assumptions": [
                "Assumes `arr` is sorted in ascending order.",
                "Uses inclusive bounds `[left, right]` with `while (left <= right)`.",
            ],
            "suggested_edge_cases": [
                "Empty vector: arr = {}, target = 5",
                "Target at first or last index: arr = {2, 4, 6}, target = 2 or 6",
                "Single-element vector: arr = {7}, target = 7 or 3",
            ],
            "attention_lines": [3, 4, 5],
            "checklist": [
                "Check if `arr.size() == 0` causes underflow or out-of-bounds access.",
                "Verify loop termination when `left == right`.",
                "Confirm `mid` calculation cannot overflow.",
            ],
            "expandable_hints": [
                {
                    "line": 3,
                    "label": "Check empty-vector cast",
                    "detail": "`static_cast<int>(0) - 1` produces `right = -1`, so `while (0 <= -1)` does not execute and returns `-1`.",
                },
                {
                    "line": 4,
                    "label": "Check single-element termination",
                    "detail": "When `left == right`, `mid == left`; either `arr[mid] == target` returns or bounds cross and exit.",
                },
            ],
        },
    },
    {
        "id": "task_palindrome",
        "title": "Case-Sensitive Palindrome Check",
        "difficulty": "Easy",
        "pair_group": "B",
        "task_set": "core",
        "problem_statement": (
            "Write a C++ function `bool isPalindrome(const std::string& s)` that returns `true` if `s` "
            "reads the same forwards and backwards (exact character match), and `false` otherwise."
        ),
        "code": (
            "bool isPalindrome(const std::string& s) {\n"
            "    int left = 0;\n"
            "    int right = static_cast<int>(s.length()) - 1;\n"
            "    while (left < right) {\n"
            "        if (s[left] != s[right]) {\n"
            "            return false;\n"
            "        }\n"
            "        left++;\n"
            "        right--;\n"
            "    }\n"
            "    return true;\n"
            "}"
        ),
        "ground_truth_correct": True,
        "ground_truth_error_line": None,
        "ground_truth_error_description": None,
        "ground_truth_test_case": None,
        "explanation_notes": [
            {
                "line": 2,
                "title": "Two-Pointer Setup",
                "text": "Initializes `left` at the first character and `right` at the last character of `s`.",
            },
            {
                "line": 4,
                "title": "Symmetric Loop",
                "text": "Continues comparing pairs while `left < right`, stopping at or past the center.",
            },
            {
                "line": 5,
                "title": "Early Exit",
                "text": "Returns `false` immediately if any mirrored pair differs; otherwise returns `true`.",
            },
        ],
        "verification_guided": {
            "assumptions": [
                "Assumes exact character-by-character comparison (case-sensitive, includes spaces).",
                "Handles empty and 1-character strings as valid palindromes.",
            ],
            "suggested_edge_cases": [
                "Empty string: \"\"",
                "Single character: \"a\"",
                "Even-length palindrome vs mismatch: \"abba\", \"abca\"",
            ],
            "attention_lines": [3, 4],
            "checklist": [
                "Check behavior for empty string `\"\"`.",
                "Verify middle character handling on odd-length strings.",
                "Confirm pointers move inward on every iteration.",
            ],
            "expandable_hints": [
                {
                    "line": 3,
                    "label": "Inspect empty string bounds",
                    "detail": "For `\"\"`, `left = 0` and `right = -1`, so `while (0 < -1)` is skipped and `true` is returned.",
                },
            ],
        },
    },
    {
        "id": "task_average_positive",
        "title": "Average of Positive Numbers",
        "difficulty": "Easy",
        "pair_group": "B",
        "task_set": "core",
        "problem_statement": (
            "Write a C++ function `double averagePositive(const std::vector<int>& nums)` that returns "
            "the arithmetic mean of all strictly positive (`> 0`) numbers in `nums`, or `0.0` if none exist."
        ),
        "code": (
            "double averagePositive(const std::vector<int>& nums) {\n"
            "    int sum = 0;\n"
            "    int count = 0;\n"
            "    for (int n : nums) {\n"
            "        if (n > 0) {\n"
            "            sum += n;\n"
            "            count++;\n"
            "        }\n"
            "    }\n"
            "    if (count == 0) return 0.0;\n"
            "    return sum / count;\n"
            "}"
        ),
        "ground_truth_correct": False,
        "ground_truth_error_line": 11,
        "ground_truth_error_description": (
            "`sum / count` performs integer division because both `sum` and `count` are `int`. "
            "Fractional parts are truncated (e.g., `5 / 2` returns `2.0` instead of `2.5`)."
        ),
        "ground_truth_test_case": "nums = {2, 3} -> returns 2.0 instead of 2.5",
        "explanation_notes": [
            {
                "line": 2,
                "title": "Accumulators",
                "text": "Tracks `sum` and `count` as 32-bit integers for positive elements.",
            },
            {
                "line": 10,
                "title": "Zero-Count Guard",
                "text": "Prevents division by zero by returning `0.0` when no positive values are found.",
            },
            {
                "line": 11,
                "title": "Mean Computation",
                "text": "Divides `sum` by `count` to produce the `double` return value.",
            },
        ],
        "verification_guided": {
            "assumptions": [
                "Assumes `sum` fits within `int` range.",
                "Returns `0.0` when no elements are strictly greater than 0.",
            ],
            "suggested_edge_cases": [
                "Non-divisible sum: {2, 3} (expected 2.5)",
                "No positive numbers: {-4, 0, -1}",
                "Mixed negative, zero, and positive: {-2, 0, 1, 2}",
            ],
            "attention_lines": [2, 11],
            "checklist": [
                "Check data types used in the division expression.",
                "Verify zero-division protection when `count == 0`.",
                "Check whether `0` is excluded by `n > 0`.",
            ],
            "expandable_hints": [
                {
                    "line": 11,
                    "label": "Inspect division operator types",
                    "detail": "In C++, dividing an `int` by an `int` truncates toward zero before implicit conversion to `double`.",
                },
            ],
        },
    },
    {
        "id": "task_remove_duplicates",
        "title": "Count Unique Elements in Sorted Array",
        "difficulty": "Medium",
        "pair_group": "C",
        "task_set": "core",
        "problem_statement": (
            "Write a C++ function `int countUnique(const std::vector<int>& sortedNums)` that returns "
            "the number of distinct values in a sorted ascending vector `sortedNums`."
        ),
        "code": (
            "int countUnique(const std::vector<int>& sortedNums) {\n"
            "    if (sortedNums.empty()) return 0;\n"
            "    int uniqueCount = 1;\n"
            "    for (size_t i = 0; i < sortedNums.size() - 1; i++) {\n"
            "        if (sortedNums[i] != sortedNums[i + 1]) {\n"
            "            uniqueCount++;\n"
            "        }\n"
            "    }\n"
            "    return uniqueCount;\n"
            "}"
        ),
        "ground_truth_correct": True,
        "ground_truth_error_line": None,
        "ground_truth_error_description": None,
        "ground_truth_test_case": None,
        "explanation_notes": [
            {
                "line": 2,
                "title": "Empty Guard",
                "text": "Returns 0 early when `sortedNums` is empty, avoiding `size() - 1` unsigned underflow.",
            },
            {
                "line": 4,
                "title": "Adjacent Pair Scan",
                "text": "Compares each element `i` with `i + 1` up to the second-to-last element.",
            },
            {
                "line": 5,
                "title": "Transition Counting",
                "text": "Increments `uniqueCount` (starting at 1) each time adjacent values differ.",
            },
        ],
        "verification_guided": {
            "assumptions": [
                "Assumes `sortedNums` is already sorted so duplicates are adjacent.",
                "Guards `sortedNums.empty()` before subtracting 1 from `size_t`.",
            ],
            "suggested_edge_cases": [
                "Empty vector: {}",
                "Single element: {5}",
                "All identical elements: {3, 3, 3, 3}",
            ],
            "attention_lines": [2, 4, 5],
            "checklist": [
                "Verify `size_t` loop bound cannot underflow when size is 0 or 1.",
                "Check `sortedNums[i + 1]` stays within valid index range.",
                "Confirm initial `uniqueCount = 1` works for 1-element input.",
            ],
            "expandable_hints": [
                {
                    "line": 4,
                    "label": "Check single-element loop bound",
                    "detail": "For size 1, `sortedNums.size() - 1` is 0; `0 < 0` is false so the loop does not run and 1 is returned.",
                },
            ],
        },
    },
    {
        "id": "task_is_prime",
        "title": "Primality Test",
        "difficulty": "Medium",
        "pair_group": "C",
        "task_set": "core",
        "problem_statement": (
            "Write a C++ function `bool isPrime(int n)` that returns `true` if `n` is a prime number, "
            "and `false` otherwise."
        ),
        "code": (
            "bool isPrime(int n) {\n"
            "    if (n <= 1) return false;\n"
            "    for (int i = 2; i * i < n; i++) {\n"
            "        if (n % i == 0) {\n"
            "            return false;\n"
            "        }\n"
            "    }\n"
            "    return true;\n"
            "}"
        ),
        "ground_truth_correct": False,
        "ground_truth_error_line": 3,
        "ground_truth_error_description": (
            "The loop condition uses `i * i < n` instead of `i * i <= n`. "
            "Perfect squares of primes (e.g., 4, 9, 25, 49) skip checking their square root and are falsely reported as prime."
        ),
        "ground_truth_test_case": "n = 9 -> loop stops at i = 3 (3*3 < 9 is false), returns true instead of false",
        "explanation_notes": [
            {
                "line": 2,
                "title": "Base Case",
                "text": "Numbers less than or equal to 1 are not prime and immediately return `false`.",
            },
            {
                "line": 3,
                "title": "Square Root Bound",
                "text": "Tests candidate divisors `i` starting from 2 while `i * i < n`.",
            },
            {
                "line": 4,
                "title": "Divisibility Check",
                "text": "If `n` is divisible by `i`, returns `false`; otherwise returns `true` after the loop.",
            },
        ],
        "verification_guided": {
            "assumptions": [
                "Assumes `n` is a standard 32-bit `int` (no overflow on `i * i` for moderate `n`).",
                "Primes are integers strictly greater than 1.",
            ],
            "suggested_edge_cases": [
                "Small perfect square: n = 4 or n = 9",
                "Smallest prime: n = 2",
                "Negative or zero: n = -5, n = 0, n = 1",
            ],
            "attention_lines": [2, 3],
            "checklist": [
                "Check boundary condition of the loop (`<` vs `<=`).",
                "Test with perfect squares like 4, 9, and 25.",
                "Verify `n = 2` and `n <= 1`.",
            ],
            "expandable_hints": [
                {
                    "line": 3,
                    "label": "Trace `i * i < n` on a square",
                    "detail": "For `n = 9`, `i = 2` gives `9 % 2 != 0`, then `i = 3` fails `3 * 3 < 9`, exiting the loop.",
                },
            ],
        },
    },
]

# ==================== PHASE 2: SYSTEMS & 100+ LINE COMPLEX TASKS ====================

SYSTEMS_COMPLEX_TASKS = [
    {
        "id": "sys_ring_buffer",
        "title": "Systems: Bounded Ring Buffer (Circular Queue)",
        "difficulty": "Hard",
        "pair_group": "S",
        "task_set": "systems_challenge",
        "problem_statement": (
            "Implement a fixed-capacity C++ `RingBuffer` for a kernel/driver packet queue supporting "
            "`push`, `pop`, `isEmpty`, `isFull`, and `size` without dynamic allocations after construction."
        ),
        "code": (
            "#include <vector>\n"
            "#include <cstddef>\n"
            "\n"
            "class RingBuffer {\n"
            "public:\n"
            "    explicit RingBuffer(size_t capacity)\n"
            "        : buffer_(capacity), head_(0), tail_(0), count_(0) {}\n"
            "\n"
            "    bool isEmpty() const { return count_ == 0; }\n"
            "    bool isFull() const { return count_ == buffer_.size(); }\n"
            "    size_t size() const { return count_; }\n"
            "\n"
            "    bool push(int value) {\n"
            "        if (isFull() || buffer_.empty()) {\n"
            "            return false;\n"
            "        }\n"
            "        buffer_[tail_] = value;\n"
            "        tail_ = (tail_ + 1) % buffer_.size();\n"
            "        count_++;\n"
            "        return true;\n"
            "    }\n"
            "\n"
            "    bool pop(int& outValue) {\n"
            "        if (isEmpty()) {\n"
            "            return false;\n"
            "        }\n"
            "        outValue = buffer_[head_];\n"
            "        head_ = (head_ + 1) % buffer_.size();\n"
            "        count_--;\n"
            "        return true;\n"
            "    }\n"
            "\n"
            "private:\n"
            "    std::vector<int> buffer_;\n"
            "    size_t head_;\n"
            "    size_t tail_;\n"
            "    size_t count_;\n"
            "};"
        ),
        "ground_truth_correct": True,
        "ground_truth_error_line": None,
        "ground_truth_error_description": None,
        "ground_truth_test_case": None,
        "explanation_notes": [
            {
                "line": 10,
                "title": "Explicit Occupancy Counter",
                "text": "Tracks `count_` separately from `head_` and `tail_` so full vs. empty states are unambiguous.",
            },
            {
                "line": 14,
                "title": "Zero-Capacity & Full Guard",
                "text": "Rejects `push` if `isFull()` or `buffer_.empty()`, preventing modulo-by-zero on line 18.",
            },
            {
                "line": 28,
                "title": "Wrap-Around Indexing",
                "text": "Advances `head_` and `tail_` modulo `buffer_.size()` in FIFO order.",
            },
        ],
        "verification_guided": {
            "assumptions": [
                "Single-threaded caller (no internal mutex).",
                "Zero-capacity buffer (`capacity = 0`) must safely return `false` on push/pop.",
            ],
            "suggested_edge_cases": [
                "capacity = 0: push(10) -> must not divide by zero",
                "Wrap-around: push 3, pop 2, push 2 on capacity 3",
                "Pop on empty buffer -> returns false without modifying outValue",
            ],
            "attention_lines": [14, 18, 28],
            "checklist": [
                "Check for modulo-by-zero when `capacity == 0`.",
                "Verify `head_` and `tail_` wrap cleanly without overwriting unread items.",
                "Confirm `count_` stays synchronized with `push` and `pop`.",
            ],
            "expandable_hints": [
                {
                    "line": 14,
                    "label": "Check capacity=0 guard",
                    "detail": "When `capacity == 0`, `count_ == buffer_.size()` (0 == 0) is true and `buffer_.empty()` is true, so `push` returns `false` before `% buffer_.size()`.",
                },
            ],
        },
    },
    {
        "id": "sys_packet_parser",
        "title": "Systems: Network Packet Frame Parser",
        "difficulty": "Hard",
        "pair_group": "S",
        "task_set": "systems_challenge",
        "problem_statement": (
            "Write a C++ function `bool extractPayload(...)` that reads a 2-byte big-endian payload length "
            "at `offset` from a raw byte buffer `frame` and copies `payloadLen` bytes into `outPayload`."
        ),
        "code": (
            "#include <cstdint>\n"
            "#include <cstddef>\n"
            "#include <vector>\n"
            "\n"
            "bool extractPayload(const std::vector<uint8_t>& frame,\n"
            "                    size_t offset,\n"
            "                    std::vector<uint8_t>& outPayload) {\n"
            "    if (offset + 2 > frame.size()) {\n"
            "        return false;\n"
            "    }\n"
            "    uint16_t payloadLen = (static_cast<uint16_t>(frame[offset]) << 8) |\n"
            "                          static_cast<uint16_t>(frame[offset + 1]);\n"
            "    uint16_t endPos = static_cast<uint16_t>(offset + 2 + payloadLen);\n"
            "    if (endPos > frame.size()) {\n"
            "        return false;\n"
            "    }\n"
            "    outPayload.assign(frame.begin() + offset + 2,\n"
            "                      frame.begin() + offset + 2 + payloadLen);\n"
            "    return true;\n"
            "}"
        ),
        "ground_truth_correct": False,
        "ground_truth_error_line": 13,
        "ground_truth_error_description": (
            "`endPos` is stored in a `uint16_t`, so `offset + 2 + payloadLen` can wrap around modulo 65536 "
            "(e.g., if `payloadLen = 65535` and `offset = 4`, `endPos` wraps to `5`, bypassing `endPos > frame.size()` and causing an out-of-bounds read on line 18)."
        ),
        "ground_truth_test_case": "frame.size() = 10, offset = 4, payloadLen = 65535 -> endPos wraps to 5 <= 10 -> out-of-bounds read",
        "explanation_notes": [
            {
                "line": 8,
                "title": "Header Bounds Check",
                "text": "Ensures at least 2 header bytes exist starting at `offset`.",
            },
            {
                "line": 11,
                "title": "Big-Endian Length Decode",
                "text": "Combines two bytes into a 16-bit unsigned `payloadLen`.",
            },
            {
                "line": 13,
                "title": "Payload End Calculation",
                "text": "Computes `endPos` as `uint16_t` and compares it against `frame.size()`.",
            },
        ],
        "verification_guided": {
            "assumptions": [
                "Assumes `frame` is an untrusted network buffer of arbitrary size.",
                "Assumes `offset` is small relative to `SIZE_MAX`.",
            ],
            "suggested_edge_cases": [
                "Malicious `payloadLen = 65535` on a 10-byte `frame`",
                "Zero-length payload (`payloadLen = 0`) at the end of `frame`",
                "`offset` near `frame.size()` (e.g., `offset = frame.size() - 1`)",
            ],
            "attention_lines": [8, 13, 14, 18],
            "checklist": [
                "Check integer width used in `endPos` bounds calculation.",
                "Test whether `offset + 2 + payloadLen` can overflow `uint16_t`.",
                "Verify `outPayload.assign(...)` uses safe iterators.",
            ],
            "expandable_hints": [
                {
                    "line": 13,
                    "label": "Check `uint16_t` wrap-around",
                    "detail": "A 16-bit unsigned integer holds 0..65535; adding `offset + 2 + payloadLen` can wrap past 65535 to a small value.",
                },
            ],
        },
    },
    {
        "id": "sys_slab_allocator_100",
        "title": "Complex Systems (108 Lines): Fixed-Block Page & Slab Allocator",
        "difficulty": "Hard",
        "pair_group": "S",
        "task_set": "systems_challenge",
        "problem_statement": (
            "Review this 108-line C++ `SlabAllocator` modeled after a kernel fixed-size object cache. "
            "It manages fixed-size slots across multiple memory pages, tracks allocation bitmaps, "
            "supports `allocate()`, `deallocate()`, and `ownsAddress()`, and reports utilization stats."
        ),
        "code": (
            "#include <cstdint>\n"
            "#include <cstddef>\n"
            "#include <vector>\n"
            "#include <cstring>\n"
            "#include <stdexcept>\n"
            "\n"
            "struct SlabPage {\n"
            "    uint8_t* memory;\n"
            "    std::vector<bool> used;\n"
            "    size_t freeCount;\n"
            "\n"
            "    SlabPage(size_t slotSize, size_t slotsPerPage)\n"
            "        : memory(new uint8_t[slotSize * slotsPerPage]),\n"
            "          used(slotsPerPage, false),\n"
            "          freeCount(slotsPerPage) {\n"
            "        std::memset(memory, 0, slotSize * slotsPerPage);\n"
            "    }\n"
            "\n"
            "    ~SlabPage() {\n"
            "        delete[] memory;\n"
            "    }\n"
            "\n"
            "    SlabPage(const SlabPage&) = delete;\n"
            "    SlabPage& operator=(const SlabPage&) = delete;\n"
            "\n"
            "    SlabPage(SlabPage&& other) noexcept\n"
            "        : memory(other.memory),\n"
            "          used(std::move(other.used)),\n"
            "          freeCount(other.freeCount) {\n"
            "        other.memory = nullptr;\n"
            "        other.freeCount = 0;\n"
            "    }\n"
            "};\n"
            "\n"
            "class SlabAllocator {\n"
            "public:\n"
            "    SlabAllocator(size_t slotSize, size_t slotsPerPage)\n"
            "        : slotSize_(slotSize),\n"
            "          slotsPerPage_(slotsPerPage),\n"
            "          totalAllocated_(0) {\n"
            "        if (slotSize_ == 0 || slotsPerPage_ == 0) {\n"
            "            throw std::invalid_argument(\"Slot size and count must be > 0\");\n"
            "        }\n"
            "        pages_.emplace_back(slotSize_, slotsPerPage_);\n"
            "    }\n"
            "\n"
            "    void* allocate() {\n"
            "        for (auto& page : pages_) {\n"
            "            if (page.freeCount == 0) {\n"
            "                continue;\n"
            "            }\n"
            "            for (size_t i = 0; i < slotsPerPage_; i++) {\n"
            "                if (!page.used[i]) {\n"
            "                    page.used[i] = true;\n"
            "                    page.freeCount--;\n"
            "                    totalAllocated_++;\n"
            "                    return page.memory + (i * slotSize_);\n"
            "                }\n"
            "            }\n"
            "        }\n"
            "        pages_.emplace_back(slotSize_, slotsPerPage_);\n"
            "        SlabPage& newPage = pages_.back();\n"
            "        newPage.used[0] = true;\n"
            "        newPage.freeCount--;\n"
            "        totalAllocated_++;\n"
            "        return newPage.memory;\n"
            "    }\n"
            "\n"
            "    bool deallocate(void* ptr) {\n"
            "        if (ptr == nullptr) {\n"
            "            return false;\n"
            "        }\n"
            "        const uint8_t* bytePtr = static_cast<const uint8_t*>(ptr);\n"
            "        for (auto& page : pages_) {\n"
            "            const uint8_t* start = page.memory;\n"
            "            const uint8_t* end = start + (slotSize_ * slotsPerPage_);\n"
            "            if (bytePtr >= start && bytePtr < end) {\n"
            "                size_t offset = static_cast<size_t>(bytePtr - start);\n"
            "                if (offset % slotSize_ != 0) {\n"
            "                    return false;\n"
            "                }\n"
            "                size_t idx = offset / slotSize_;\n"
            "                if (!page.used[idx]) {\n"
            "                    return false;\n"
            "                }\n"
            "                page.used[idx] = false;\n"
            "                page.freeCount++;\n"
            "                totalAllocated_--;\n"
            "                return true;\n"
            "            }\n"
            "        }\n"
            "        return false;\n"
            "    }\n"
            "\n"
            "    bool ownsAddress(const void* ptr) const {\n"
            "        const uint8_t* bytePtr = static_cast<const uint8_t*>(ptr);\n"
            "        for (const auto& page : pages_) {\n"
            "            const uint8_t* start = page.memory;\n"
            "            const uint8_t* end = start + (slotSize_ * slotsPerPage_);\n"
            "            if (bytePtr >= start && bytePtr < end) {\n"
            "                return true;\n"
            "            }\n"
            "        }\n"
            "        return false;\n"
            "    }\n"
            "\n"
            "    size_t pageCount() const { return pages_.size(); }\n"
            "    size_t activeAllocations() const { return totalAllocated_; }\n"
            "\n"
            "private:\n"
            "    size_t slotSize_;\n"
            "    size_t slotsPerPage_;\n"
            "    size_t totalAllocated_;\n"
            "    std::vector<SlabPage> pages_;\n"
            "};"
        ),
        "ground_truth_correct": True,
        "ground_truth_error_line": None,
        "ground_truth_error_description": None,
        "ground_truth_test_case": None,
        "explanation_notes": [
            {
                "line": 26,
                "title": "Noexcept Move Constructor",
                "text": "Transfers raw `memory` ownership and nulls `other.memory` so `std::vector<SlabPage>` growth is safe.",
            },
            {
                "line": 47,
                "title": "First-Fit & Page Growth",
                "text": "Scans existing pages for `freeCount > 0`, or appends a new `SlabPage` when all pages are full.",
            },
            {
                "line": 70,
                "title": "Pointer Validation in Deallocate",
                "text": "Checks `ptr != nullptr`, address range `[start, end)`, slot alignment (`offset % slotSize_ == 0`), and double-free.",
            },
        ],
        "verification_guided": {
            "assumptions": [
                "Assumes `slotSize_` and `slotsPerPage_` are strictly positive.",
                "Assumes `deallocate` only frees aligned slot start addresses.",
            ],
            "suggested_edge_cases": [
                "Allocate more than `slotsPerPage_` items to trigger a second `SlabPage`",
                "Call `deallocate(ptr + 1)` with an unaligned interior pointer",
                "Call `deallocate(ptr)` twice on the same pointer (double-free)",
            ],
            "attention_lines": [26, 61, 79, 83],
            "checklist": [
                "Check `SlabPage` move semantics when `pages_` reallocates.",
                "Check alignment and double-free guards in `deallocate`.",
                "Verify `totalAllocated_` and `freeCount` stay consistent across page growth.",
            ],
            "expandable_hints": [
                {
                    "line": 26,
                    "label": "Check `SlabPage` move safety",
                    "detail": "Because `SlabPage(SlabPage&&)` is `noexcept` and sets `other.memory = nullptr`, `delete[] nullptr` on the moved-from object is a safe no-op.",
                },
            ],
        },
    },
]
