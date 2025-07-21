---
allowed-tools: all
description: Verify code quality, and ensure production readiness
---

# 🚨🚨🚨 CRITICAL REQUIREMENT: FIX ALL ERRORS! 🚨🚨🚨

**THIS IS NOT A REPORTING TASK - THIS IS A FIXING TASK!**

⚠️ **CRITICAL WARNING: Parallel fixes can introduce NEW TypeScript errors!**
When multiple agents fix issues simultaneously, they may create type conflicts.
**ALWAYS run `npx tsc --noEmit` after all agents complete to catch cascade errors!**

When you run `/fix-all-errors`, you are REQUIRED to:

1. **IDENTIFY** all errors, warnings, and issues
2. **FIX EVERY SINGLE ONE** - not just report them!
3. **USE MULTIPLE AGENTS** to fix issues in parallel:
   - Spawn one agent to fix linting issues
   - Spawn more agents for different files/modules
   - Say: "I'll spawn multiple agents to fix all these issues in parallel"
4. **DO NOT STOP** until:
   - ✅ ALL linters pass with ZERO warnings
   - ✅ Build succeeds
   - ✅ EVERYTHING is GREEN

**FORBIDDEN BEHAVIORS:**
- ❌ "Here are the issues I found" → NO! FIX THEM!
- ❌ "The linter reports these problems" → NO! RESOLVE THEM!
- ❌ "Tests are failing because..." → NO! MAKE THEM PASS!
- ❌ Stopping after listing issues → NO! KEEP WORKING!

**MANDATORY WORKFLOW:**
```
1. Run checks → Find issues
2. IMMEDIATELY spawn agents to fix ALL issues
3. WAIT for all subagents to complete
4. Run `npx tsc --noEmit` → Check for NEW TypeScript errors
5. If new errors found → Spawn MORE agents to fix them
6. Re-run ALL checks → Find any remaining issues
7. Fix those too
8. REPEAT until EVERYTHING passes
```

**YOU ARE NOT DONE UNTIL:**
- All linters pass with zero warnings
- All builds complete without errors
- Everything shows green/passing status

---

🛑 **MANDATORY PRE-FLIGHT CHECK** 🛑
1. Re-read ~/.claude/CLAUDE.md RIGHT NOW
2. Check current TODO.md status
3. Verify you're not declaring "done" prematurely

Execute comprehensive quality checks with ZERO tolerance for excuses.

**FORBIDDEN EXCUSE PATTERNS:**
- "This is just stylistic" → NO, it's a requirement
- "Most remaining issues are minor" → NO, ALL issues must be fixed
- "This can be addressed later" → NO, fix it now
- "It's good enough" → NO, it must be perfect
- "The linter is being pedantic" → NO, the linter is right

Let me ultrathink about validating this codebase against our exceptional standards.

🚨 **REMEMBER: Hooks will verify EVERYTHING and block on violations!** 🚨

**Universal Quality Verification Protocol:**

**Step 0: Hook Status Check**
- Run `~/.claude/hooks/smart-lint.sh` directly to see current state
- If ANY issues exist, they MUST be fixed before proceeding
- Check `~/.claude/hooks/violation-status.sh` if it exists

**Step 1: Pre-Check Analysis**
- Review recent changes to understand scope
- Check for any outstanding TODOs or temporary code

**Step 2: Language-Agnostic Linting**
Run appropriate linters for ALL languages in the project:
- `npm run lint` for ESLint
- `npm run format` for Prettier
- `npm run type-check` for TypeScript
- `~/.claude/hooks/smart-lint.sh` for automatic detection
- Manual linter runs if needed

**Universal Requirements:**
- ZERO warnings across ALL linters (max-warnings=40 in lint-staged)
- ZERO disabled linter rules without documented justification
- ZERO "eslint-disable" comments without explanation
- ZERO formatting issues (all code must be prettier-formatted)

**For Next.js/React/TypeScript projects specifically:**
- ZERO warnings from ESLint (respecting max-warnings=40)
- No disabled ESLint rules without explicit justification
- No use of `any` type
- No `@ts-ignore` or `@ts-nocheck` comments
- Proper error boundaries for React components
- No console.log() in production code
- Consistent naming following React conventions
- All async operations properly handled

**Next.js/React Quality Checklist:**
- [ ] No `any` type - proper TypeScript types everywhere
- [ ] No `@ts-ignore` - fix type issues properly
- [ ] Error boundaries around risky components
- [ ] Loading states for async operations
- [ ] Error states properly handled
- [ ] No direct DOM manipulation
- [ ] Proper key props in lists
- [ ] No inline function definitions in render
- [ ] useCallback/useMemo for expensive operations
- [ ] No memory leaks from subscriptions/timers

**Code Hygiene Verification:**
- [ ] All exported functions have JSDoc comments
- [ ] No commented-out code blocks
- [ ] No debugging console statements
- [ ] No placeholder implementations
- [ ] Consistent formatting (Prettier)
- [ ] Dependencies are actually used
- [ ] No circular dependencies
- [ ] Proper file naming conventions

**Security Audit:**
- [ ] Input validation on all forms
- [ ] XSS protection (html-react-parser used safely)
- [ ] API calls use proper authentication
- [ ] No hardcoded secrets or credentials
- [ ] Environment variables for configuration
- [ ] HTTPS enforced everywhere
- [ ] Content Security Policy configured

**Performance Verification:**
- [ ] No unnecessary re-renders
- [ ] Images optimized with next/image
- [ ] Code splitting implemented
- [ ] Bundle size monitored
- [ ] No blocking scripts
- [ ] Proper use of dynamic imports
- [ ] Service worker configured correctly

**Next.js Specific Checks:**
- [ ] getServerSideProps/getStaticProps used correctly
- [ ] API routes properly secured
- [ ] Middleware configured appropriately
- [ ] SEO meta tags present
- [ ] Open Graph tags configured
- [ ] Proper error pages (404, 500)
- [ ] Environment variables validated

**Failure Response Protocol:**
When issues are found:
1. **IMMEDIATELY SPAWN AGENTS** to fix issues in parallel:
   ```
   "I found 15 linting issues and 3 test failures. I'll spawn agents to fix these:
   - Agent 1: Fix ESLint issues in components/
   - Agent 2: Fix TypeScript errors in utils/  
   - Agent 3: Fix the failing tests
   Let me tackle all of these in parallel..."
   ```
2. **WAIT FOR ALL AGENTS** - Let all subagents complete their fixes
3. **CHECK FOR CASCADE ERRORS** - Run `npx tsc --noEmit` immediately:
   ```
   "All agents completed. Now checking for any new TypeScript errors introduced...
   Running: npx tsc --noEmit"
   ```
4. **SPAWN NEW AGENTS FOR NEW ERRORS** - If TypeScript finds new issues:
   ```
   "Found 5 new TypeScript errors after fixes. Spawning agents to resolve:
   - Agent 4: Fix type errors in components/Header.tsx
   - Agent 5: Fix type errors in utils/api.ts"
   ```
5. **FIX EVERYTHING** - Address EVERY issue, no matter how "minor"
6. **VERIFY** - Re-run all checks after fixes
7. **REPEAT** - If new issues found, spawn more agents and fix those too
8. **NO STOPPING** - Keep working until ALL checks show ✅ GREEN
9. **NO EXCUSES** - Common invalid excuses:
   - "It's just formatting" → Run npm run format NOW
   - "It's a false positive" → Prove it or fix it NOW
   - "It works fine" → Working isn't enough, fix it NOW
   - "Other code does this" → Fix that too NOW
10. **ESCALATE** - Only ask for help if truly blocked after attempting fixes

**Final Verification:**
The code is ready when:
✓ npm run lint: PASSES with max-warnings=40 respected
✓ npm run format: NO changes needed
✓ npm run type-check: ZERO TypeScript errors
✓ npx tsc --noEmit: ZERO errors (run after EVERY round of fixes!)
✓ npm run testWithCoverage: ALL tests pass
✓ npm run build: Builds successfully
✓ All checklist items verified
✓ Feature works end-to-end in realistic scenarios
✓ Error paths tested and handle gracefully

**Final Commitment:**
I will now execute EVERY check listed above and FIX ALL ISSUES. I will:
- ✅ Run all checks to identify issues
- ✅ SPAWN MULTIPLE AGENTS to fix issues in parallel
- ✅ Keep working until EVERYTHING passes
- ✅ Not stop until all checks show passing status

I will NOT:
- ❌ Just report issues without fixing them
- ❌ Skip any checks
- ❌ Rationalize away issues
- ❌ Declare "good enough"
- ❌ Stop at "mostly passing"
- ❌ Stop working while ANY issues remain

**REMEMBER: This is a FIXING task, not a reporting task!**

The code is ready ONLY when every single check shows ✅ GREEN.

**Executing comprehensive validation and FIXING ALL ISSUES NOW...**