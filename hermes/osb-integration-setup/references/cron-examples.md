# Cron Command Examples for OSB Integration

## Discipline Report (daily)
hermes cron create \
  --name "discipline-daily" \
  --deliver "telegram:-1003949932611:6" \
  --workdir "/" \
  "0 21 * * *" \
  "o2b discipline report --vault /c/Users/Tiger/Vault --telegram-target telegram:-1003949932611:6"

## Weekly Ideas
hermes cron create \
  --name "weekly-ideas" \
  --deliver "telegram:-1003949932611:7" \
  --workdir "/" \
  "0 10 * * 0" \
  "o2b brain ideas --vault /c/Users/Tiger/Vault --limit 5"

## Monthly Synthesis
hermes cron create \
  --name "monthly-synthesis" \
  --deliver "telegram:-1003949932611:8" \
  --workdir "/" \
  "0 8 1 * *" \
  "o2b brain monthly --vault /c/Users/Tiger/Vault --format markdown"

## Monthly Metrics Report
hermes cron create \
  --name "monthly-metrics" \
  --deliver "telegram:-1003949932611:9" \
  --workdir "/" \
  "0 9 1 * *" \
  "cat /c/Users/Tiger/Vault/Brain/metrics/*.jsonl | jq -s 'group_by(.surface) | map({surface: .[0].surface, count: length, latest: .[-1].payload})' | head -n 20"

## Quarterly Recall-Gate Effectiveness
hermes cron create \
  --name "quarterly-recall" \
  --deliver "telegram:-1003949932611:10" \
  --workdir "/" \
  "0 9 1 */3 *" \
  "cat /c/Users/Tiger/Vault/Brain/metrics/brain_recall_telemetry.jsonl | jq -s 'map(select(.operation == \"gate_summary\")) | .[-10:]'"

## Bi-monthly Self-Tuning Review
hermes cron create \
  --name "bimonthly-tuning" \
  --deliver "telegram:-1003949932611:11" \
  --workdir "/" \
  "0 10 1,15 * *" \
  "cat /c/Users/Tiger/Vault/Brain/metrics/self_tuning.jsonl | jq -s '.[-5:]'"