# Development Partnership

Building production-quality code together. Create maintainable, efficient solutions. When stuck/complex, I'll redirect.

## 🚨 AUTOMATED CHECKS MANDATORY
**ALL hook issues BLOCKING - EVERYTHING ✅ GREEN!** Zero tolerance for errors/formatting/linting.

## CRITICAL WORKFLOW

### Research→Plan→Implement (NEVER SKIP!)
1. **Research**: Explore codebase, understand patterns
2. **Plan**: Detailed implementation plan, verify with me
3. **Implement**: Execute with validation checkpoints

Always say: "Let me research the codebase and create a plan before implementing."

For complex decisions: "Let me ultrathink about this architecture before proposing a solution."

### USE MULTIPLE AGENTS!
Spawn agents for:
- Parallel codebase exploration
- Writing tests while implementing features
- Research tasks ("I'll have an agent investigate X while I analyze Y")
- Complex refactors (one identifies, another implements)

Say: "I'll spawn agents to tackle different aspects" for multi-part tasks.

### Reality Checkpoints
Validate at: feature completion, new components, something feels wrong, declaring "done", **HOOK FAILURES ❌**

Run: `npm run format && npm run lint && npm run type-check`

### 🚨 Hook Failures = BLOCKING
1. **STOP** - Don't continue
2. **FIX ALL** - Every ❌ to ✅
3. **VERIFY** - Re-run command
4. **CONTINUE** - Return to original task
5. **NEVER IGNORE** - No exceptions

Includes: formatting (prettier), linting (eslint), type errors, ALL checks. 100% clean required.

**Recovery**: Maintain task awareness, fix issues, verify, continue original work.

## Working Memory

**Long context**: Re-read CLAUDE.md, summarize in PROGRESS.md, document state

**TODO.md**:
```
## Current Task
- [ ] What RIGHT NOW
## Completed  
- [x] Done and tested
## Next Steps
- [ ] What next
```

## Git: Brief, clear commits
- Never git commit without my permission

## JavaScript/TypeScript Rules

### FORBIDDEN:
- NO `any` type - use proper types!
- NO `@ts-ignore` - fix the type issue!
- NO console.log() in production code
- NO commented-out code
- NO old+new code together
- NO migration/compatibility layers
- NO versioned names (V2, New)
- NO TODOs in final code
- NO setTimeout for async coordination - use Promises/async-await

### REQUIRED:
- Delete old code when replacing
- Meaningful names: `userId` not `id`
- Early returns
- Proper TypeScript types everywhere
- Async/await over callbacks
- Named exports for better tree-shaking
- Error boundaries for React components
- Proper loading/error states

## Standards

**Complete when**: prettier passes, eslint passes (max-warnings=40), type-check passes, tests pass, works e2e

**Testing**: Complex logic→test first, Components→test after render, Utils→comprehensive tests

## Problem-Solving

When stuck:
1. **Stop** - Don't spiral
2. **Delegate** - Spawn agents
3. **Ultrathink** - "I need to ultrathink through this challenge"
4. **Step back** - Re-read requirements
5. **Simplify** - Simple usually correct
6. **Ask** - "I see [A] vs [B]. Which preferred?"

## Performance/Security

**Measure First**: No premature optimization, use React DevTools, Lighthouse for metrics

**Security Always**: Validate inputs, sanitize HTML (html-react-parser), secure API calls, HTTPS only

## Communication

**Progress**:
```
✓ Implemented auth component (tests passing)
✗ TypeScript error in user hook - investigating
```

**Improvements**: "Current works, but [observation]. Should I [improvement]?"

## Working Together
- Feature branch - no backwards compatibility
- Clarity > cleverness
- **REMINDER**: Re-read if 30+ minutes passed

## Scripts Reference
- `npm run dev` - Development server
- `npm run build` - Production build
- `npm run format` - Prettier formatting
- `npm run lint` - ESLint check
- `npm run type-check` - TypeScript check
- `npm run testWithCoverage` - Run tests with coverage

## Misc
- C:\ paths → /mnt/c (WSL mounted)
- Use `date` for system time. Your idea of what the current datetime is always wrong.