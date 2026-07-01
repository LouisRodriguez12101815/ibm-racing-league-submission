# Self-reminder email — S3 cleanup after IBM submission
Copy-paste the block below into an email to yourself (or a calendar event) so you don't forget to shut down the public S3 bucket after the IBM Racing League judges finish reviewing.
Suggested send-to-self subject line and body:

---

**Subject:** ACTION: Delete IBM Racing League submission S3 bucket (~7 days after 2026-07-01)

**Body:**

Hey Louis,

You uploaded the MDC Racing IBM AI Racing League submission assets to a public S3 bucket in AWS account `637675605360` (us-east-1). Once judging is done, delete the bucket to stop storage + egress charges.

Assets currently in the bucket:
- Lap video: `mdc-racing-lap-corkscrew-2-23-96.mp4` (~170 MB)
- Livery: `mdc_racing_livery.jpg` (~500 KB)

Bucket name: `mdc-racing-ibm-submission-637675605360`

**Cleanup commands** (run in PowerShell on the machine with your AWS CLI configured):

```
aws s3 rm s3://mdc-racing-ibm-submission-637675605360 --recursive
aws s3 rb s3://mdc-racing-ibm-submission-637675605360
```

**Verify it's gone:**

```
aws s3api list-buckets --query "Buckets[?Name=='mdc-racing-ibm-submission-637675605360']" --output json
```
(An empty `[]` means the bucket is gone.)

Approximate charges if left running: ~$0.004/month storage + $0.09 per GB egress. Every judge who downloads = ~$0.015 in transfer.

Do not delete before judging concludes and any appeals window closes.
