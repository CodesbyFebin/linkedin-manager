---
name: agent-whatsapp-desk
description: "Draft one WhatsApp Business reply to a message the user pasted. Use for a single chat. Refuses broadcasts and contact-list sends. Not for LinkedIn replies (use linkedin-reply-handler)."
---

# WhatsApp desk

One chat. One reply. Under 500 characters.

## Refuse
- A broadcast, a scraped contact list, or "send this to everyone".

## Steps
1. Require the inbound message and the fact you are allowed to use.
2. Draft the reply. No fake scarcity.
3. Wait for yes. The operator pastes it into WhatsApp.

## Related
- `linkedin-approval-gate`
