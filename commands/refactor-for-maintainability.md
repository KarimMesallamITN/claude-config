---
allowed-tools: all
description: Refactor specific files/features for maintainability without changing functionality
---

# 🔧🔧🔧 CRITICAL REQUIREMENT: REFACTOR WITHOUT BREAKING! 🔧🔧🔧

**THIS IS NOT A REPORTING TASK - THIS IS A REFACTORING TASK!**

⚠️ **CRITICAL WARNING: Refactoring can introduce subtle behavioral changes!**
When multiple subagents refactor simultaneously, they may break interdependencies.
**ALWAYS create behavior snapshots before refactoring and verify after!**
**ALWAYS spawn subagents in ONE PROMPT for true parallel execution!**
**USE PARALLEL SUBAGENTS for ALL phases: snapshot, analysis, refactoring, verification!**

When you run `/refactor-for-maintainability`, you are REQUIRED to:

1. **SNAPSHOT** the target scope: $ARGUMENTS (via parallel subagents)
2. **ANALYZE** all code smells and issues (via parallel subagents)
3. **REFACTOR EVERY CODE SMELL** - not just report them!
4. **USE MULTIPLE SUBAGENTS** to refactor in parallel via instructions written in one prompt:
   - Spawn subagents for different modules/components
   - Spawn subagents for specific refactoring patterns
   - Say: "I'll spawn multiple subagents to refactor these areas in parallel via one prompt"
5. **DO NOT STOP** until:
   - ✅ ALL dead code eliminated
   - ✅ ZERO code duplication
   - ✅ Complexity metrics GREEN
   - ✅ EXACT functionality preserved

**FORBIDDEN BEHAVIORS:**
- ❌ "Here's what could be improved" → NO! IMPROVE IT!
- ❌ "This method is too complex" → NO! EXTRACT IT!
- ❌ "There's duplicate logic here" → NO! CONSOLIDATE IT!
- ❌ Changing ANY behavior → NO! PRESERVE EXACT FUNCTIONALITY!
- ❌ Spawning subagents one by one → NO! ALL IN ONE PROMPT!

**MANDATORY WORKFLOW:**
```
1. Snapshot behavior → Spawn subagents IN ONE PROMPT to capture all functionality
2. Analyze code smells → Spawn subagents IN ONE PROMPT to find all issues
3. IMMEDIATELY spawn subagents to refactor ALL issues in ONE PROMPT
   (NOT sequentially - write all subagent instructions together!)
4. WAIT for all subagents to complete
5. Run behavior verification → Spawn subagents IN ONE PROMPT to verify
6. If behavior changed → REVERT and try different approach
7. Re-analyze → Find any remaining issues (use subagents if needed)
8. REPEAT until architecture is CLEAN
```

**YOU ARE NOT DONE UNTIL:**
- Zero code duplication in target scope (verified by parallel subagents)
- All functions < 50 lines (checked across all files simultaneously)
- Cyclomatic complexity < 10 (analyzed in parallel)
- All SOLID principles satisfied (validated by multiple subagents)
- Behavior 100% unchanged (confirmed by parallel verification)

---

🛑 **MANDATORY PRE-REFACTOR CHECK** 🛑
1. Create comprehensive behavior snapshot via MULTIPLE SUBAGENTS IN ONE PROMPT
2. Document all side effects and edge cases (parallel capture)
3. Verify you understand EXACT current behavior from all subagents

Execute refactoring with ZERO tolerance for behavioral changes.

**FORBIDDEN EXCUSE PATTERNS:**
- "This works better now" → NO, maintain exact behavior
- "The old way was buggy" → NO, preserve bugs if depended upon
- "This is more efficient" → NO, maintain performance profile
- "Users won't notice" → NO, they might depend on it
- "It's cleaner this way" → NO, only if behavior identical
- "I'll check these one by one" → NO, use parallel subagents!

🔧 **REMEMBER: If it changes behavior, it's NOT refactoring!** 🔧

**Refactoring Target Analysis:**

**Step 0: Behavior Snapshot**
- **SPAWN MULTIPLE SUBAGENTS IN ONE PROMPT** to capture behavior:
  ```
  "Creating comprehensive behavior snapshot for $ARGUMENTS. Spawning subagents in parallel via one prompt:
  
  Subagent 1: Capture ALL inputs/outputs for component modules
  Subagent 2: Document ALL side effects (I/O, state changes, timing)
  Subagent 3: Create characterization tests for untested code
  Subagent 4: Record performance baselines and memory patterns
  Subagent 5: Catalog error scenarios and edge cases
  
  Launching all snapshot subagents NOW in parallel..."
  ```
- Consolidate all subagent findings into master behavior snapshot
- Verify snapshot is complete before ANY refactoring begins

**Step 1: Code Smell Detection**
**SPAWN SUBAGENTS IN ONE PROMPT** to identify smells across target scope:
```
"Analyzing code smells in $ARGUMENTS. Spawning analysis subagents in parallel via one prompt:

Subagent 1: Detect long methods and complex conditionals
Subagent 2: Find duplicate code patterns
Subagent 3: Identify coupling and cohesion issues
Subagent 4: Locate dead code and unused dependencies
Subagent 5: Check for SOLID principle violations

Launching all analysis subagents NOW in parallel..."
```

Then FIX these smells in target scope:
- Long methods (> 50 lines) → Extract Method
- Large classes (> 300 lines) → Split Responsibilities
- Long parameter lists (> 3) → Parameter Object
- Duplicate code → Extract Shared Logic
- Complex conditionals → Strategy Pattern
- Feature envy → Move Method
- Data clumps → Extract Class

**Step 2: Apply Refactoring Patterns**
- Repository Pattern for data access
- Factory Pattern for object creation
- Strategy Pattern for algorithms
- Observer Pattern for events
- Adapter Pattern for integrations

**Architecture Quality Checklist:**
- [ ] Single Responsibility - one reason to change
- [ ] Open/Closed - extensible without modification
- [ ] Liskov Substitution - subtypes substitutable
- [ ] Interface Segregation - no unused methods
- [ ] Dependency Inversion - depend on abstractions
- [ ] No circular dependencies
- [ ] Clear module boundaries
- [ ] Proper error handling preserved
- [ ] All edge cases still work

**Code Metrics Requirements:**
- [ ] Cyclomatic Complexity < 10
- [ ] Cognitive Complexity < 15
- [ ] Method length < 50 lines
- [ ] Class length < 300 lines
- [ ] Coupling < 5 per module
- [ ] Zero duplicate code blocks
- [ ] All dead code removed

**Behavioral Preservation:**
- [ ] All inputs produce same outputs
- [ ] Side effects occur in same order
- [ ] Error messages unchanged
- [ ] Performance within 10%
- [ ] Memory patterns preserved
- [ ] Async behavior identical
- [ ] State mutations unchanged

**Failure Response Protocol:**
When finding refactoring opportunities:
1. **IMMEDIATELY SPAWN SUBAGENTS** to refactor in parallel (all in one prompt):
   ```
   "I found 23 refactoring opportunities in $ARGUMENTS. I'll spawn subagents in parallel via one prompt:
   
   Subagent 1: Extract 5 long methods in components/
   Subagent 2: Remove duplicate logic across 3 files
   Subagent 3: Apply Repository Pattern to data access
   Subagent 4: Simplify complex conditionals
   
   Launching all subagents NOW in parallel..."
   ```
   **CRITICAL: Write ALL subagent instructions in ONE prompt for parallel execution!**
2. **VERIFY BEHAVIOR** after each batch of subagents completes:
   ```
   "All refactoring subagents completed. Spawning verification subagents in parallel via one prompt:
   
   Subagent 1: Compare input/output behavior against snapshot
   Subagent 2: Verify all side effects unchanged
   Subagent 3: Check performance within 10% tolerance
   Subagent 4: Validate error handling preserved
   Subagent 5: Confirm API contracts maintained
   
   Launching all verification subagents NOW in parallel..."
   ```
3. **REVERT IF CHANGED** - Any behavioral change means REVERT:
   ```
   "Behavior changed in auth flow! Reverting Subagent 2's changes.
   Trying different refactoring approach..."
   ```
4. **CONTINUE REFACTORING** - Keep improving architecture
5. **NO STOPPING** - Continue until ALL smells eliminated
6. **SPAWN MORE SUBAGENTS** - If new issues found, spawn them ALL IN ONE PROMPT

**Final Verification:**
The refactoring is complete when ALL parallel verification subagents confirm:
✓ Behavior snapshot: 100% match with original (verified in parallel)
✓ All code smells: ELIMINATED (checked by multiple subagents)
✓ Complexity metrics: ALL GREEN (analyzed simultaneously)
✓ SOLID principles: FULLY satisfied (validated in parallel)
✓ Performance: Within 10% of original (tested concurrently)
✓ All tests: Still passing if any exist (run in parallel)
✓ Module boundaries: Clean and clear (verified by subagents)
✓ Dead code: ZERO remaining (confirmed across all files)

**Final Commitment:**
I will now refactor $ARGUMENTS while preserving EXACT behavior. I will:
- ✅ Create behavior snapshots via MULTIPLE SUBAGENTS IN ONE PROMPT
- ✅ SPAWN MULTIPLE SUBAGENTS to refactor in parallel via one prompt
- ✅ Apply proven refactoring patterns
- ✅ Verify behavior unchanged after EVERY modification
- ✅ Keep working until architecture is CLEAN

I will NOT:
- ❌ Change any observable behavior
- ❌ "Fix" bugs unless explicitly asked
- ❌ Optimize performance unless preserving profile
- ❌ Add new features or capabilities
- ❌ Break backward compatibility
- ❌ Stop while code smells remain

**REMEMBER: This is a REFACTORING task, not a rewriting task!**

The code is ready ONLY when it's CLEAN but behaves IDENTICALLY.

**Executing comprehensive PARALLEL refactoring of $ARGUMENTS NOW...**
(Snapshot → Analyze → Refactor → Verify - ALL IN PARALLEL IN ONE PROMPT!)