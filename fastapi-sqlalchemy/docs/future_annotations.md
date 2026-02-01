You’re getting this error because **`Employee` is used in `Company` *before it is defined*** in the file.
Pylance is correctly complaining.

You have **three clean ways** to fix this. I’ll show them in order of best practice.

---

# ✅ **Solution 1 — Best (recommended in modern SQLAlchemy)**

Use **`from __future__ import annotations`**

At the **very top of your file**, add this:

```python
from __future__ import annotations
```

Then your original line works as-is:

```python
employees: Mapped[list[Employee]] = relationship(back_populates="company")
```

### ✅ Final working top of file should look like:

```python
from __future__ import annotations   # ← VERY IMPORTANT

from typing import override
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from src.database.config import Base
```

👉 What this does:

It makes all annotations **lazy-evaluated as strings automatically**, so Python doesn’t need `Employee` to be defined yet.

This is the **cleanest modern fix**.

---

# ✅ **Solution 2 — Manual string forward reference (old style)**

If you *don’t* want `__future__` import, change this line to:

```python
employees: Mapped[list["Employee"]] = relationship(back_populates="company")
```

Notice quotes around `"Employee"`.

This also fixes the error.

---

# ✅ **Solution 3 — TYPE_CHECKING pattern (optional/advanced)**

If you want strict typing + avoid quotes:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import Employee   # or wherever Employee lives
```

But this is usually unnecessary here.

---

# ✅ Your corrected minimal version (recommended)

```python
from __future__ import annotations   # ← ADD THIS

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.config import Base
```

Everything else in your models is **already correct for joined inheritance.**

---

# Bonus: Why this happens

Your file is read top-to-bottom:

1. Python sees `Company`
2. Inside `Company`, you reference `Employee`
3. But `Employee` is defined **later**
4. → Pylance: *“Employee is not defined”*

`__future__.annotations` solves this elegantly.

---

# If you want, I can:

* refactor your whole file in a production-ready style, or
* adapt this pattern to your FastAPI project (users, roles, etc.).
