# Fix Plan: Notes API

## 1. Fix `update_note` double DB connection

**File**: `app/main.py:108-136`

The `update_note` endpoint opens two separate connections: one for the UPDATE, then another for the SELECT. Combine into a single connection.

**Steps**:
- After `conn.commit()`, run the SELECT on the same connection before closing
- Remove the second `get_db_connection()` / `conn.close()` pair

---

## 2. Change POST `/notes` status code to 201

**File**: `app/main.py:48-71`

POST creating a new resource should return `201 Created`, not `200`.

**Steps**:
- Add `status_code=status.HTTP_201_CREATED` to the `@app.post("/notes")` decorator
- Update all tests in `test/test_api.py` that assert `200` on POST `/notes` to assert `201`

---

## 4. Fix XSS vulnerability in `demo.html`

**File**: `templates/demo.html:208-232` and `templates/demo.html:247-280`

`note.title` and `note.body` are injected directly into `innerHTML`, allowing script injection if a note contains `<script>` tags.

**Steps**:
- Replace `innerHTML` assignment in `createNoteCard` with safe text assignment
- Use `textContent` or `document.createTextNode` for user-supplied content
- Also fix the edit form (`editNote` function) which injects `title`/`body` into `innerHTML` via attribute values — escape quotes and HTML entities

---

## 5. Add pagination to `GET /notes`

**File**: `app/main.py:73-88`

Currently returns all notes with no limit. Add query parameters for pagination.

**Steps**:
- Add `skip: int = 0` and `limit: int = 50` query parameters to `get_notes()`
- Add `OFFSET ? LIMIT ?` to the SQL query
- Clamp `limit` to a reasonable max (e.g., 100)
- Add tests for pagination behavior

---

## 6. Consider async SQLite (low priority / optional)

**File**: `app/main.py`

All endpoints are synchronous. For production workloads, async DB access prevents blocking the event loop.

**Options**:
- **Option A**: Add `aiosqlite` dependency, convert endpoints to `async def`, use `await` for DB calls
- **Option B**: Keep synchronous but run in a thread pool via `app.run_in_threadpool()` (FastAPI default for sync endpoints)
- **Recommendation**: Option B is already the default behavior in FastAPI, so no code change needed. Document this explicitly. If higher concurrency is needed later, migrate to Option A.

**Decision**: Document current behavior. Defer async migration unless performance testing shows it's needed.

---

## Implementation Order

1. **Fix 1** — double DB connection (quick refactor, no behavior change)
2. **Fix 2** — 201 status code (requires test update)
3. **Fix 4** — XSS fix in `demo.html` (security)
4. **Fix 5** — pagination (new feature, requires API change + tests)
5. **Fix 6** — document async behavior (no code change)
