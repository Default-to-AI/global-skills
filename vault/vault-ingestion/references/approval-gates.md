# Vault Ingestion Approval Gates

Stop and ask Robert before taking these actions during ingestion:

- delete a durable note or raw capture;
- merge two durable notes;
- rename a durable wiki page;
- create or modify `Types/`;
- create a new domain or alter domain taxonomy;
- make a bulk rewrite across many files;
- overwrite source content beyond obvious metadata or formatting repair;
- route the source into a domain when the correct domain is genuinely ambiguous.

If an ingestion run hits one of these gates in background or cron mode, leave the item unprocessed, record the reason, and surface it in the report.
