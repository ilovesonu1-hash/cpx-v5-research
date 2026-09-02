@AGENTS.md

# Claude Code adapter

- Follow the imported repository authority and task router.
- Use the current-state document named by `AGENTS.md` as the authority for
  current phase, gates, effective checkpoints, blockers, and next permitted
  action.
- Repository files and verified Git state override conversation history,
  resumed-session memory, and auto memory.
- Load only the minimum context routed for the classified task.
- Do not infer authorization to advance beyond the recorded boundary.
