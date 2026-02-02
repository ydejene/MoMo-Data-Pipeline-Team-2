## ERD Design Rationale
Our database is built around the core idea that every MoMo transaction involves an individual, a transaction type, and potentially multiple fees. We structured it this way to reflect reality while keeping data clean and queryable.

It starts with Momo_User to store customer information; name, phone number, and optional email. Phone is the natural key here since it's how the system identifies people, but we also give each user a numeric ID (surrogate key) to make joins fast and stable even if phone numbers change. We index both the phone and username so searches are quick.

Transaction_Categories is a lookup table for transaction types: Transfer, Airtime Purchase, Bill Payment, etc. We keep this separate so if the business decides to add a new category or rename one, we don't have to rewrite history. Each transaction points to exactly one category.

Transactions is where the money flows live. It holds the amount, currency, status (completed/pending/failed), the raw SMS text for auditing, and timestamps. Each transaction belongs to one user and one category, so we link them via foreign keys. We also add checks: amounts can't be negative, currency is limited to RWF/ETB/USD, and status is locked to our three known values. Multiple indexes let us quickly find "all transactions from this user on this date" or "how many failed transfers did we process?"

A single transaction can have multiple fees applied to it; say, a transaction fee and a tax. At the same time, the same fee type might apply to hundreds of transactions. That's a many-to-many relationship, so we use a junction table called Transaction_fees. This lets us track which fees hit which transactions without storing messy arrays or duplicating data.

Finally, System_Logs captures pipeline errors and events (parse failures, batch start/end times) without cluttering the transaction tables. This helps us debug what went wrong without mixing operational data with financial facts.
